import time
import pygame
import math
from Settings import *
from Level import *
from Texture import *
from st_func import *
from Screen import *


class Raycast:  # Level, Texture, Screen):
    def __init__(self):
        # Screen.__init__(self)
        # Level.__init__(self)
        # Texture.__init__(self)

        self.angle_increment = FOV / screen_width
        self.sin_val = []
        self.cos_val = []
        self.tan_val = []
        for angle in range(3840):
            if angle == 0:
                angle = 0.00001
            angle = math.radians(angle * self.angle_increment)
            self.sin_val.append(math.sin(angle))
            self.cos_val.append(math.cos(angle))
            self.tan_val.append(math.tan(angle))
        self.len_look = 3840
        self.ratio = self.len_look / 360
        self.view_angle = 90
        self.view_look = int(self.view_angle * self.ratio)
        self.plane_center = screen_height // 2
        self.to_plane_dist = int((screen_width / 2) / math.tan(math.radians(FOV / 2)))

        self.x_move = int(move_speed * self.cos_val[self.view_look])
        self.y_move = -int(move_speed * self.sin_val[self.view_look])

        self.walked = 0
        self.mouse_cord = (-100, -100)

    def start_raycast(self):
        ray_angle = self.view_angle + half_FOV
        ray_look = self.view_look + int(half_FOV * self.ratio)
        self.screen.fill(self.floor, rect=(0, 0, screen_width, screen_height / 2))
        self.screen.fill(self.ceil, rect=(0, screen_height / 2, screen_width, screen_height / 2))
        for x in range(0, screen_width, resolution):
            if ray_angle < 0:
                ray_angle += 360
            if ray_angle >= 360:
                ray_angle -= 360
            if ray_angle == 0:
                ray_angle = 0.00001
            if ray_look < 0:
                ray_look += self.len_look
            if ray_look >= self.len_look:
                ray_look -= self.len_look
            if 0 <= ray_angle <= 90:
                tx = 1
                ty = -1
            elif 91 <= ray_angle <= 180:
                tx = 1
                ty = 1
            elif 181 <= ray_angle <= 270:
                tx = -1
                ty = 1
            else:
                tx = -1
                ty = -1

            wall_hit = 0
            hor_wall_dist = ver_wall_dist = 10000
            hor_wall_id = ver_wall_id = 0
            if 0 <= ray_angle <= 180:
                y_side = -1
                signed_y = -1
            else:
                y_side = grid_height
                signed_y = 1
            if 90 <= ray_angle <= 270:
                x_side = -1
                signed_x = -1
            else:
                x_side = grid_width
                signed_x = 1
            tan_angle = self.tan_val[ray_look]
            y_step = ((self.player_pos[1] >> 6) << 6) + y_side
            x_step = (self.player_pos[0] + abs(self.player_pos[1] - y_step) / tan_angle * tx)
            ray_x = x_step
            ray_y = y_step
            ray_pos = [int(ray_y) >> 6, int(ray_x) >> 6]
            if 0 <= ray_pos[0] < self.y_limit and 0 <= ray_pos[1] < self.x_limit:
                if self.grid[ray_pos[0]][ray_pos[1]] > 0:
                    hor_wall_dist = abs(self.player_pos[1] - ray_y) / abs(self.sin_val[ray_look])
                    hor_wall_id = self.grid[ray_pos[0]][ray_pos[1]]
                    wall_hit = 1
                else:
                    x_step = grid_height / tan_angle * tx
                    y_step = grid_height * signed_y
                    while True:
                        ray_x += x_step
                        ray_y += y_step
                        ray_pos = [int(ray_y) >> 6, int(ray_x) >> 6]
                        if 0 <= ray_pos[0] < self.y_limit and 0 <= ray_pos[1] < self.x_limit:
                            if self.grid[ray_pos[0]][ray_pos[1]] > 0:
                                hor_wall_dist = abs(self.player_pos[1] - ray_y) / abs(self.sin_val[ray_look])
                                hor_wall_id = self.grid[ray_pos[0]][ray_pos[1]]
                                wall_hit = 1
                                break
                        else:
                            break
            hor_wall_pos = ray_x

            x_step = ((self.player_pos[0] >> 6) << 6) + x_side
            y_step = (self.player_pos[1] + abs(self.player_pos[0] - x_step) * tan_angle * ty)
            ray_x = x_step
            ray_y = y_step
            ray_pos = [int(ray_y) >> 6, int(ray_x) >> 6]
            if 0 <= ray_pos[0] < self.y_limit and 0 <= ray_pos[1] < self.x_limit:
                if self.grid[ray_pos[0]][ray_pos[1]] > 0:
                    ver_wall_dist = abs(self.player_pos[0] - ray_x) / abs(self.cos_val[ray_look])
                    ver_wall_id = self.grid[ray_pos[0]][ray_pos[1]]
                    wall_hit = 1
                else:
                    x_step = grid_width * signed_x
                    y_step = (grid_width * tan_angle * ty)
                    while True:
                        ray_x += x_step
                        ray_y += y_step
                        ray_pos = [int(ray_y) >> 6, int(ray_x) >> 6]
                        if 0 <= ray_pos[0] < self.y_limit and 0 <= ray_pos[1] < self.x_limit:
                            if self.grid[ray_pos[0]][ray_pos[1]] > 0:
                                ver_wall_dist = abs(self.player_pos[0] - ray_x) / abs(self.cos_val[ray_look])
                                ver_wall_id = self.grid[ray_pos[0]][ray_pos[1]]
                                wall_hit = 1
                                break
                        else:
                            break
            ver_wall_pos = ray_y

            if wall_hit:
                wall_id = 0
                wall_dist = 0
                wall_side = 0
                wall_pos = 0
                if hor_wall_dist <= ver_wall_dist:
                    wall_dist = hor_wall_dist
                    wall_id = hor_wall_id
                    wall_side = 1
                    wall_pos = int(hor_wall_pos)
                else:
                    wall_dist = ver_wall_dist
                    wall_id = ver_wall_id
                    wall_side = 2
                    wall_pos = int(ver_wall_pos)
                texture_pos = int(wall_pos % wall_width)
                if wall_side == 1 and y_side == grid_height:
                    texture_pos = int((wall_width - 0.1) - texture_pos)
                elif wall_side == 2 and x_side == 2:
                    texture_pos = int((wall_width - 0.1) - texture_pos)
                cos_beta = self.cos_val[int((self.view_angle - ray_angle) * self.ratio)]
                wall_dist *= cos_beta
                column = self.texture[wall_id - 1].subsurface(texture_pos, 0, 1, wall_height)
                slice_height = int(wall_height / wall_dist * self.to_plane_dist)
                column = pygame.transform.scale(column, (resolution, slice_height))
                slice_y = self.plane_center - (slice_height // 2)
                alpha = int(wall_dist * 0.25)
                if alpha > 255:
                    alpha = 255
                shadow = pygame.Surface((resolution, slice_height)).convert_alpha()
                shadow.fill((0, 0, 0, alpha))
                self.screen.blit(column, (x, slice_y))
                self.screen.blit(shadow, (x, slice_y))
            ray_angle -= self.angle_increment * resolution
            ray_look -= resolution

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            # if event.type == pygame.MOUSEMOTION:
            #     print("ss")
            #     x, y = pygame.mouse.get_rel()
            #     pygame.mouse.set_pos((screen_width // 2, screen_height // 2))
            #     if self.mouse_cord == (-100, -100) and False:
            #         self.mouse_cord = (x, y)
            #     else:
            #         if x > 0:
            #             self.view_angle -= rotation_speed
            #             if self.view_angle < 0:
            #                 self.view_angle += 360
            #             self.view_look = int(self.view_angle * self.ratio)
            #             self.x_move = int(move_speed * self.cos_val[self.view_look])
            #             self.y_move = -int(move_speed * self.sin_val[self.view_look])
            #         elif x < 0:
            #             self.view_angle += rotation_speed
            #             if self.view_angle >= 360:
            #                 self.view_angle -= 360
            #             self.view_look = int(self.view_angle * self.ratio)
            #             self.x_move = int(move_speed * self.cos_val[self.view_look])
            #             self.y_move = -int(move_speed * self.sin_val[self.view_look])
            #         self.mouse_cord = (x, y)

        self.walked = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.walked = 1
            self.player_pos[0] += self.x_move
            self.player_pos[1] += self.y_move
            if self.player_pos[0] < 0 or self.player_pos[0] > self.x_limit * grid_width:
                self.player_pos[0] -= self.x_move
                self.player_pos[1] -= self.y_move
            elif self.player_pos[1] < 0 or self.player_pos[1] > self.y_limit * grid_height:
                self.player_pos[0] -= self.x_move
                self.player_pos[1] -= self.y_move
            elif self.grid[int(self.player_pos[1]) >> 6][int(self.player_pos[0]) >> 6] > 0:
                self.player_pos[0] -= self.x_move
                self.player_pos[1] -= self.y_move

        if key[pygame.K_s]:
            self.walked = 1
            self.player_pos[0] -= self.x_move
            self.player_pos[1] -= self.y_move
            if self.player_pos[0] < 0 or self.player_pos[0] > self.x_limit * grid_width:
                self.player_pos[0] += self.x_move
                self.player_pos[1] += self.y_move
            elif self.player_pos[1] < 0 or self.player_pos[1] > self.y_limit * grid_height:
                self.player_pos[0] += self.x_move
                self.player_pos[1] += self.y_move
            elif self.grid[int(self.player_pos[1]) >> 6][int(self.player_pos[0]) >> 6] > 0:
                self.player_pos[0] += self.x_move
                self.player_pos[1] += self.y_move

        if self.walked:
            pass
            # self.walk_music.play()
        else:
            pass
            # self.walk_music.stop()

        if key[pygame.K_a]:
            self.view_angle += rotation_speed
            if self.view_angle >= 360:
                self.view_angle -= 360
            self.view_look = int(self.view_angle * self.ratio)
            self.x_move = int(move_speed * self.cos_val[self.view_look])
            self.y_move = -int(move_speed * self.sin_val[self.view_look])
        if key[pygame.K_d]:
            self.view_angle -= rotation_speed
            if self.view_angle < 0:
                self.view_angle += 360
            self.view_look = int(self.view_angle * self.ratio)
            self.x_move = int(move_speed * self.cos_val[self.view_look])
            self.y_move = -int(move_speed * self.sin_val[self.view_look])

        if key[pygame.K_e] and self.check_door():
            if self.next_map == "win":
                self.win_screen()

    def fun(self):
        if self.traps[self.player_pos[1] >> 6][self.player_pos[0] >> 6] == 0:
            return
        id = self.traps[self.player_pos[1] >> 6][self.player_pos[0] >> 6]
        self.traps[self.player_pos[1] >> 6][self.player_pos[0] >> 6] = 0
        # pygame.mixer.music.pause()
        self.screams[id - 1].play()
        self.screen.blit(self.horrors[id - 1], (0, 0))
        # pygame.display.flip()
        last = time.perf_counter()
        while time.perf_counter() - last <= 3:
            continue
        # pygame.mixer.music.unpause()

    def check_door(self):
        check_x = (self.player_pos[0] + self.x_move) >> 6
        check_y = (self.player_pos[1] + self.y_move) >> 6
        if 0 <= check_x < self.x_limit and 0 <= check_y < self.y_limit:
            if self.grid[check_y][check_x] == 5:
                return True
        return False
