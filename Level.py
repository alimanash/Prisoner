from Settings import *
from st_func import *


class Level:
    def __init__(self):
        self.player_pos = [0, 0]
        self.grid = []
        self.traps = []
        self.next_map = ""
        self.x_limit = 0
        self.y_limit = 0

        # self.win_image = load_image("data/tile/win.png")

    def load_level(self, name):
        self.grid = []
        self.traps = []

        name = "data/map/" + name
        with open(name, "r") as file:
            line = str.split(file.readline().strip("\n"), " ")
            self.y_limit = int(line[0])
            self.x_limit = int(line[1])
            q = int(line[2])
            self.next_map = line[3]
            self.player_pos[0] = int(float(line[4]) * grid_width)
            self.player_pos[1] = int(float(line[5]) * grid_height)

            for i in range(self.y_limit):
                self.grid.append([])
                self.traps.append([])
                line = file.readline().strip("\n")
                for j in range(self.x_limit):
                    self.grid[i].append(int(line[j]))
                    self.traps[i].append(0)
            for i in range(q):
                line = str.split(file.readline().strip("\n"), ' ')
                self.traps[int(line[0]) - 1][int(line[1]) - 1] = int(line[2])

    def end_win(self):
        terminate()
