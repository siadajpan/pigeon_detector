from typing import Tuple, List

import cv2
import numpy as np


def group_rectangles(rectangles: List[Tuple[int, int, int, int]]):
    rectangles = np.asarray(rectangles)
    max_x = np.max(rectangles[:, 2])
    max_y = np.max(rectangles[:, 3])
    temp_image = np.zeros((max_y + 1, max_x + 1), dtype=np.uint8)

    for rect in rectangles:
        x0, y0, xe, ye = rect
        cv2.rectangle(temp_image, (x0, y0), (xe, ye), (255, 0, 0), -1)

    cnts, _ = cv2.findContours(temp_image, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)

    rects_out = np.asarray([cv2.boundingRect(cnt) for cnt in cnts])
    rects_out[:, 2] += rects_out[:, 0]
    rects_out[:, 3] += rects_out[:, 1]

    return rects_out


if __name__ == '__main__':
    image = np.zeros((60, 100, 3), dtype=np.uint8)
    temp_image = np.zeros(image.shape[:2], dtype=np.uint8)

    overlap_distance = 1

    rect1 = (10, 10, 20, 20)
    rect2 = (25, 27, 40, 45)
    rect3 = (8, 12, 25, 50)
    rect4 = (60, 10, 80, 40)

    rectangles = [rect1, rect2, rect3, rect4]

    for rect in rectangles:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 1)

    rects = group_rectangles(rectangles)

    print(rects)
    for rect in rects:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 1)

    cv2.imshow('f', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()