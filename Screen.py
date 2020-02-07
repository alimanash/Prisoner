import pygame
from Settings import *


class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Prisoner")