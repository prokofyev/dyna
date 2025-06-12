import pygame
import sys

from constants import *
from map import Map
from player import Player
from textures import TextureManager
from controls import Controls
from bomb import Bomb


class Game:
    def __init__(self):
        pygame.init()

        # Настройки окна
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dyna Blaster")

        self.texture_manager = TextureManager()

        self.players = [Player(GRID_SIZE, GRID_SIZE,
            Controls(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE),
            self), Player((GRID_WIDTH - 2) * GRID_SIZE, (GRID_HEIGHT - 2) * GRID_SIZE,
            Controls(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE),
            self)]
        self.map = Map(self)
        self.bombs = []


    def run(self):
        # Игровой цикл
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            for player in self.players:
                player.control(keys)
            
            for bomb in self.bombs:
                bomb.update()

            self.bombs = [bomb for bomb in self.bombs if not bomb.should_remove]  

            # Отрисовка
            self.screen.fill(BLACK)
            self.map.draw_map(self.screen)
            for bomb in self.bombs:
                bomb.draw(self.screen)
            for player in self.players:
                player.draw(self.screen)
            
            # Обновление экрана
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 

