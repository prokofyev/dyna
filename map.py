import pygame
import random

from constants import *
from player import Player
from controls import Controls
from utils import *

class Map:
    def __init__(self, game):
        self.game = game

        # Пример карты (0 - пусто, 1 - неразрушаемый блок, 2 - разрушаемый блок)
        self.game_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        breaking_walls = random.randint(10, 20)
        while breaking_walls > 0:
            r = random.randint(0, len(self.game_map) - 1)
            c = random.randint(0, len(self.game_map[0]) - 1)

            f = True
            for player in self.game.players:
                if get_grid_pos(player.x, player.y) == (c, r):
                    f = False

            if self.game_map[r][c] == 0 and f:
                self.game_map[r][c] = 2
                breaking_walls -= 1

    def draw_map(self, screen):
        for y in range(len(self.game_map)):
            for x in range(len(self.game_map[y])):
                if self.game_map[y][x] == 1:
                   screen.blit(self.game.texture_manager.textures["wall"], 
                            (x * GRID_SIZE, y * GRID_SIZE))
                elif self.game_map[y][x] == 2:
                    screen.blit(self.game.texture_manager.textures["wall2"], 
                            (x * GRID_SIZE, y * GRID_SIZE))
