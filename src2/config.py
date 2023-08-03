# STORES AVAILABLE THEMES AND ASSETS SETTINGS

import pygame
import os

from sound import Sound
from theme import Theme
from constants import *

class Config:
    def __init__(self):
        self.themes = [] # stores available themes in a list
        self._add_themes()
        self.index = 0
        self.theme = self.themes[self.index]
        self.hover = self.theme.hover
        self.font = pygame.font.SysFont(FONT, 18)
        self.move_sound = Sound(os.path.join(self.theme.move_sound))
        self.capture_sound = Sound(os.path.join(self.theme.capture_sound))

    def change_theme(self):
        self.index += 1

        self.index %= len(self.themes)

        self.theme = self.themes[self.index]

    # stores all available themes
    def _add_themes(self):
        green = Theme(Green.LIGHT_TILE, Green.DARK_TILE,
                      Green.LIGHT_MOVE, Green.DARK_MOVE,
                      Green.LIGHT_VALID, Green.DARK_VALID,
                      Green.HOVER, 
                      Green.MOVE_SOUND_PATH, Green.CAPTURE_SOUND_PATH)
        brown = Theme(Brown.LIGHT_TILE, Brown.DARK_TILE,
                      Brown.LIGHT_MOVE, Brown.DARK_MOVE,
                      Brown.LIGHT_VALID, Brown.DARK_VALID,
                      Brown.HOVER, 
                      Brown.MOVE_SOUND_PATH, Brown.CAPTURE_SOUND_PATH)
        blue = Theme(Blue.LIGHT_TILE, Blue.DARK_TILE,
                      Blue.LIGHT_MOVE, Blue.DARK_MOVE,
                      Blue.LIGHT_VALID, Blue.DARK_VALID,
                      Blue.HOVER, 
                      Blue.MOVE_SOUND_PATH, Blue.CAPTURE_SOUND_PATH)
        gray = Theme(Gray.LIGHT_TILE, Gray.DARK_TILE,
                      Gray.LIGHT_MOVE, Gray.DARK_MOVE,
                      Gray.LIGHT_VALID, Gray.DARK_VALID,
                      Gray.HOVER, 
                      Gray.MOVE_SOUND_PATH, Gray.CAPTURE_SOUND_PATH)

        self.themes = [green, brown, blue, gray]