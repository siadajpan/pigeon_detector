import time
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests

import settings
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
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

    @patch.object(AbstractDetectionRunner, 'update_detection_result')
    def test_update_detection_result_not_connected(self, update_mock):
        # given
        detected = (False, [MagicMock()])

        # when
        self.runner.update_detection_result(detected)

        # then
        self.assertFalse(self.runner.connected)
        update_mock.assert_not_called()

    @patch.object(AbstractDetectionRunner, 'update_detection_result')
    def test_update_detection_result(self, update_mock):
        # given
        detected = (True, [MagicMock()])

        # when
        self.runner.update_detection_result(detected)

        # then
        update_mock.assert_called()

    def test_init_detection_caller(self):
        # given

        # when
        result = self.runner._init_detection_caller([1, 2])

        # then
        self.assertIsInstance(result, ServerDetectionCaller)

    @patch('cv2.imencode')
    @patch.object(AbstractDetectionRunner, 'send_image')
    def test_send_image(self, send_mock, encode_mock):
        # given
        caller = MagicMock()
        self.runner._init_detection_caller = MagicMock(return_value=caller)
        image = MagicMock()
        encode_mock.return_value = ('', image)

        # when
        self.runner.send_image()

        # then
        send_mock.acssert_called()
        encode_mock.assert_called()
        image.tostring.assert_called()
        self.runner._init_detection_caller.assert_called()
        caller.start.assert_called()

    def test_last_connection_check_too_recent(self):
        # given
        self.runner.last_connection_check = time.time()

        # when
        too_recent = self.runner._last_connection_check_too_recent()

        # then
        self.assertTrue(too_recent)

    def test_last_connection_check_too_recent_not(self):
        # given
        self.runner.last_connection_check = time.time() - 1000

        # when
        too_recent = self.runner._last_connection_check_too_recent()

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

    @patch('requests.get')
    def test_check_connection_connected(self, get_mock):
        # given

        # when
        connected = self.runner.check_connection()

        # then
        get_mock.assert_called()
        self.assertTrue(connected)

    @patch('requests.get')
    def test_check_connection_not_connected(self, get_mock):
        # given
        get_mock.side_effect = requests.exceptions.ConnectionError

        # when
        connected = self.runner.check_connection()

        # then
        self.assertFalse(self.runner.connected)
        self.assertFalse(connected)

    @patch('requests.get')
    def test_check_connection_timeout(self, get_mock):
        # given
        get_mock.side_effect = requests.exceptions.Timeout

        # when
        connected = self.runner.check_connection()

        # then
        self.assertFalse(self.runner.connected)
        self.assertFalse(connected)
