import os

CAMERA_RESOLUTION = (1024, 768)
CAMERA_FRAMERATE = 32
NOISE_LENGTH = 10
NEW_BASE_TIME = 10
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


class PreProcessing:
    HISTORY = 1000
    DIST_TO_THRESHOLD = 300
    DETECT_SHADOWS = True
    MAX_SIZE = 2000
    MIN_SIZE = 10


class SimpleDetection:
    MAX_SIZE = 2000
    MIN_SIZE = 10


class MovementIgnoredShapes:
    # in image scale (0-1) x0, y0, w, h
    # balcony
    RECTANGLES = [[0.0, 0.4, 0.2, 0.2]]


class Video:
    MIN_LENGTH = 10
    FPS = 10
