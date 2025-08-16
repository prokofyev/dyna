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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
        self.esc_pressed = False

    def reset(self):
        self.map = Map(self)
        self.bombs = []
        for player in self.players:
            player.reset()
            player.teleport()
        self.state = GameState.PLAYING   
        self.game_over_timer = GAME_OVER_MESSAGE_DURATION
        self.esc_pressed = False

    def draw_score(self):
        font = pygame.font.SysFont(None, FONT_SIZE)
        score_text = font.render(f"{self.players[0].score} - {self.players[1].score}", True, WHITE)
        score_pos = (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 25)
        
        # Миниатюры игроков
        player1_icon = pygame.transform.scale(self.players[0].texture, (SMALL_PLAYER_SIZE, SMALL_PLAYER_SIZE))
        player2_icon = pygame.transform.scale(self.players[1].texture, (SMALL_PLAYER_SIZE, SMALL_PLAYER_SIZE))
        
        # Позиции иконок
        self.screen.blit(player1_icon, (score_pos[0] - SMALL_PLAYER_SIZE - 10, 20))
        self.screen.blit(player2_icon, (score_pos[0] + score_text.get_width() + 10, 20))
        
        # Текст счёта
        self.screen.blit(score_text, score_pos)
        
    def draw_game_over_screen(self):
        """Рисует экран окончания игры"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

    def draw_pause_screen(self):
        """Рисует экран паузы"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, FONT_SIZE)
        line1 = font.render("Нажмите ПРОБЕЛ, чтобы завершить игру,", True, WHITE)
        line2 = font.render("или ESC, чтобы продолжить", True, WHITE)
        
        line1_pos = (SCREEN_WIDTH // 2 - line1.get_width() // 2, SCREEN_HEIGHT // 2 - 25)
        line2_pos = (SCREEN_WIDTH // 2 - line2.get_width() // 2, SCREEN_HEIGHT // 2 + 25)
        
        self.screen.blit(line1, line1_pos)
        self.screen.blit(line2, line2_pos)

    def update(self):
        if self.state == GameState.GAME_OVER:
            self.game_over_timer -= 1
            if self.game_over_timer <= 0:
                self.reset()
        
        if self.state == GameState.PLAYING:
            self.map.update()

            for player in self.players:
                player.update()

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
        elif self.state == GameState.PAUSED:
            self.draw_pause_screen() 

    def run(self):
        # Игровой цикл
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.PAUSED
                        elif self.state == GameState.PAUSED:
                            self.state = GameState.PLAYING
                    elif event.key == pygame.K_SPACE and self.state == GameState.PAUSED:
                        running = False

            keys = pygame.key.get_pressed()
            if self.state == GameState.PLAYING:
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

