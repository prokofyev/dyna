import pygame
import sys

from constants import *
from map import Map
from player import Player
from textures import TextureManager
from controls import Controls
from state import GameState


class Game:
    def __init__(self):
        pygame.init()

        # Настройки окна
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dyna Blaster")

        self.texture_manager = TextureManager()

        self.players = [
            Player(
                Controls(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT),
                self
            ), 
            Player(Controls(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE),
                self
            )]
        self.reset()

    def reset(self):
        self.map = Map(self)
        self.bombs = []
        for player in self.players:
            player.dead = False
            player.teleport()
        self.state = GameState.PLAYING   
        self.game_over_timer = GAME_OVER_MESSAGE_DURATION

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"{self.players[0].score} - {self.players[1].score}", True, WHITE)
        score_pos = (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10)
        
        # Миниатюры игроков
        player1_icon = pygame.transform.scale(self.players[0].texture, (30, 30))
        player2_icon = pygame.transform.scale(self.players[1].texture, (30, 30))
        
        # Позиции иконок
        self.screen.blit(player1_icon, (score_pos[0] - 40, 10))
        self.screen.blit(player2_icon, (score_pos[0] + score_text.get_width() + 10, 10))
        
        # Текст счёта
        self.screen.blit(score_text, score_pos)
        
    def draw_game_over_screen(self):
        """Рисует экран окончания игры"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

    def update(self):
        if self.state == GameState.GAME_OVER:
            self.game_over_timer -= 1
            if self.game_over_timer <= 0:
                self.reset()
        
        self.map.update()

        for bomb in self.bombs:
            bomb.update()

        self.bombs = [bomb for bomb in self.bombs if not bomb.should_remove] 

    def game_over(self):
        self.state = GameState.GAME_OVER    

    def draw(self):
        # Отрисовка
        self.screen.fill(BLACK)
        self.map.draw_map(self.screen)
        for bomb in self.bombs:
            bomb.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
        self.draw_score()

        if self.state == GameState.GAME_OVER:
            self.draw_game_over_screen() 

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

            self.update()
            self.draw()
            
            # Обновление экрана
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 

