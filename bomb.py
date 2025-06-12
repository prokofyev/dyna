import pygame

from constants import *
from utils import *

class Bomb:
    def __init__(self, x, y, range, game):
        self.x = x
        self.y = y
        self.range = range
        self.timer = 3 * FPS 
        self.explosion_timer = 0.5 * FPS
        self.exploded = False
        self.should_remove = False

        self.game = game
    
    def update(self):
        if not self.exploded:
            self.timer -= 1
            if self.timer <= 0:
                self.explode()
        else:
            self.explosion_timer -= 1
            if self.explosion_timer <= 0:
                self.should_remove = True

    def explode(self):
        self.exploded = True
        self.timer = 1 * FPS

        grid_x, grid_y = get_grid_pos(self.x, self.y)
        for i in range(-self.range, self.range + 1):
            if 0 <= grid_y + i < GRID_HEIGHT:
                if self.game.map.game_map[grid_y + i][grid_x] == 2:
                    self.game.map.game_map[grid_y + i][grid_x] = 0
            if 0 <= grid_x + i < GRID_WIDTH:
                if self.game.map.game_map[grid_y][grid_x + i] == 2:
                    self.game.map.game_map[grid_y][grid_x + i] = 0
        # Уничтожение блоков и нанесение урона игрокам/врагам
        # (нужно добавить логику взрыва)
    
    def draw(self, screen):
        if self.exploded:
            screen.blit(self.game.texture_manager.textures["explosion"], 
                                (self.x, self.y))
        else:
            screen.blit(self.game.texture_manager.textures["bomb"], 
                                (self.x, self.y))