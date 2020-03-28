import time

import cv2
import numpy as np

import settings
from master_controller.camera.generic_camera import GenericCamera
from master_controller.detection_runners.local_detection_runner import \
    LocalDetectionRunner
from master_controller.image_preprocessing.movement_background_subtract import \
    MovementDetectorBackgroundSubtract
from master_controller.video_recorder import VideoRecorder


class NoMovementController:
    def __init__(self, camera: GenericCamera,
                 movement_detector: MovementDetectorBackgroundSubtract,
                 video_recorder: VideoRecorder,
                 picture_show: bool = False):
        self._camera = camera
        self._movement_detector = movement_detector
        self._classifier = LocalDetectionRunner()
        self._video_recorder = video_recorder
        self._picture_show = picture_show
        self._last_detection_time = 0
        self._recording = False

    def start_camera(self):
        self._camera.start()

    def start_recording(self, frame):
        fps = settings.Video.FPS
        self._video_recorder.init_recording(frame, fps)
        self._recording = True

    def stop_recording(self):
        self._video_recorder.stop_recording()
        self._recording = False

    def stop(self):
        self._camera.stop()
        self.stop_recording()

    @staticmethod
    def flip_image(image):
        image_flipped = cv2.flip(image, -1)
        return image_flipped

    def check_detection_time(self):
        detection_time = self._classifier.last_detection_time
        detection = time.time() - detection_time < settings.Video.MIN_LENGTH

        return detection

    def get_image_with_movement(self) -> np.array:
        """
        Get current frame from camera together with latest classified boxes

        :return: image
        """
        image = self._camera.get_current_frame().copy()
        boxes = self._classifier.movement_boxes

        for rect in boxes:
            cv2.rectangle(
                image, (rect.x, rect.y), (rect.x_end, rect.y_end), (0, 0, 255)
            )

        return image

    def show_picture(self):
        image = self.get_image_with_movement()
        image = self._movement_detector.draw_color_mask(image)
        cv2.imshow('detection', image)
        if cv2.waitKey(1) == ord('q'):
            raise KeyboardInterrupt

    def check_detection(self):
        image = self._camera.get_current_frame()
        detection_present = self.check_detection_time()

        if self._recording:
            self._video_recorder.update_frame(image)

        if self._recording and not detection_present:
            print('stopping recording')
            self.stop_recording()

        if not self._recording and detection_present:
            print('starting recording')
            self.start_recording(image)

    def send_update_to_detector(self, picture_to_analyze, movements):
        self._classifier.update_image(picture_to_analyze)
        self._classifier.update_movement_boxes(movements)
        self._classifier.send_image()

    def update_picture_to_detector_if_not_processing(self, image: np.array):
        if self._classifier.processing:
            return

        movements = self._movement_detector.analyze_image(image)
        if movements is None:
            return

        self.send_update_to_detector(image, movements)

    def process_detection(self):
        if self._camera.image is None:
            return

        self.update_picture_to_detector_if_not_processing(self._camera.image)

        if self._picture_show:
            self.show_picture()

        self.check_detection()
