from threading import Thread
from typing import List

import cv2
import numpy as np

import settings
from master_controller.image_preprocessing import rectangles_connector
from master_controller.image_preprocessing.rectangle import Rectangle


class MovementDetectorBackgroundSubtract:
    def __init__(self):
        self.movement_boxes: List[Rectangle] = []
        self.background_subtractor = cv2.createBackgroundSubtractorKNN(
            history=settings.PreProcessing.HISTORY,
            dist2Threshold=settings.PreProcessing.DIST_TO_THRESHOLD,
            detectShadows=settings.PreProcessing.DETECT_SHADOWS
        )
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    def find_contours(self, binary_image):
        binary_image = cv2.erode(binary_image, self.kernel)
        binary_image = cv2.dilate(binary_image, self.kernel)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def analyze_contours(self, contours):
        max_size = settings.PreProcessing.MAX_SIZE
        min_size = settings.PreProcessing.MIN_SIZE

        boxes = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if max_size > w > min_size and max_size > h > min_size:
                boxes.append((x, y, x + w, y + h))

        if len(boxes) == 0:
            return boxes

        rects = rectangles_connector.group_rectangles(boxes)

        return rects

    def find_movement_boxes(self, binary_image):
        contours = self.find_contours(binary_image)
        boxes = self.analyze_contours(contours)
        rectangles = [Rectangle(box[0], box[1], box[2] - box[0],
                                box[3] - box[1]) for box in boxes]

        return rectangles

    def analyze_image(self, image: np.array):
        foreground = self.background_subtractor.apply(image)
        rectangles = self.find_movement_boxes(foreground)

        return rectangles
