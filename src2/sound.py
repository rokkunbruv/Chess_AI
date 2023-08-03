# LISTS ALL METHODS FOR SFX CONTROL

import pygame

class Sound:
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(self.path)

    # play sound from path provided by self.sound
    def play(self):
        pygame.mixer.Sound.play(self.sound)