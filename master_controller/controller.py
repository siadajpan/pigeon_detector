import requests

import settings
from master_controller.camera.generic_camera import GenericCamera
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
from master_controller.detection_runners.local_detection_runner import \
    LocalDetectionRunner
from master_controller.detection_runners.server_detection_runner import \
    ServerDetectionRunner
from master_controller.music_player import MusicPlayer
from settings import NOISE_LENGTH, PICTURES_FOLDER, BIRDS_FOLDER
from master_controller.image_preprocessing.movement_detector import \
    MovementDetector
from os.path import join
import time
import datetime
import cv2


LOCAL_DETECTOR = 'LOCAL_DETECTOR'
SERVER_DETECTOR = 'SERVER_DETECTOR'


class Controller:
    def __init__(self, camera: GenericCamera, detector: MovementDetector,
                 music_player: MusicPlayer):
        self._camera: GenericCamera = camera
        self._movement_detector: MovementDetector = detector
        self._music_player: MusicPlayer = music_player
        self._playing_music: bool = False
        self._picture_show = False
        self._local_detector = LocalDetectionRunner()
        self._server_detector = ServerDetectionRunner()
        self._detector_in_use: AbstractDetectionRunner = self._local_detector

    def start_camera(self):
        self._camera.start()

    def start_detector(self):
        self._movement_detector.start()

    def stop(self):
        self.stop_camera()
        self.stop_detector()
        self.stop_music_player()

    def stop_detector(self):
        self._movement_detector.stop()

    def stop_camera(self):
        self._camera.stop()

    def start_music_player(self):
        self._music_player.start()
        self._playing_music = True

    @staticmethod
    def start_movement():
        try:
            requests.post(settings.Server.MOVEMENT_ADDRESSES[0]
                          + settings.Server.MOVEMENT)
        except requests.exceptions.ConnectionError:
            return

    def stop_music_player(self):
        self._music_player.stop()
        self._playing_music = False

    def save_picture(self, desc: str = '', birds=True):
        print('saving picture')
        saving_folder = BIRDS_FOLDER if birds else PICTURES_FOLDER
        now = datetime.datetime.now()
        time_desc = now.strftime('%m_%d__%H_%M_%S')
        cv2.imwrite(join(saving_folder, time_desc + desc + '.jpg'),
                    self._movement_detector.movement_frame)

    def music_timeout(self):
        return time.time() - self._detector_in_use.last_detection_time \
               > NOISE_LENGTH

    def check_music_timeout(self):
        if self._playing_music and self.music_timeout():
            self.stop_music_player()
            self.save_picture('_movement_stopped', False)

    def show_picture(self):
        try:
            if self._movement_detector.movement_area:
                x, y, w, h = self._movement_detector.movement_area.data
                cv2.rectangle(
                    self._camera.image, (x, y), (x + w, y + h), (200, 200, 104)
                )

            cv2.imshow('detected', self._camera.image)

        except cv2.error:
            return

    def check_detection(self):
        if not self.music_timeout():
            if not self._playing_music:
                self.save_picture()
                self.start_movement()
                self.start_music_player()

        elif self._playing_music:
            self.stop_music_player()

    def choose_detector(self):
        if self._server_detector.check_connection():
            self._detector_in_use = self._server_detector
        else:
            self._detector_in_use = self._local_detector

    def update_picture_to_detector(self):
        picture_to_analyze = self._movement_detector.movement_frame
        if picture_to_analyze is None:
            return

        if not self._detector_in_use.processing:
            self._detector_in_use.update_image(picture_to_analyze)
            self._detector_in_use.process_image()

    def process_detection(self):
        self._movement_detector.add_frame(self._camera.image)
        self.choose_detector()

        if not self._detector_in_use.processing:
            self.update_picture_to_detector()

        if self._picture_show:
            self.show_picture()

            if cv2.waitKey(1) == ord('q'):
                return True

        self.check_detection()

        time.sleep(1)
