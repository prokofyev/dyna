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

        for player in self.game.players:
            player_grid_x, player_grid_y = get_grid_pos(player.target_x, player.target_y)
            if player_grid_x == grid_x and player_grid_y == grid_y:
                if not player.dead:
                    player.dye()

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, self.range + 1):
                    check_x = grid_x + dx * i
                    check_y = grid_y + dy * i

                    if 0 <= check_x < GRID_WIDTH and 0 <= check_y < GRID_HEIGHT:
                        can_explode = True
                        should_stop = False
                        if self.game.map.game_map[check_y][check_x] == 1:
                            can_explode = False
                            should_stop = True
                        for dw in self.game.map.destructables:
                            dw_grid_x, dw_grid_y = get_grid_pos(dw.x, dw.y)
                            if dw_grid_x == check_x and dw_grid_y == check_y:
                                if not dw.show_boost:
                                    should_stop = True
                                dw.destruct()

                        if can_explode:
                            for bomb in self.game.bombs:
                                bomb_grid_x, bomb_grid_y = get_grid_pos(bomb.x, bomb.y)
                                if bomb_grid_x == check_x and bomb_grid_y == check_y:
                                    if not bomb.exploded:
                                        bomb.explode()
                            for player in self.game.players:
                                player_grid_x, player_grid_y = get_grid_pos(player.target_x, player.target_y)
                                if player_grid_x == check_x and player_grid_y == check_y:
                                    if not player.dead:
                                        player.dye()

                        if should_stop:
                            break
    
    def draw(self, screen):
        if self.exploded:
            # Отрисовываем центр взрыва
            screen.blit(self.game.texture_manager.textures["explosion"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
            
            # Отрисовываем все клетки в зоне поражения
            grid_x, grid_y = get_grid_pos(self.x, self.y)
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, self.range + 1):
                    check_x = grid_x + dx * i
                    check_y = grid_y + dy * i

                    if 0 <= check_x < GRID_WIDTH and 0 <= check_y < GRID_HEIGHT:
                        can_explode = True
                        should_stop = False
                        if self.game.map.game_map[check_y][check_x] == 1:
                            can_explode = False
                            should_stop = True
                        for dw in self.game.map.destructables:
                            dw_grid_x, dw_grid_y = get_grid_pos(dw.x, dw.y)
                            if dw_grid_x == check_x and dw_grid_y == check_y:
                                if not dw.show_boost:
                                    should_stop = True

                        if can_explode:
                            explosion_x = check_x * GRID_SIZE
                            explosion_y = check_y * GRID_SIZE
                            screen.blit(self.game.texture_manager.textures["explosion"],
                                    (explosion_x + MARGIN_SIZE, explosion_y + TOP_MARGIN_SIZE))
                        if should_stop:
                            break
        else:
            screen.blit(self.game.texture_manager.textures["bomb"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))