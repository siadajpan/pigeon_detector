from unittest import TestCase
from unittest.mock import MagicMock

import numpy as np

import settings
from detection.yolo_detector import YOLODetector


class TestYOLODetector(TestCase):
    def setUp(self) -> None:
        self.yolo = YOLODetector()

    def test_init(self):
        self.assertEqual(settings.YOLO_CONFIG_FOLDER, self.yolo.config_folder)
        self.assertLess(self.yolo.min_confidence, 1)
        self.assertGreater(self.yolo.min_confidence, 0)
        self.assertLess(self.yolo.threshold, 1)
        self.assertGreater(self.yolo.threshold, 0)
        self.assertEqual(0, len(self.yolo.boxes))
        self.assertEqual(0, len(self.yolo.confidences))
        self.assertEqual(0, len(self.yolo.class_ids))
        self.assertIsNone(self.yolo.image_shape)

    def test_reset_detection(self):
        # given
        self.yolo.boxes = 'some boxes'
        self.yolo.confidences = [2, 2]
        self.yolo.class_ids = [2, 3]

        # when
        self.yolo.reset_detection()

        # then
        self.assertEqual(0, len(self.yolo.boxes))
        self.assertEqual(0, len(self.yolo.confidences))
        self.assertEqual(0, len(self.yolo.class_ids))

    def test_init_labels(self):
        # given

        # when
        labels = self.yolo.init_labels()

        # then
        self.assertTrue('bird' in labels)

    def test_init_colors(self):
        # given

        # when
        colors = self.yolo.init_colors()

        # then
        self.assertEqual(len(self.yolo.labels), len(colors))

    def test_init_net_no_weights(self):
        # given
        self.yolo.config_folder = 'some_non_existing_path'

        # when

        # then
        with self.assertRaises(FileNotFoundError):
            self.yolo.init_net()

    def test_init_net(self):
        # given

        # when
        net = self.yolo.init_net()

        # then
        self.assertIsNotNone(net)

    def test_init_output_layer_names(self):
        # given

        # when
        layer_names = self.yolo.init_output_layer_names()

        # then
        self.assertEqual(['yolo_82', 'yolo_94', 'yolo_106'], layer_names)

    def test_forward_net(self):
        # given
        image_ = (np.random.rand(1000, 1200, 3) * 255).astype(np.uint8)
        self.yolo.net = MagicMock()
        self.yolo.net.setInput = MagicMock()
        self.yolo.net.forward = MagicMock(return_value=['detection'])

        # when
        detections = self.yolo.forward_net(image_)

        # then
        self.yolo.net.setInput.assert_called()
        self.yolo.net.forward.assert_called_with(self.yolo.layer_names)
        self.assertEqual('detection', detections[0])

    def test_calculate_left_top(self):
        # given
        center_x = 50
        center_y = 100
        width = 30
        height = 50

        # when
        x, y = self.yolo.calculate_left_top(center_x, center_y, width, height)

        # then
        self.assertEqual(35, x)
        self.assertEqual(75, y)

    def test_process_detection_low_confidence(self):
        # given
        self.yolo.image_shape = [120, 100]
        box = [0.1, 0.3, 0.2, 0.4]
        scores = [0.02, 0.02, 0.03]
        detection = [*box, 1, *scores]

        # when
        self.yolo.process_detection(detection)

        # then
        self.assertEqual(0, len(self.yolo.boxes))
        self.assertEqual(0, len(self.yolo.confidences))
        self.assertEqual(0, len(self.yolo.class_ids))

    def test_process_detection_high_confidence(self):
        # given
        self.yolo.image_shape = [120, 100]
        box = [0.1, 0.3, 0.2, 0.4]
        scores = [0.04, 0.9, 0.03]
        detection = [*box, 1, *scores]

        # when
        self.yolo.process_detection(detection)

        # then
        self.assertEqual([0, 12, 20, 48], self.yolo.boxes[0])
        self.assertEqual(0.9, self.yolo.confidences[0])
        self.assertEqual(1, self.yolo.class_ids[0])

    def test_process_detections(self):
        # given
        detections = [1]
        self.yolo.process_detection = MagicMock()

        # when
        self.yolo.process_detections(detections)

        # then
        self.yolo.process_detection.assert_called_with(1)

    def test_process_outputs(self):
        # given
        layer_outputs = [[1]]
        self.yolo.reset_detection = MagicMock()
        self.yolo.process_detections = MagicMock()

        # when
        self.yolo.process_outputs(layer_outputs)

        # then
        self.yolo.reset_detection.assert_called()
        self.yolo.process_detections.assert_called_with([1])

    def test_draw_boxes_no_indexes(self):
        # given
        image_ = ''
        self.yolo.draw_box = MagicMock()
        indexes = []

        # when
        self.yolo.draw_boxes(image_, indexes)

        # then
        self.yolo.draw_box.assert_not_called()

    def test_draw_boxes(self):
        # given
        image_ = ''
        self.yolo.draw_box = MagicMock()
        indexes = np.array([1])

        # when
        self.yolo.draw_boxes(image_, indexes)

        # then
        self.yolo.draw_box.assert_called_with(image_, 1)

    def test_get_detected_objects_empty(self):
        # given
        indexes = []

        # when
        labels = self.yolo._get_detected_objects(indexes)

        # then
        self.assertEqual([], labels)

    def test_get_detected_objects(self):
        # given
        indexes = np.array([1, 2])
        self.yolo.labels = ['person', 'cat', 'dog']
        self.yolo.class_ids = [0, 1, 2]

        # when
        labels = self.yolo._get_detected_objects(indexes)

        # then
        self.assertEqual(['cat', 'dog'], labels)

    def test_process_image(self):
        # given
        image_ = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        self.yolo.forward_net = MagicMock(return_value=[1])
        self.yolo.process_outputs = MagicMock()
        self.yolo._get_detected_objects = MagicMock(return_value=['cat'])
        self.yolo.draw_boxes = MagicMock()

        # when
        detected = self.yolo.process_image(image_)

        # then
        self.yolo.forward_net.assert_called_with(image_)
        self.yolo.process_outputs.assert_called_with([1])
        self.yolo._get_detected_objects.assert_called()
        self.assertEqual(['cat'], detected)

    def test_detect_birds_detected(self):
        # given
        image_ = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        self.yolo.process_image = MagicMock(return_value=['bird', 'person'])

        # when
        bird_detected = self.yolo.detect_birds(image_)

        # then
        self.yolo.process_image.assert_called_with(image_)
        self.assertTrue(bird_detected)

    def test_detect_birds_not_detected(self):
        # given
        image_ = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        self.yolo.process_image = MagicMock(return_value=['person'])

        # when
        bird_detected = self.yolo.detect_birds(image_)

        # then
        self.yolo.process_image.assert_called_with(image_)
        self.assertFalse(bird_detected)
