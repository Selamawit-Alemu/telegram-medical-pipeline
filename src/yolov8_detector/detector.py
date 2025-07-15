# src/yolov8_detector/detector.py

import logging
from typing import List, Tuple
from ultralytics import YOLO

class YOLOv8Detector:
    """
    YOLOv8 object detection wrapper class.
    Loads the model and runs detection on images.
    """

    def __init__(self, model_path: str = 'yolov8n.pt'):
        self.model_path = model_path
        try:
            self.model = YOLO(self.model_path)
            logging.info(f"Loaded YOLOv8 model from {self.model_path}")
        except Exception as e:
            logging.error(f"Error loading YOLOv8 model: {e}")
            raise

    def detect(self, image_path: str) -> List[Tuple[str, float]]:
        """
        Run detection on an image.

        Returns:
            List of tuples: (detected_class_name, confidence_score)
        """
        try:
            results = self.model(image_path)
            detections = []
            for result in results:
                for box in result.boxes:
                    cls_name = self.model.names[int(box.cls[0])]
                    confidence = float(box.conf[0])
                    detections.append((cls_name, confidence))
            return detections
        except Exception as e:
            logging.error(f"Error during detection on {image_path}: {e}")
            return []
