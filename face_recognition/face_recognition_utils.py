import cv2
import time
import sys
import platform
from utils.database_helper import execute_query
from face_recognition.model_cache import model_cache
from utils.logging_config import get_logger

logger = get_logger(__name__)


def get_all_faces():
    """Get all users with face registration enabled"""
    try:
        sql = "SELECT user_id, user_name FROM users WHERE face_registered=1"
        results = execute_query(sql, dictionary=True)
        return {row["user_id"]: row["user_name"] for row in results}
    except Exception as e:
        logger.error(f"Error getting user faces: {e}")
        return {}


def get_cached_user_map():
    """Get user map from cache or database"""
    # Try to load from cache first
    cached_map = model_cache.load_cached_user_map()
    if cached_map is not None:
        return cached_map

    # Load from database and cache it
    user_map = get_all_faces()
    if user_map:
        model_cache.cache_user_map(user_map)

    return user_map


def get_cached_recognizer():
    """Get face recognizer from cache or load from file"""
    # Try to load from cache first
    cached_recognizer = model_cache.load_cached_recognizer()
    if cached_recognizer is not None:
        return cached_recognizer

    # Load from file and cache it
    try:
        # Check if cv2.face module is available
        if not hasattr(cv2, 'face'):
            error_msg = (
                "cv2.face module is not available.\n\n"
                "The virtual environment has opencv-python installed, but opencv-contrib-python is required.\n\n"
                "Please run the following commands to fix:\n"
                "pip uninstall opencv-python\n"
                "pip install opencv-contrib-python==4.10.0.84"
            )
            logger.error(error_msg)
            return None
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        model_path = "model/trainer.yml"
        
        # Check if model file exists
        import os
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            return None
        
        recognizer.read(model_path)
        model_cache.cache_recognizer()
        logger.info("Successfully loaded face recognizer model")
        return recognizer
    except AttributeError as e:
        error_msg = (
            f"OpenCV face module is not available: {e}\n\n"
            "Please install opencv-contrib-python (not opencv-python):\n"
            "pip uninstall opencv-python\n"
            "pip install opencv-contrib-python==4.10.0.84"
        )
        logger.error(error_msg)
        return None
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading face recognizer: {e}", exc_info=True)
        return None


