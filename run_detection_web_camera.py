
import time

from master_controller.camera.camera_web import CameraWeb
from master_controller.controller import Controller
from master_controller.music_player import MusicPlayer
from master_controller.image_preprocessing.movement_detector import \
    MovementDetector

if __name__ == '__main__':
    
    crow_player = MusicPlayer()

    camera = CameraWeb(show_frame=False)
    detector = MovementDetector()

    # allow the camera to warm up
    time.sleep(0.1)
    
    controller = Controller(camera, detector, crow_player)
    controller.start_camera()
    controller.start_detector()

    while True:
        try:
            stop = controller.process_detection()
        except KeyboardInterrupt:
            break
        if stop:
            break

    controller.stop()
