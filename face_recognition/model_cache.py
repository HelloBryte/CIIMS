"""
Face recognition model caching system
"""

import os
import pickle
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ModelCache:
    """Cache for face recognition models and related data"""

    def __init__(self, cache_dir="cache", model_file="model/trainer.yml", ttl_hours=24):
        self.cache_dir = cache_dir
        self.model_file = model_file
        self.ttl_hours = ttl_hours
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_cache_path(self, cache_name: str) -> str:
        """Get cache file path"""
        return os.path.join(self.cache_dir, f"{cache_name}.cache")

    def _is_cache_valid(self, cache_path: str) -> bool:
        """Check if cache file is still valid"""
        if not os.path.exists(cache_path):
            return False

        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        expiry_time = datetime.now() - timedelta(hours=self.ttl_hours)

        return file_time > expiry_time

    def _load_model_metadata(self) -> Dict[str, Any]:
        """Load model metadata including file modification time"""
        model_path = self.model_file
        if not os.path.exists(model_path):
            return {"exists": False}

        return {
            "exists": True,
            "modified_time": datetime.fromtimestamp(os.path.getmtime(model_path)),
            "size": os.path.getsize(model_path),
        }

    def cache_recognizer(self, cache_name: str = "recognizer") -> bool:
        """Cache the face recognizer model"""
        try:
            cache_path = self._get_cache_path(cache_name)

            # Check if we need to update cache
            if self._is_cache_valid(cache_path):
                metadata = self._load_model_metadata()
                cached_data = self.load_cache(cache_name)

                if cached_data and cached_data.get("model_metadata") == metadata:
                    logger.info("Using cached recognizer: %s", cache_name)
                    return True

            # Load and cache the model
            try:
                import cv2
            except ImportError:
                logger.error("Failed to import cv2")
                return False

            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
            except AttributeError:
                logger.error("LBPHFaceRecognizer not available in OpenCV")
                return False

            recognizer.read(self.model_file)

            # Cache metadata only (recognizer cannot be pickled)
            cache_data = {
                "model_metadata": self._load_model_metadata(),
                "cached_time": datetime.now(),
                "recognizer_cached": True,
            }

            with open(cache_path, "wb") as f:
                pickle.dump(cache_data, f)

            logger.info("Cached recognizer metadata: %s", cache_name)
            return True

        except Exception as e:
            logger.error("Failed to cache recognizer: %s", e)
            return False

    def load_cached_recognizer(self, cache_name="recognizer"):
        """Load cached recognizer model"""
        try:
            cache_data = self.load_cache(cache_name)
            if cache_data and cache_data.get("recognizer_cached"):
                # Load fresh recognizer from file
                try:
                    import cv2
                    
                    # Check if cv2.face module is available
                    if not hasattr(cv2, 'face'):
                        logger.error("cv2.face module not available. Please install opencv-contrib-python")
                        return None

                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    recognizer.read(self.model_file)
                    logger.info("Loaded cached recognizer: %s", cache_name)
                    return recognizer
                except AttributeError as e:
                    logger.error("cv2.face module not available: %s. Please install opencv-contrib-python", e)
                    return None
                except Exception as e:
                    logger.error("Failed to load recognizer from file: %s", e)
                    return None
        except Exception as e:
            logger.error("Failed to load cached recognizer: %s", e)
        return None

    def cache_user_map(
        self, user_map: Dict[int, str], cache_name: str = "user_map"
    ) -> bool:
        """Cache user mapping data"""
        try:
            cache_data = {"user_map": user_map, "cached_time": datetime.now()}

            cache_path = self._get_cache_path(cache_name)
            with open(cache_path, "wb") as f:
                pickle.dump(cache_data, f)

            logger.info(f"Cached user map: {len(user_map)} users")
            return True

        except Exception as e:
            logger.error(f"Failed to cache user map: {e}")
            return False

    def load_cached_user_map(
        self, cache_name: str = "user_map"
    ) -> Optional[Dict[int, str]]:
        """Load cached user mapping"""
        try:
            cache_data = self.load_cache(cache_name)
            if cache_data and "user_map" in cache_data:
                logger.info(
                    f"Loaded cached user map: {len(cache_data['user_map'])} users"
                )
                return cache_data["user_map"]
        except Exception as e:
            logger.error(f"Failed to load cached user map: {e}")
        return None

    def load_cache(self, cache_name: str) -> Optional[Dict[str, Any]]:
        """Load cache data"""
        cache_path = self._get_cache_path(cache_name)

        if not self._is_cache_valid(cache_path):
            return None

        try:
            with open(cache_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Failed to load cache {cache_name}: {e}")
            return None

    def clear_cache(self, cache_name: Optional[str] = None):
        """Clear cache - either specific cache or all caches"""
        if cache_name:
            cache_path = self._get_cache_path(cache_name)
            if os.path.exists(cache_path):
                os.remove(cache_path)
                logger.info(f"Cleared cache: {cache_name}")
        else:
            # Clear all caches
            for filename in os.listdir(self.cache_dir):
                if filename.endswith(".cache"):
                    os.remove(os.path.join(self.cache_dir, filename))
            logger.info("Cleared all caches")


# Global cache instance
model_cache = ModelCache()
