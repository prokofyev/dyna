import pygame
import random

from constants import *
from bomb import Bomb
from utils import *

class Player:
    def __init__(self, controls, game):
        self.speed = GRID_SIZE
        self.bomb_limit = 1
        self.bomb_range = 1
        self.dead = False
        self.score = 0
        self.x = 0
        self.y = 0

        self.controls = controls
        self.game = game
        self.texture, self.color = self.game.texture_manager.get_colored_texture("player", 160)

        self.move_cooldown = 200  # 200 мс (0.2 сек) между шагами
        self.last_move_time = 0
    
    def control(self, keys):
        if not self.dead:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time < self.move_cooldown:
                return

            if keys[self.controls.left]:
                self.move(-1, 0)
                self.last_move_time = current_time
            if keys[self.controls.right]:
                self.move(1, 0)
                self.last_move_time = current_time
            if keys[self.controls.up]:
                self.move(0, -1)
                self.last_move_time = current_time
            if keys[self.controls.down]:
                self.move(0, 1)
                self.last_move_time = current_time
            if keys[self.controls.bomb]:
                self.game.bombs.append(Bomb(self.x, self.y, self.bomb_range, self.game))
                self.last_move_time = current_time

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Проверка на выход за границы и столкновение с блоками
        if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
            grid_x, grid_y = get_grid_pos(new_x, new_y)

            f = True
            for bomb in self.game.bombs:
                if get_grid_pos(bomb.x, bomb.y) == (grid_x, grid_y):
                    f = False

            for dw in self.game.map.destructables:
                if get_grid_pos(dw.x, dw.y) == (grid_x, grid_y):
                    f = False

            if self.game.map.game_map[grid_y][grid_x] == 1:
                f = False

            if f:
                self.x, self.y = new_x, new_y

    
    def draw(self, screen):
        if self.dead:
            screen.blit(self.game.texture_manager.textures["tomb"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
        else:
            screen.blit(self.texture, 
                            (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))

    def dye(self):
        self.dead = True
        self.other_player().score += 1
        self.game.game_over()

    def other_player(self):
        return self.game.players[1] if self.game.players[0] == self else self.game.players[0]

    def teleport(self):
        f = True

        while f:
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            if self.game.map.game_map[y][x] == 0:
                f = False
            for dw in self.game.map.destructables:
                dw_grid_x, dw_grid_y = get_grid_pos(dw.x, dw.y)
                if dw_grid_x == x and dw_grid_y == y:
                    f = True
    
        self.x = x * GRID_SIZE
        self.y = y * GRID_SIZE
