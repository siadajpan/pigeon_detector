import time
from threading import Thread
from typing import Optional, List

import cv2
import numpy as np

import settings
from master_controller.image_preprocessing.rectangle import Rectangle


class MovementDetector(Thread):
    def __init__(self):
        super().__init__()
        self.curr_frame: Optional[np.array] = None
        self._base_frame: Optional[np.array] = None
        self._base_frame_time: float = 0.
        self._stop_detector: bool = False
        self.movement_boxes: Optional[List[Rectangle]] = None
        self.contours: Optional[np.array] = None

    def stop(self):
        self._stop_detector = True

    def add_frame(self, frame):
        self.curr_frame = frame

    @staticmethod
    def pre_process_image(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        return gray

    def update_base_frame(self, frame):
        self._base_frame = frame.copy()
        self._base_frame = self.pre_process_image(self._base_frame)
        self._base_frame_time = time.time()

    @staticmethod
    def cut_frame(frame: np.array, rectangle: Rectangle):
        box = rectangle.data
        x = box[0]
        y = box[1]
        x_end = box[0] + box[2]
        y_end = box[1] + box[3]

        return frame[y: y_end, x: x_end]

    @staticmethod
    def find_first_non_zero_row(array_2d: np.array):
        for index, row in enumerate(array_2d):
            if any(row):
                return index

        return None

    def find_contour(self, bin_frame: np.array):
        # finds rectangle contour around all non-zero elements in binary array
        contours, _ = cv2.findContours(bin_frame, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contours
        rectangles = [Rectangle(*cv2.boundingRect(contour))
                      for contour in contours]

        return rectangles

    @staticmethod
    def find_array_difference(base_frame: np.array, gray_array: np.array):
        frame_diff = cv2.absdiff(base_frame, gray_array)
        min_pixel_difference = settings.PreProcessing.MIN_PIXEL_DIFFERENCE
        _, thresh = cv2.threshold(frame_diff, min_pixel_difference, 255,
                                  cv2.THRESH_BINARY)
        kernel = np.ones((51, 51))
        dilation = cv2.dilate(thresh, kernel)
        erosion = cv2.erode(dilation, kernel)

        return erosion

    def select_movement_contours(self):
        gray = self.pre_process_image(self.curr_frame)
        difference_binary = self.find_array_difference(self._base_frame, gray)
        self.movement_boxes = self.find_contour(difference_binary)

    def check_if_update_base_frame(self):
        return time.time() - self._base_frame_time > settings.NEW_BASE_TIME

    def update_base_and_select_movement(self):
        if self.check_if_update_base_frame():
            self.update_base_frame(self.curr_frame)

        self.select_movement_contours()

    def run(self):
        while not self._stop_detector:
            if self.curr_frame is None:
                time.sleep(0.1)
                continue

            self.update_base_and_select_movement()
