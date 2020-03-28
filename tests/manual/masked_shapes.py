import cv2
import numpy as np

from master_controller.image_preprocessing.movement_background_subtract import \
    MovementDetectorBackgroundSubtract

rects = [[50, 50, 20, 40], [25, 35, 40, 40]]

image = np.zeros((200, 200, 3), dtype=np.uint8)

# detections
color = (255, 255, 255)
cv2.circle(image, (40, 40), 20, color, -1)
cv2.circle(image, (10, 110), 30, color, -1)
cv2.rectangle(image, (110, 40), (150, 150), color, -1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

if __name__ == '__main__':
    movement = MovementDetectorBackgroundSubtract()
    rects = movement.find_movement_boxes(gray)
    image = movement.draw_color_mask(image)

    for rect in rects:
        cv2.rectangle(image, (rect.x, rect.y), (rect.x_end, rect.y_end),
                      (122, 122, 0), 1)

    cv2.imshow('s', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
