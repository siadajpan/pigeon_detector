import datetime
import time
from os.path import join

import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    time.sleep(1)
    ret, frame = cap.read()
    now = datetime.datetime.now()
    time_desc = now.strftime('%m_%d__%H_%M_%S')

    cv2.imwrite(join('/home/pi/Pictures', time_desc + '.jpg'), frame)
