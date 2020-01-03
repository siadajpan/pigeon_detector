from threading import Thread
from typing import Optional
import time
import cv2
import numpy as np
import settings
from master_controller.image_preprocessing.rectangle import Rectangle


class MovementDetector(Thread):
    def __init__(self):
        super().__init__()
        self.birds_detected = False
        self.curr_frame: Optional[np.array] = None
        self.base_frame: Optional[np.array] = None
        self.movement_frame: Optional[np.array] = None
        self.base_frame_time: float = 0.
        self.stop_detector: bool = False
        self.movement_area: Rectangle = Rectangle(0, 0, 0, 0)
        self.use_self_detector = True

    def stop(self):
        self.stop_detector = True
        
    def add_frame(self, frame):
        self.curr_frame = frame

    @staticmethod
    def preprocess_image(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        return gray
        
    def update_base_frame(self, frame):
        self.base_frame = frame.copy()
        self.base_frame = self.preprocess_image(self.base_frame)
        self.base_frame_time = time.time()

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
        indexes = []
        height, width = bin_frame.shape[:2]

        for i in range(4):
            index = self.find_first_non_zero_row(bin_frame)

            if index is None:
                return None

            indexes.append(index)
            bin_frame = np.rot90(bin_frame)

        y_top, x_right, y_bot, x_left = indexes
        x_width = width - x_right - x_left
        y_height = height - y_bot - y_top

        return Rectangle(x_left, y_top, x_width, y_height)

    @staticmethod
    def find_array_difference(base_frame: np.array, gray_array: np.array):
        frame_diff = cv2.absdiff(base_frame, gray_array)
        thresh = cv2.threshold(frame_diff, 55, 255, cv2.THRESH_BINARY)[1]
        return cv2.dilate(thresh, None, iterations=2)

    def select_movement_contours(self, frame):
        gray = self.preprocess_image(frame)
        difference_binary = self.find_array_difference(self.base_frame, gray)
        self.movement_area = self.find_contour(difference_binary)

    def cut_frame_by_movement(self, frame):
        self.select_movement_contours(frame)
        if self.movement_area:
            frame = self.cut_frame(frame, self.movement_area)
            return frame

        return None

    def preprocess_frame(self):
        frame = self.curr_frame.copy()
        frame = self.cut_frame_by_movement(frame)

        if frame is None:
            self.movement_frame = None
            return

        if frame.shape[0] < 4 or frame.shape[1] < 4:
            self.movement_frame = None
            return

        self.movement_frame = frame

    def check_if_update_base_frame(self):
        return time.time() - self.base_frame_time > settings.NEW_BASE_TIME

    def run(self):
        while not self.stop_detector:
            if self.curr_frame is None:
                time.sleep(0.1)
                continue

            if self.check_if_update_base_frame():
                self.update_base_frame(self.curr_frame)

            self.preprocess_frame()
