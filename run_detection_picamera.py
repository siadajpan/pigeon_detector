import time

from master_controller.camera.camera_pi import CameraPi
from master_controller.image_preprocessing.movement_background_subtract import \
    MovementDetectorBackgroundSubtract
from master_controller.no_movement_controller import NoMovementController
from master_controller.video_recorder import VideoRecorder

if __name__ == '__main__':
    camera = CameraPi()
    detector = MovementDetectorBackgroundSubtract()
    video_recorder = VideoRecorder()

    # allow the camera to warm up
    time.sleep(1)

    controller = NoMovementController(camera, detector, video_recorder, True)
    controller.start_camera()

    while True:
        try:
            controller.process_detection()
        except KeyboardInterrupt:
            break

    controller.stop()
