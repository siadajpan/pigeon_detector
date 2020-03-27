import cv2
import numpy as np

import settings

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    background = cv2.createBackgroundSubtractorMOG2(varThreshold=30,
                                                    detectShadows=False)

    while True:
        _, frame = cap.read()

        foreground = background.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        foreground = cv2.dilate(foreground, kernel)
        if np.mean(foreground) > 10:
            continue

        contours, _ = cv2.findContours(foreground, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 100 > w > 5 and 100 > h > 5:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (155, 255, 12))
                boxes.append([x, y, w, h])

        new_boxes = cv2.dnn.NMSBoxes(boxes, np.ones(len(boxes)), 0.5, 0.5)

        print(new_boxes)
        for indices in new_boxes:
            x, y, w, h = boxes[indices[0]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 212))

        cv2.imshow('f', frame)
        cv2.imshow('g', foreground)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
