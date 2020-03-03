from unittest import TestCase
from unittest.mock import MagicMock, patch

from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner


class TestAbstractDetectionRunner(TestCase):
    def setUp(self) -> None:
        self.detection_runner = AbstractDetectionRunner()

    def test_init(self):
        self.assertIsNone(self.detection_runner.image)
        self.assertFalse(self.detection_runner.processing)
        self.assertEqual(0, self.detection_runner.last_detection_time)

    def test_update_image(self):
        # given
        image = 'image'

        # when
        self.detection_runner.update_image(image)

        # then
        self.assertEqual(image, self.detection_runner.image)

    def test_update_movement_boxes(self):
        # given
        boxes = [MagicMock()]

        # when
        self.detection_runner.update_movement_boxes(boxes)

        # then
        self.assertEqual(boxes, self.detection_runner.movement_boxes)

    @patch('time.time')
    def test_update_detection_result_True(self, time_mock):
        # given
        detection = MagicMock()
        time_mock.return_value = 'time'

        # when
        self.detection_runner.update_detection_result(detection)

        # then
        self.assertFalse(self.detection_runner.processing)
        self.assertEqual(detection, self.detection_runner.last_detections)
        self.assertEqual('time', self.detection_runner.last_detection_time)

    @patch('time.time')
    def test_update_detection_result_false(self, time_mock):
        # given
        detection = []
        time_mock.return_value = 'time'

        # when
        self.detection_runner.update_detection_result(detection)

        # then
        time_mock.assert_not_called()
        self.assertFalse(self.detection_runner.processing)
        self.assertEqual(0, self.detection_runner.last_detection_time)

    def test_send_image_image_none(self):
        # given
        self.detection_runner.image = None

        # then
        self.assertRaises(ValueError, self.detection_runner.send_image)

    def test_send_image_movement_boxes_none(self):
        # given
        self.detection_runner.image = MagicMock()
        self.detection_runner.movement_boxes = None

        # then
        self.assertRaises(ValueError, self.detection_runner.send_image)

    def test_send_image_processing(self):
        # given
        self.detection_runner.image = MagicMock()
        self.detection_runner.movement_boxes = MagicMock()
        self.detection_runner.processing = True

        # then
        self.assertRaises(RuntimeError, self.detection_runner.send_image)

    def test_send_image(self):
        # given
        self.detection_runner.image = MagicMock()
        self.detection_runner.movement_boxes = MagicMock()
        self.detection_runner.processing = False

        # when
        self.detection_runner.send_image()

        # then
        self.assertTrue(self.detection_runner.processing)
