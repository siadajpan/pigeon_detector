from typing import Optional

from movement_controller.movement_caller import MovementCaller
from movement_controller.pi_servo_controller import PiServoController


class MovementController:
    # Object that is initialized once. Every time we want to start servo,
    # it changes moving state to True and initializes movement with callback
    # that changes the moving state back to False
    def __init__(self):
        self.moving = False
        self.servo_controller = PiServoController()
        self.movement_caller = None

    def stopped_movement(self):
        self.moving = False

    def start_movement(self):
        if self.moving:
            return

        self.start_servo()

    def start_servo(self):
        self.moving = True
        self.movement_caller = MovementCaller(self.servo_controller,
                                              self.stopped_movement)
        self.movement_caller.start()
