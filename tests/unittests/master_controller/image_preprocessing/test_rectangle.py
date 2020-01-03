from unittest import TestCase

from master_controller.image_preprocessing.rectangle import Rectangle


class TestRectangle(TestCase):
    def setUp(self) -> None:
        self.rect = Rectangle(1, 2, 5, 10)

    def check_init(self):
        self.assertEqual(self.rect.x, 1)
        self.assertEqual(self.rect.y, 2)
        self.assertEqual(self.rect.width, 5)
        self.assertEqual(self.rect.height, 10)

    def test_eq_diff(self):
        # given
        diff_rect = Rectangle(2, 2, 5, 10)
        # when

        # then
        self.assertNotEqual(self.rect, diff_rect)

    def test_eq_same(self):
        # given
        same_rect = Rectangle(1, 2, 5, 10)

        # when

        # then
        self.assertEqual(self.rect, same_rect)

    def test_get_data(self):
        # given
        rect = Rectangle(1, 2, 3, 4)

        # when
        rect2 = rect.data

        # then
        self.assertEqual(rect2, (1, 2, 3, 4))

    def test_set_none_data(self):
        # given
        rect = Rectangle(1, 2, 3, 4)

        # when
        rect.data = None

        # then
        self.assertEqual(rect.data, (0, 0, 0, 0))

    def test_set_data(self):
        # given
        rect = Rectangle(1, 2, 3, 4)

        # when
        rect.data = (4, 5, 6, 7)

        # then
        self.assertEqual(rect.data, (4, 5, 6, 7))

    def test_check_correct_data(self):
        # given

        # when

        # then
        with self.assertRaises(ValueError):
            Rectangle(-1, 3, 3, 3)

        with self.assertRaises(ValueError):
            Rectangle(4, -1, 3, 3)

        with self.assertRaises(ValueError):
            Rectangle(4, 5, -3, 3)

        with self.assertRaises(ValueError):
            Rectangle(4, 5, 3, -3)

    def test_x_end(self):
        # given

        # when

        # then
        self.assertEqual(self.rect.x_end, 6)

    def test_y_end(self):
        # given

        # when

        # then
        self.assertEqual(self.rect.y_end, 12)

    def test_ends(self):
        # given

        # when

        # then
        self.assertEqual(self.rect.ends, (6, 12))