def recognize_face():
    """Face recognition with caching support"""
    cap = None
    error_details = []
    
    try:
        # On macOS, OpenCV camera access can cause app crash if permission denied
        # We wrap everything in try-except to catch any issues
        logger.info("Attempting to open camera 0...")
        try:
            cap = cv2.VideoCapture(0)
            logger.info(f"VideoCapture(0) returned: {cap}")
            if cap is None:
                error_details.append("VideoCapture(0) returned None")
                raise Exception("VideoCapture returned None for camera 0")
            time.sleep(0.5)  # Give camera more time to initialize
            logger.info(f"Camera 0 isOpened: {cap.isOpened()}")
        except Exception as e:
            error_msg = f"Error opening camera 0: {e}"
            logger.error(error_msg, exc_info=True)
            error_details.append(error_msg)
            cap = None
        
        # CRITICAL: Check if camera opened successfully
        if cap is None or not cap.isOpened():
            logger.info("Camera 0 failed, trying camera 1...")
            try:
                cap = cv2.VideoCapture(1)
                logger.info(f"VideoCapture(1) returned: {cap}")
                if cap is None:
                    error_details.append("VideoCapture(1) returned None")
                    raise Exception("VideoCapture returned None for camera 1")
                time.sleep(0.5)
                logger.info(f"Camera 1 isOpened: {cap.isOpened()}")
            except Exception as e:
                error_msg = f"Error opening camera 1: {e}"
                logger.error(error_msg, exc_info=True)
                error_details.append(error_msg)
                cap = None
        
        # CRITICAL CHECK: Verify camera object exists and is opened
        if cap is None:
            error_message = "Unable to create camera object"
            if error_details:
                error_message += f"\n\nDetailed errors:\n" + "\n".join(error_details)
            error_message += "\n\nPlease check:\n1. System Settings > Privacy & Security > Camera - grant permission to Python\n2. Other applications may be using the camera\n3. Camera is connected"
            logger.error(error_message)
            return None, error_message
            
        if not cap.isOpened():
            if cap:
                try:
                    cap.release()
                except:
                    pass
            return None, "Unable to open camera.\n\nPlease check:\n1. Camera is connected\n2. System Settings > Privacy & Security > Camera - grant permission\n3. Other applications may be using the camera"
        
        # CRITICAL: Test if camera can actually read frames
        try:
            ret, test_frame = cap.read()
            # Validate frame - this is critical to prevent crashes
            if not ret:
                if cap:
                    try:
                        cap.release()
                    except:
                        pass
                return None, "Camera unable to read frame (ret=False)"
            if test_frame is None:
                if cap:
                    try:
                        cap.release()
                    except:
                        pass
                return None, "Camera unable to read frame (frame=None)"
            if test_frame.size == 0:
                if cap:
                    try:
                        cap.release()
                    except:
                        pass
                return None, "Camera read empty frame"
        except Exception as e:
            logger.error(f"Error reading test frame: {e}", exc_info=True)
            if cap:
                try:
                    cap.release()
                except:
                    pass
            return None, f"Camera read error: {str(e)}\n\nPlease check camera permission in system settings."
        
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # Get cached recognizer and user map
        recognizer = get_cached_recognizer()
        if recognizer is None:
            if cap:
                cap.release()
            return None, "Failed to load face recognition model"

        user_map = get_cached_user_map()
        if not user_map:
            if cap:
                cap.release()
            return None, "No registered face data found"

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                logger.warning("Failed to read frame from camera")
                continue

            # Validate frame before processing
            if frame is None or frame.size == 0:
                logger.warning("Invalid frame received")
                continue
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            recognized = False
            for x, y, w, h in faces:
                # Validate face region
                if x < 0 or y < 0 or x + w > gray.shape[1] or y + h > gray.shape[0]:
                    continue
                    
                try:
                    # Extract face region safely
                    face_roi = gray[y:y+h, x:x+w]
                    if face_roi.size == 0:
                        continue
                        
                    id, confidence = recognizer.predict(face_roi)
                    if confidence < 70:  # Confidence threshold
                        name = user_map.get(id, "Unknown")
                        if name != "Unknown":
                            # Release camera and return result immediately
                            recognized = True
                            break
                except Exception as e:
                    logger.warning(f"Recognition error: {e}")
                    continue
            
            # If recognized, clean up and return
            if recognized:
                if cap:
                    try:
                        cap.release()
                    except:
                        pass
                try:
                    cv2.destroyAllWindows()
                except:
                    pass
                return name, "Face recognition successful"
            
            # Don't use cv2.imshow in thread - it causes crashes
            # Just process frames without display
            # Limit processing time to avoid infinite loop
            if not hasattr(recognize_face, '_start_time'):
                recognize_face._start_time = time.time()
            
            if time.time() - recognize_face._start_time > 30:  # 30 second timeout
                break

        if cap:
            try:
                cap.release()
            except:
                pass
        try:
            cv2.destroyAllWindows()
        except:
            pass
        # Clean up timer
        if hasattr(recognize_face, '_start_time'):
            del recognize_face._start_time
        return None, "No face recognized, please ensure adequate lighting and face the camera"

    except cv2.error as e:
        logger.error(f"OpenCV error: {e}")
        if cap:
            try:
                cap.release()
            except:
                pass
        try:
            cv2.destroyAllWindows()
        except:
            pass
        return None, f"Camera error: {str(e)}\nPlease check camera permission in system settings"
    except KeyboardInterrupt:
        logger.warning("Face recognition interrupted by user")
        if cap:
            try:
                cap.release()
            except:
                pass
        try:
            cv2.destroyAllWindows()
        except:
            pass
        return None, "Face recognition cancelled"
    except Exception as e:
        logger.error(f"Unexpected error in face recognition: {e}", exc_info=True)
        if cap:
            try:
                cap.release()
            except:
                pass
        try:
            cv2.destroyAllWindows()
        except:
            pass
        return None, f"Error during face recognition: {str(e)}\nPlease check camera permission and connection"
