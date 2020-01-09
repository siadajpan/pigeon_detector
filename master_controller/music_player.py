from settings import MUSIC_PATH
import pygame
    

class MusicPlayer:
    def __init__(self):
        self._mixer = pygame.mixer
        self._mixer.init()
        self._mixer.music.load(MUSIC_PATH)
        self._mixer.music.set_volume(1.0)
        
    def start(self):
        self._mixer.music.play()
    
    def stop(self):
        self._mixer.music.stop()
