import datetime
import time
from os.path import join

import cv2
import numpy as np
import requests

import settings
from master_controller.camera.generic_camera import GenericCamera
from master_controller.detection_runners.local_detection_runner import \
    LocalDetectionRunner
from master_controller.detection_runners.server_detection_runner import \
    ServerDetectionRunner
from master_controller.image_preprocessing.movement_background_subtract import \
    MovementDetectorBackgroundSubtract
from master_controller.music_player import MusicPlayer
from master_controller.video_recorder import VideoRecorder
from settings import NOISE_LENGTH, BIRDS_FOLDER

LOCAL_DETECTOR = 'LOCAL_DETECTOR'
SERVER_DETECTOR = 'SERVER_DETECTOR'


class Controller:
    def __init__(self, camera: GenericCamera,
                 detector: MovementDetectorBackgroundSubtract,
                 music_player: MusicPlayer, video_recorder: VideoRecorder,
                 picture_show: bool = False):
        self._camera = camera
        self._movement_detector = detector
        self._music_player = music_player
        self._video_recorder = video_recorder
        self._playing_music = False
        self._picture_show = picture_show
        self._local_detector = LocalDetectionRunner()
        self._server_detector = ServerDetectionRunner()
        self._detector_in_use = self._local_detector
        self._last_detection_time = 0

    def start_camera(self):
        self._camera.start()

    def start_music_player(self):
        self._music_player.start()
        self._playing_music = True

    def stop_music_player(self):
        self._music_player.stop()
        self._playing_music = False

    def start_recording(self, frame, fps):
        self._video_recorder.init_recording(frame, fps)

    def stop_recording(self):
        self._video_recorder.stop_recording()

    def stop(self):
        self._camera.stop()
        self.stop_music_player()
        self.stop_recording()

    @staticmethod
    def start_movement():
        try:
            requests.post(settings.Server.MOVEMENT_ADDRESSES[0]
                          + settings.Server.MOVEMENT, timeout=0.1)
        except requests.exceptions.ConnectionError:
            return
        except requests.exceptions.Timeout:
            return

    @staticmethod
    def flip_image(image):
        image_flipped = cv2.flip(image, -1)
        return image_flipped

    def save_picture(self, desc: str = ''):
        saving_folder = BIRDS_FOLDER
        now = datetime.datetime.now()
        time_desc = now.strftime('%m_%d__%H_%M_%S')
        image = self.get_image_with_movement()
        image_flipped = self.flip_image(image)
        cv2.imwrite(join(saving_folder, time_desc + desc + '.jpg'),
                    image_flipped)

    def music_timeout(self):
        time_gone = time.time() - self._last_detection_time

        return time_gone > NOISE_LENGTH

    def check_detection_time(self):
        detection_time = self._detector_in_use.last_detection_time
        detection = time.time() - detection_time < NOISE_LENGTH

        if detection:
            self._last_detection_time = detection_time

        return detection

    def check_music_timeout(self):
        if self.music_timeout():
            self.stop_music_player()
            self.stop_recording()

    def get_image_with_movement(self):
        image = self._camera.get_current_frame().copy()
        last_detections = self._detector_in_use.last_detections
        if last_detections is None:
            return image

        for rect in self._detector_in_use.last_detections:
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

        if self._playing_music:
            self._video_recorder.update_frame(image)
            self.check_music_timeout()
            return

        detection = self.check_detection_time()
        if detection:
            self.save_picture()
            self.start_movement()
            self.start_music_player()
            self.start_recording(image, 30)

    def choose_detector(self):
        if self._server_detector.check_connection():
            self._detector_in_use = self._server_detector
        else:
            self._detector_in_use = self._local_detector

    def send_update_to_detector(self, picture_to_analyze, movements):
        self._detector_in_use.update_image(picture_to_analyze)
        self._detector_in_use.update_movement_boxes(movements)
        self._detector_in_use.send_image()

    def update_picture_to_detector_if_not_processing(self, image: np.array):
        if self._detector_in_use.processing:
            return

        movements = self._movement_detector.analyze_image(image)
        if movements is None:
            return

        self.send_update_to_detector(image, movements)

    def process_detection(self):
        self.choose_detector()
        self.update_picture_to_detector_if_not_processing(self._camera.image)

        if self._picture_show:
            self.show_picture()

        self.check_detection()
