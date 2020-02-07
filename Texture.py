from st_func import *
from Settings import *

class Texture:
    def __init__(self):
        self.texture = []
        self.texture.append(load_image("data/tile/wall.png"))
        self.texture.append(load_image("data/tile/bad_wall.png"))
        self.texture.append(load_image("data/tile/vase.png"))
        self.texture.append(load_image("data/tile/window.png"))
        self.texture.append(load_image("data/tile/exit.png"))

        self.floor = (0, 0, 0)
        self.ceil = (0, 0, 0)

        self.horrors = []
        image = load_image("data/tile/scream1.png")
        image = pygame.transform.scale(image, (screen_width, screen_height))
        self.horrors.append(image)

        self.st_image = load_image("data/tile/prisoner.png")
        self.st_image = pygame.transform.scale(self.st_image, (screen_width, screen_height))

        self.nd_image = load_image("data/tile/prisoner.png")
        self.nd_image = pygame.transform.scale(self.nd_image, (screen_width, screen_height))