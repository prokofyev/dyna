import pygame

from constants import *
from utils import *

class DestructableWall:
    def __init__(self, x, y, game, kind=None):
        self.x = x
        self.y = y
        self.kind = kind
        self.destruction_timer = 0.5 * FPS
        self.destructed = False
        self.show_boost = False
        self.boost_destruction_timer = 0.5 * FPS
        self.boost_destructed = False
        self.should_remove = False

        self.game = game
    
    def update(self):
        if self.boost_destructed:
            self.boost_destruction_timer -= 1
            if self.boost_destruction_timer <= 0:
                self.should_remove = True
        elif self.destructed:
            self.destruction_timer -= 1
            if self.destruction_timer <= 0:
                if self.kind:
                    self.show_boost = True
                else:
                    self.should_remove = True

    def destruct(self):
        if self.show_boost:
            self.boost_destructed = True
        else:
            self.destructed = True
    
    def draw(self, screen):
        if self.boost_destructed:
            screen.blit(self.game.texture_manager.textures["explosion"],
                        (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
        elif self.show_boost:
            if self.kind == BoostKind.BOMB:
                screen.blit(self.game.texture_manager.textures["boost_bomb"],
                                    (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
            elif self.kind == BoostKind.SPEED:
                screen.blit(self.game.texture_manager.textures["boost_speed"],
                                    (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
            elif self.kind == BoostKind.RANGE:
                screen.blit(self.game.texture_manager.textures["boost_range"],
                                    (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
        elif self.destructed:
            screen.blit(self.game.texture_manager.textures["explosion"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
        else:
            screen.blit(self.game.texture_manager.textures["destructable"],
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))