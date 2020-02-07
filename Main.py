import pygame
import math
import sys
import time
from Texture import *
from Level import *
from Raycast import *
from st_func import *
from Music import *


class Game(Texture, Level, Raycast, Screen, Music):
    def __init__(self):
        Screen.__init__(self)
        Texture.__init__(self)
        Level.__init__(self)
        Raycast.__init__(self)
        Music.__init__(self)

        self.load_level("1.txt")

    def start_game(self):
        self.start_time = int(time.process_time())
        while True:
            self.screen.fill((0, 0, 0))
            self.update()
            self.start_raycast()
            self.show_time()
            self.fun()
            pygame.display.flip()
            # print(self.player_pos[0] >> 6, self.player_pos[1] >> 6)

    def start_screen(self):
        image = load_image("data/tile/prisoner.png")
        image = pygame.transform.scale(image, (screen_width, screen_height))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = myfont.render('Press backspace to start', False, (255, 255, 255))
        self.screen.blit(image, (0, 0))
        self.screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_BACKSPACE]:
                        self.st_music.play()
                        running = False

    def win_screen(self):
        pygame.mixer.music.load("data/music/win_music.ogg")
        pygame.mixer.music.play(-1)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = myfont.render('Press backspace to exit', False, (255, 255, 255))
        image = load_image("data/tile/you-win.png")
        image = pygame.transform.scale(image, (screen_width, screen_height))
        self.screen.blit(image, (0, 0))
        self.screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_BACKSPACE]:
                        terminate()

    def lose_screen(self):
        pygame.mixer.music.load("data/music/ded.ogg")
        pygame.mixer.music.play(-1)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = myfont.render('Press backspace to exit', False, (255, 255, 255))
        image = load_image("data/tile/ded.png")
        image = pygame.transform.scale(image, (screen_width, screen_height))
        self.screen.blit(image, (0, 0))
        self.screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_BACKSPACE]:
                        terminate()

    def show_time(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = myfont.render('Time left: ' + str(600 - int(time.perf_counter()) + self.start_time), False, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))
        if int(time.perf_counter()) - self.start_time > 600:
            self.lose_screen()


if __name__ == '__main__':
    pygame.init()
    g = Game()
    g.start_screen()
    g.start_game()
