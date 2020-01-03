from typing import Optional, Tuple
import numpy as np
import time
import cv2
import os
import settings


class YOLODetector:
    def __init__(self):
        self.config_folder = settings.YOLO_CONFIG_FOLDER
        self.labels = self.init_labels()
        self.colors = self.init_colors()
        self.net = self.init_net()
        self.layer_names = self.init_output_layer_names()
        self.min_confidence = 0.5
        self.threshold = 0.3
        self.boxes = []
        self.confidences = []
        self.class_ids = []
        self.image_shape: Optional[Tuple[int, int]] = None

    def reset_detection(self):
        self.boxes = []
        self.confidences = []
        self.class_ids = []

    def init_labels(self):
        labels_path = os.path.join(self.config_folder,
                                   settings.YoloFiles.COCO_NAMES)
        with open(labels_path) as label_file:
            labels = label_file.read().strip().split("\n")

        return labels

    def init_colors(self):
        colors = np.random.randint(0, 255, size=(len(self.labels), 3),
                                   dtype="uint8")
        return colors

    def init_net(self):
        weights_path = os.path.join(self.config_folder,
                                    settings.YoloFiles.WEIGHTS)
        if not os.path.exists(weights_path):
            raise FileNotFoundError(
                'YOLO weights has not been found. Please find the information '
                'about how to download weights in README.md file.')
        config_path = os.path.join(self.config_folder,
                                   settings.YoloFiles.CONFIG)
        net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

        return net

    def init_output_layer_names(self):
        layer_names = self.net.getLayerNames()
        layer_names = [layer_names[i[0] - 1]
                       for i in self.net.getUnconnectedOutLayers()]

        return layer_names

    @staticmethod
    def image_to_blob(image_):
        return cv2.dnn.blobFromImage(image_, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)

    def forward_net(self, image_):
        blob = self.image_to_blob(image_)
        self.net.setInput(blob)
        start = time.time()
        layer_outputs = self.net.forward(self.layer_names)
        end = time.time()
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))
        return layer_outputs

    @staticmethod
    def calculate_left_top(center_x, center_y, width, height):
        # use the center (x, y)-coordinates to derive the top and
        # and left corner of the bounding box
        x = int(center_x - (width / 2))
        y = int(center_y - (height / 2))

        return x, y

    def process_detection(self, detection):
        # extract the class ID and confidence (i.e., probability) of
        # the current object image_preprocessing
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        (H, W) = self.image_shape
        # filter out weak predictions by ensuring the detected
        # probability is greater than the minimum probability
        if confidence > self.min_confidence:
            # scale the bounding box coordinates back relative to the
            # size of the image, keeping in mind that YOLO actually
            # returns the center (x, y)-coordinates of the bounding
            # box followed by the boxes' width and height
            box = detection[0:4] * np.array([W, H, W, H])
            (center_x, center_y, width, height) = box.astype("int")

            # use the center (x, y)-coordinates to derive the top and
            # and left corner of the bounding box
            x, y = self.calculate_left_top(center_x, center_y, width, height)

            # update our list of bounding box coordinates, confidences,
            # and class IDs
            self.boxes.append([x, y, int(width), int(height)])
            self.confidences.append(float(confidence))
            self.class_ids.append(class_id)

    def process_detections(self, detections):
        for detection in detections:
            self.process_detection(detection)

    def process_outputs(self, layer_outputs):
        self.reset_detection()
        for detections in layer_outputs:
            self.process_detections(detections)

    def draw_box(self, image_, box_index):
        # draw a bounding box rectangle and label on the image
        (x, y) = (self.boxes[box_index][0], self.boxes[box_index][1])
        (width, height) = (self.boxes[box_index][2], self.boxes[box_index][3])

        color = [int(c) for c in self.colors[self.class_ids[box_index]]]
        cv2.rectangle(image_, (x, y), (x + width, y + height), color, 2)
        text = "{}: {:.4f}".format(self.labels[self.class_ids[box_index]],
                                   self.confidences[box_index])
        cv2.putText(image_, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

    def draw_boxes(self, image_: np.array, indexes: np.array):
        # ensure at least one image_preprocessing exists
        if len(indexes) == 0:
            return

        # loop over the indexes we are keeping
        for i in indexes.flatten():
            # extract the bounding box coordinates
            self.draw_box(image_, i)

    def _get_detected_objects(self, indexes):
        if len(indexes) == 0:
            return []
        return [self.labels[self.class_ids[i]] for i in indexes.flatten()]

    def process_image(self, image_):
        self.image_shape = image_.shape[:2]
        layer_outputs = self.forward_net(image_)
        self.process_outputs(layer_outputs)

        indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences,
                                   self.min_confidence, self.threshold)
        detected_objects = self._get_detected_objects(indexes)
        self.draw_boxes(image_, indexes)

        return detected_objects

    def detect_birds(self, image_: np.array):
        detected_objects = self.process_image(image_)

        return 'bird' in detected_objects


if __name__ == '__main__':
    image_path = '/home/karol/Downloads/p1.jpg'

    detector = YOLODetector()
    print(image_path)
    image = cv2.imread(image_path)

    detected_objects_ = detector.process_image(image)
    print(detected_objects_)
    cv2.imshow('w', image)
    cv2.waitKey(0)
