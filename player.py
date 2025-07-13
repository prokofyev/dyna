import pygame
import random

from constants import *
from bomb import Bomb
from utils import *

class Player:
    def __init__(self, controls, game):
        self.score = 0
        self.x = 0
        self.y = 0
        self.target_x = 0  
        self.target_y = 0
        self.is_moving = False
        self.speed = PLAYER_SPEED

        self.controls = controls
        self.game = game
        self.texture, self.color = self.game.texture_manager.get_colored_texture("player", 120)

        self.move_cooldown = PLAYER_MOVE_COOLDOWN
        self.last_move_time = 0

        self.reset()

    def reset(self):
        self.bomb_limit = 1
        self.bomb_range = 2
        self.dead = False
        self.move_cooldown = PLAYER_MOVE_COOLDOWN

    def control(self, keys):
        if not self.dead and not self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time < self.move_cooldown:
                return

            moved = False

            if keys[self.controls.left]:
                moved = self.start_move(-1, 0)
            if keys[self.controls.right]:
                moved = self.start_move(1, 0)
            if keys[self.controls.up]:
                moved = self.start_move(0, -1)
            if keys[self.controls.down]:
                moved = self.start_move(0, 1)

            if moved:
                self.last_move_time = current_time

            if keys[self.controls.bomb]:
                f = True
                for b in self.game.bombs:
                    if b.x == self.x and b.y == self.y:
                        f = False

                c = sum([1 for bomb in self.game.bombs if bomb.player == self])
                if c < self.bomb_limit and f:
                    self.game.bombs.append(Bomb(self.x, self.y, self.bomb_range, self.game, self))
                    self.last_move_time = current_time

    def start_move(self, dx, dy):
        new_x = self.x + dx * GRID_SIZE
        new_y = self.y + dy * GRID_SIZE
        
        grid_x, grid_y = get_grid_pos(new_x, new_y)

        if not (0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT):
            return False

        for bomb in self.game.bombs:
            if get_grid_pos(bomb.x, bomb.y) == (grid_x, grid_y):
                return False

        for dw in self.game.map.destructables:
            if get_grid_pos(dw.x, dw.y) == (grid_x, grid_y):
                if not dw.show_boost:
                    return False

        if self.game.map.game_map[grid_y][grid_x] == 1:
            return False

        self.target_x, self.target_y = new_x, new_y
        self.is_moving = True
        return True

    def update(self):
        if self.is_moving:
            # Плавное перемещение к целевой позиции
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = max(abs(dx), abs(dy))
            
            if distance < self.speed:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False

                grid_x, grid_y = get_grid_pos(self.x, self.y)
                for dw in self.game.map.destructables:
                    if get_grid_pos(dw.x, dw.y) == (grid_x, grid_y):
                        if dw.show_boost:
                            if dw.kind == BoostKind.BOMB:
                                self.bomb_limit += 1
                            elif dw.kind == BoostKind.RANGE:
                                self.bomb_range += 1
                            elif dw.kind == BoostKind.SPEED:
                                self.move_cooldown -= 30

                            dw.should_remove = True
            else:
                self.x += dx * self.speed / distance
                self.y += dy * self.speed / distance
    
    def draw(self, screen):
        if self.dead:
            screen.blit(self.game.texture_manager.textures["tomb"], 
                                (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))
        else:
            screen.blit(self.texture, 
                            (self.x + MARGIN_SIZE, self.y + TOP_MARGIN_SIZE))

    def dye(self):
        self.dead = True
        self.is_moving = False
        self.other_player().score += 1
        self.game.game_over()

    def other_player(self):
        return self.game.players[1] if self.game.players[0] == self else self.game.players[0]

    def teleport(self):
        f = True

        while f:
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            if self.game.map.game_map[y][x] == 0:
                f = False
            for dw in self.game.map.destructables:
                dw_grid_x, dw_grid_y = get_grid_pos(dw.x, dw.y)
                if dw_grid_x == x and dw_grid_y == y:
                    f = True
    
        self.x = x * GRID_SIZE
        self.y = y * GRID_SIZE
        self.target_x = self.x
        self.target_y = self.y
