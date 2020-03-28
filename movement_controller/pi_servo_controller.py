from time import sleep

import RPi.GPIO as GPIO

import settings


class PiServoController:
    def __init__(self, pwm_speed: int = 30):
        self.port = settings.SERVO_PORT
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        self.pwm = GPIO.PWM(self.port, pwm_speed)
        self.init_servo()

    def init_servo(self):
        self.pwm.start(0)

    def move_servo(self):
        self.set_angle(10)
        self.set_angle(60)

    def set_angle(self, angle):
        duty = angle / 10
        self.pwm.ChangeDutyCycle(duty)
        sleep(0.2)
        self.pwm.ChangeDutyCycle(0)
        sleep(0.2)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
