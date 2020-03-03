from unittest import TestCase

import numpy as np

from master_controller.camera.generic_camera import GenericCamera


class TestGenericCamera(TestCase):
    def setUp(self) -> None:
        self.camera = GenericCamera()

    def test_init(self):
        # given

        # when

        # then
        self.assertIsNone(self.camera.image)
        self.assertFalse(self.camera._stop_camera)

    def test_stop(self):
        # given

        # when
        self.camera.stop()

        # then
        self.assertTrue(self.camera._stop_camera)

    def test_check_stop(self):
        self.assertEqual(self.camera.check_stop(), self.camera._stop_camera)

    def test_get_current_frame(self):
        # given
        im = np.ones((200, 300, 3), dtype=np.uint8)
        self.camera.image = im

        # when
        im_got = self.camera.get_current_frame()

        # then
        self.assertTrue(np.array_equal(im, im_got))
