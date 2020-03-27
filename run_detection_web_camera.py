from master_controller.camera.camera_web import CameraWeb
from master_controller.controller import Controller
from master_controller.image_preprocessing.movement_background_subtract import \
    MovementDetectorBackgroundSubtract
from master_controller.music_player import MusicPlayer
from master_controller.video_recorder import VideoRecorder

if __name__ == '__main__':

    crow_player = MusicPlayer()

    camera = CameraWeb()
    detector = MovementDetectorBackgroundSubtract()
    video_recorder = VideoRecorder()

    controller = Controller(camera, detector, crow_player, video_recorder,
                            picture_show=True)
    controller.start_camera()

    while True:
        try:
            controller.process_detection()
        except KeyboardInterrupt:
            break

    controller.stop()
