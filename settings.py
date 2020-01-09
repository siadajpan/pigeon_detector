import os


CAMERA_RESOLUTION = (1024, 768)
CAMERA_FRAMERATE = 32
NOISE_LENGTH = 24
NEW_BASE_TIME = 25
SETTINGS_PATH = os.path.realpath(__file__)
PROJECT_PATH = os.path.dirname(SETTINGS_PATH)


class Server:
    DETECTION_ADDRESS = 'http://192.168.1.66:5000'
    IMAGE_PROCESSING = '/process_image'
    CONNECTION_CHECK = '/connection_check'
    MOVEMENT_ADDRESSES = ['http://192.168.1.16:5000']
    MOVEMENT = '/movement'


SERVO_PORT = 11


def create_path(path: str):
    return os.path.join(PROJECT_PATH, path)


PICTURES_FOLDER = create_path('pictures/non_birds/')
BIRDS_FOLDER = '/home/pi/Pictures'
MUSIC_PATH = create_path('master_controller/files/crows.mp3')
YOLO_CONFIG_FOLDER = create_path('detection/yolo_coco/')


class YoloFiles:
    COCO_NAMES = 'coco.names'
    CONFIG = 'yolov3.cfg'
    WEIGHTS = 'yolov3.weights'


class SimpleDetection:
    MAX_SIZE = 200
    MIN_SIZE = 5
