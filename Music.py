import pygame


class Music:
    def __init__(self):
        self.h_music = []

        self.next_level = pygame.mixer.Sound("data/music/next_level.ogg")
        pygame.mixer.music.load("data/music/fon.ogg")
        pygame.mixer.music.set_volume(0.1)
        self.walk_music = pygame.mixer.Sound("data/music/walk_sound.ogg")
        pygame.mixer.music.play(-1)

        self.screams = []
        self.screams.append(pygame.mixer.Sound("data/music/scream1.ogg"))

        self.st_music = pygame.mixer.Sound("data/music/zvuk-cepi.ogg")