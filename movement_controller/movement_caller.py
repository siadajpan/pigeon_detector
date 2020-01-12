import time
from threading import Thread
from typing import Callable

from movement_controller.pi_servo_controller import PiServoController


class MovementCaller(Thread):
    # Object that runs servo controller. This object is initialized each time
    # we want to start servo movement
    def __init__(self, servo_controller: PiServoController,
                 movement_callback: Callable):
        super().__init__()
        self.servo_controller = servo_controller
        self.movement_callback = movement_callback

    def run(self):
        for i in range(10):
            self.servo_controller.move_servo()
            time.sleep(0.5)

        self.movement_callback()
