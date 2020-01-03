import time
from unittest import TestCase
from unittest.mock import MagicMock

import cv2
import numpy as np
import requests

import settings
from master_controller.detection_runners.server_detection_caller import \
    ServerDetectionCaller
from master_controller.detection_runners.server_detection_runner import \
    ServerDetectionRunner


class TestServerDetectionRunner(TestCase):
    def setUp(self) -> None:
        self.runner = ServerDetectionRunner()

    def test_init(self):
        addr = settings.Server.DETECTION_ADDRESS
        self.assertEqual(addr + settings.Server.IMAGE_PROCESSING,
                         self.runner.send_pic_address)
        self.assertEqual(addr + settings.Server.CONNECTION_CHECK,
                         self.runner.connection_check)
        self.assertFalse(self.runner.connected)
        self.assertEqual(0., self.runner.last_connection_check)

    def test_process_image(self):
        # given
        self.runner.image = (np.array((100, 120, 3))).astype(np.uint8)
        process_image_function = requests.post
        _, image_encoded = cv2.imencode('.jpg', self.runner.image)
        arguments = [self.runner.send_pic_address, image_encoded.tostring()]

        self.runner.start_detection = MagicMock()

        # when
        self.runner.process_image()

        # then
        self.runner.start_detection.assert_called_with(process_image_function,
                                                       arguments)

    def test_update_detecion_result(self):
        # given
        detected = (True, True)

        # when
        self.runner.update_detection_result(detected)

        # then
        self.assertTrue(self.runner.connected)
        self.assertFalse(self.runner.processing)
        self.assertAlmostEqual(time.time(), self.runner.last_detection_time,
                               places=3)

    def test_init_detection_caller(self):
        # given

        # when
        self.runner.init_detection_caller(sum, [1, 2])

        # then
        self.assertIsInstance(self.runner.detection_caller,
                              ServerDetectionCaller)

    def test_last_connection_check_too_recent(self):
        # given
        self.runner.last_connection_check = time.time()

        # when
        too_recent = self.runner.last_connection_check_too_recent()

        # then
        self.assertTrue(too_recent)

    def test_last_connection_check_too_recent_not(self):
        # given
        self.runner.last_connection_check = time.time() - 1000

        # when
        too_recent = self.runner.last_connection_check_too_recent()

        # then
        self.assertFalse(too_recent)

    def test_check_connection(self):
        # given
        self.runner.connected = True

        # when
        connected = self.runner.check_connection()

        # then
        self.assertTrue(connected)

    def test_check_connection_too_recent(self):
        # given
        self.runner.connected = False
        self.runner.last_connection_check = time.time() - 1

        # when
        connected = self.runner.check_connection()

        # then
        self.assertFalse(connected)

    def test_check_connection_connected(self):
        # given
        self.runner.connection_check = 'http://google.com'

        # when
        connected = self.runner.check_connection()

        # then
        self.assertTrue(connected)

    def test_check_connection_not_connected(self):
        # given
        self.runner.connection_check = 'http://non_existing_address'

        # when
        connected = self.runner.check_connection()

        # then
        self.assertFalse(connected)









