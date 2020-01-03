from unittest import TestCase
from unittest.mock import MagicMock

from master_controller.detection_runners.server_detection_caller import \
    ServerDetectionCaller


class TestServerDetectionCaller(TestCase):
    def setUp(self) -> None:
        self.process_function = MagicMock()
        self.callback = MagicMock()
        self.caller = ServerDetectionCaller(self.process_function, [1],
                                            self.callback)

    def test_init(self):
        self.assertEqual(self.caller.process_image_function,
                         self.process_function)
        self.assertEqual(self.caller.arguments, [1])
        self.assertEqual(self.caller.callback, self.callback)
