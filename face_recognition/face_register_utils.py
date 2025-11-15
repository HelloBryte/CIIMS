import cv2
import os
import numpy as np
from utils.logging_config import get_logger

logger = get_logger(__name__)


def capture_for_register(user_id, num=10):
    """Capture face images for registration"""
    cam = None
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            cam = cv2.VideoCapture(1)
        if not cam.isOpened():
            raise Exception("Unable to open camera, please check camera connection and permission settings")
        
        # Test if camera can actually read frames (for macOS permission check)
        ret, test_frame = cam.read()
        if not ret or test_frame is None:
            raise Exception("Camera permission denied, please grant camera permission in system settings")
        
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        save_path = f"dataset/{user_id}"
        os.makedirs(save_path, exist_ok=True)

        count = 0
        print("Starting face data collection...")

        while True:
            ret, img = cam.read()
            if not ret or img is None:
                logger.warning("Failed to read frame from camera")
                continue
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                count += 1
                cv2.imwrite(f"{save_path}/{count}.jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

            cv2.imshow("register", img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

            if count >= num:
                break

        if cam:
            cam.release()
        cv2.destroyAllWindows()
        print("Collection completed")
        
    except cv2.error as e:
        logger.error(f"OpenCV error in capture_for_register: {e}")
        if cam:
            cam.release()
        cv2.destroyAllWindows()
        raise Exception(f"Camera error: {str(e)}")
    except Exception as e:
        logger.error(f"Error in capture_for_register: {e}", exc_info=True)
        if cam:
            cam.release()
        cv2.destroyAllWindows()
        raise


def train_one_user(user_id):
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Read existing model (if exists)
    model_path = "model/trainer.yml"
    if os.path.exists(model_path):
        recognizer.read(model_path)

    user_path = f"dataset/{user_id}"
    samples = []
    labels = []

    for img in os.listdir(user_path):
        path = f"{user_path}/{img}"
        gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        samples.append(gray)
        labels.append(user_id)

    recognizer.update(samples, np.array(labels))

    os.makedirs("model", exist_ok=True)
    recognizer.save(model_path)

    print("Incremental training completed")
