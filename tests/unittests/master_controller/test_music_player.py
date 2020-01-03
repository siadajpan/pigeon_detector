from unittest import TestCase
from unittest.mock import patch

import settings
from master_controller.music_player import MusicPlayer


class TestMusicPlayer(TestCase):
    @patch('pygame.mixer')
    def setUp(self, mixer_mock) -> None:
        self.mixer = mixer_mock
        self.music_player = MusicPlayer()

    def test___init__(self):
        self.mixer.init.assert_called()
        self.mixer.music.load.assert_called_with(settings.MUSIC_PATH)
        self.mixer.music.set_volume.assert_called_with(1.0)

    def test_start(self):
        # given
        
        # when
        self.music_player.start()
        
        # then
        self.mixer.music.play.assert_called()

    def test_stop(self):
        # given

        # when
        self.music_player.stop()

        # then
        self.mixer.music.stop.assert_called()

