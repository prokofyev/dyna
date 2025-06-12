import pygame

from constants import *
from bomb import Bomb
from utils import *

class Player:
    def __init__(self, x, y, controls, game):
        self.x = x
        self.y = y
        self.speed = GRID_SIZE
        self.bomb_limit = 1
        self.bomb_range = 1

        self.map = map
        self.controls = controls
        self.game = game

        self.move_cooldown = 200  # 200 мс (0.2 сек) между шагами
        self.last_move_time = 0
    
    def control(self, keys):
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
            if self.game.map.game_map[grid_y][grid_x] == 0:
                self.x, self.y = new_x, new_y
    
    def draw(self, screen):
        screen.blit(self.game.texture_manager.textures["player"], 
                            (self.x, self.y))
