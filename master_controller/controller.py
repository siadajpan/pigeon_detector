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
                 music_player: MusicPlayer, picture_show: bool = False):
        self._camera = camera
        self._movement_detector = detector
        self._music_player = music_player
        self._playing_music = False
        self._picture_show = picture_show
        self._local_detector = LocalDetectionRunner()
        self._server_detector = ServerDetectionRunner()
        self._detector_in_use = self._local_detector
        self._last_detection_time = 0

    def start_camera(self):
        self._camera.start()

    def start_detector(self):
        self._movement_detector.start()

    def start_music_player(self):
        self._music_player.start()
        self._playing_music = True

    def stop_music_player(self):
        self._music_player.stop()
        self._playing_music = False

    def stop(self):
        self._camera.stop()
        self._movement_detector.stop()
        self.stop_music_player()

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
        cv2.imshow('detection', image)
        if cv2.waitKey(1) == ord('q'):
            raise KeyboardInterrupt

    def check_detection(self):
        if self._playing_music:
            self.check_music_timeout()
            return

        detection = self.check_detection_time()
        if detection:
            self.save_picture()
            self.start_movement()
            self.start_music_player()

    def choose_detector(self):
        if self._server_detector.check_connection():
            self._detector_in_use = self._server_detector
        else:
            self._detector_in_use = self._local_detector

    def send_update_to_detector(self, picture_to_analyze, movements):
        self._detector_in_use.update_image(picture_to_analyze)
        self._detector_in_use.update_movement_boxes(movements)
        self._detector_in_use.send_image()

    def update_picture_to_detector_if_not_processing(self):
        if self._detector_in_use.processing:
            return

        picture_to_analyze = self._movement_detector.curr_frame
        movements = self._movement_detector.movement_boxes
        
        if picture_to_analyze is None or movements is None:
            return

        self.send_update_to_detector(picture_to_analyze, movements)

    def process_detection(self):
        self._movement_detector.add_frame(self._camera.image)
        self.choose_detector()

        self.update_picture_to_detector_if_not_processing()

        if self._picture_show:
            self.show_picture()

        self.check_detection()

        time.sleep(1)
