import pygame

from constants import *
from utils import *

class Bomb:
    def __init__(self, x, y, range, game, player):
        self.x = x
        self.y = y
        self.range = range
        self.timer = 3 * FPS 
        self.explosion_timer = 0.5 * FPS
        self.exploded = False
        self.should_remove = False

        self.game = game
        self.player = player
    
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

        grid_x, grid_y = get_grid_pos(self.x, self.y)

        for dw in self.game.map.destructables:
            dw_grid_x, dw_grid_y = get_grid_pos(dw.x, dw.y)
            if dw_grid_x == grid_x and abs(dw_grid_y - grid_y) <= self.range or \
                dw_grid_y == grid_y and abs(dw_grid_x - grid_x) <= self.range:
                dw.destruct()

        for bomb in self.game.bombs:
            dw_grid_x, dw_grid_y = get_grid_pos(bomb.x, bomb.y)
            if dw_grid_x == grid_x and abs(dw_grid_y - grid_y) <= self.range or \
                dw_grid_y == grid_y and abs(dw_grid_x - grid_x) <= self.range:
                if not bomb.exploded:
                    bomb.explode()

        for player in self.game.players:
            dw_grid_x, dw_grid_y = get_grid_pos(player.x, player.y)
            if dw_grid_x == grid_x and abs(dw_grid_y - grid_y) <= self.range or \
                dw_grid_y == grid_y and abs(dw_grid_x - grid_x) <= self.range:
                if not player.dead:
                    player.dye()
    
    def draw(self, screen):
        if self.exploded:
            screen.blit(self.game.texture_manager.textures["explosion"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
        else:
            screen.blit(self.game.texture_manager.textures["bomb"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))