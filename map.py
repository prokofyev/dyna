import pygame
import random

from constants import *
from destructable import DestructableWall
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

        self.destructables = []

        destructables_count = random.randint(10, 20)
        while destructables_count > 0:
            r = random.randint(0, len(self.game_map) - 1)
            c = random.randint(0, len(self.game_map[0]) - 1)

            f = True

            for dw in self.destructables:
                if get_grid_pos(dw.x, dw.y) == (c, r):
                    f = False

            if self.game_map[r][c] == 0 and f:
                self.destructables.append(DestructableWall(c * GRID_SIZE, r * GRID_SIZE, self.game))
                destructables_count -= 1

    def draw_map(self, screen):
        for y in range(len(self.game_map)):
            for x in range(len(self.game_map[y])):
                if self.game_map[y][x] == 1:
                   screen.blit(self.game.texture_manager.textures["wall"], 
                            (x * GRID_SIZE + MARGIN_SIZE, y * GRID_SIZE + TOP_MARGIN_SIZE))

        for dw in self.destructables:
            dw.draw(screen)

    def update(self):
        for dw in self.destructables:
            dw.update()

        self.destructables = [dw for dw in self.destructables if not dw.should_remove]  
