# from pigeon_shooter.camera.camera_pi import CameraPi
# from pigeon_shooter.controller import Controller
# from processing_server.image_preprocessing.detector import Detector
# from pigeon_shooter.music_player import MusicPlayer
# import time
#
#
# if __name__ == '__main__':
#
#     crow_player = MusicPlayer()
#
#     camera = CameraPi(show_frame=False)
#     detector = Detector()
#
#     # allow the camera to warm up
#     time.sleep(0.1)
#
#     controller = Controller(camera, detector, crow_player)
#     controller.start_camera()
#     controller.start_detector()
#     controller.poll_camera_detection()
#
#     controller.stop()
