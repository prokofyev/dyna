import pygame

from constants import *
from utils import *

class DestructableWall:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.destruction_timer = 0.5 * FPS
        self.destructed = False
        self.should_remove = False

        self.game = game
    
    def update(self):
        if self.destructed:
            self.destruction_timer -= 1
            if self.destruction_timer <= 0:
                self.should_remove = True

    def destruct(self):
        self.destructed = True
    
    def draw(self, screen):
        if self.destructed:
            screen.blit(self.game.texture_manager.textures["explosion"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
        else:
            screen.blit(self.game.texture_manager.textures["wall2"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))