import pygame
import os
from enum import Enum

from const.const import ZOMBIE_HEIGHT, ZOMBIE_WIDTH, ZOMBIE_MAX_HEIGHT, DEFAULT_ALPHA, MAX_TIME_LAST

class ZombieState(Enum):
    GO_UP = 0
    IS_SLAMED = 1
    GO_DOWN = 2
    NONE = 3

class Zombie:
    def __init__(self, x, y, screen):
        self.state = ZombieState.GO_UP
        self.x = x
        self.y = y
        self.screen = screen
        self.y_rise = ZOMBIE_MAX_HEIGHT
        self.alpha = DEFAULT_ALPHA
        self.time_last = MAX_TIME_LAST
        self.hit_time = 0
        self.go_down_time = 0
        self.last_update_time = pygame.time.get_ticks()

    def change_state(self, new_state):  
        self.state = new_state
        if new_state == ZombieState.GO_DOWN:
            self.go_down_time = pygame.time.get_ticks()
        elif new_state == ZombieState.IS_SLAMED:
            self.hit_time = pygame.time.get_ticks()

    def draw(self):
        surface = pygame.Surface((ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
        zombie = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath('Zombie.py')), "Assets/images/ZOMBIE.png"
                                                if self.state != ZombieState.IS_SLAMED else "Assets/images/zombie_stun.png"))
        zombie = pygame.transform.scale(zombie, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
        zombie_sur = zombie.convert_alpha()
        zombie_sur.set_alpha(self.alpha)
        surface.fill((255, 255, 255))
        surface.set_colorkey((255, 255, 255))
        surface.blit(zombie_sur, (0, self.y_rise))
        if self.state == ZombieState.GO_UP:
            zombie_rect = zombie.get_rect()
            zombie_center = zombie_rect.center
            self.screen.blit(
                surface, (self.x - zombie_center[0], self.y - zombie_center[1]))
            self.go_up()
        if self.state == ZombieState.IS_SLAMED:
            zombie_rect = zombie.get_rect()
            zombie_center = zombie_rect.center
            self.screen.blit(
                surface, (self.x - zombie_center[0], self.y - zombie_center[1]))
            self.fade()
        if self.state == ZombieState.GO_DOWN:
            zombie_rect = zombie.get_rect()
            zombie_center = zombie_rect.center
            self.screen.blit(
                surface, (self.x - zombie_center[0], self.y - zombie_center[1]))
            self.go_down()

    def go_up(self):
        if self.y_rise == 0:
            return
        self.y_rise -= 10

    def fade(self):
        if self.alpha == 0:
            self.y_rise = ZOMBIE_MAX_HEIGHT
            self.state = ZombieState.NONE
            self.alpha = DEFAULT_ALPHA
            return
        self.alpha -= 51

    def need_go_down(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= MAX_TIME_LAST:
            self.last_update_time = current_time
            return True
        return False

    def go_down(self):
        if self.y_rise == ZOMBIE_MAX_HEIGHT:
            self.state = ZombieState.NONE
            return
        self.y_rise += 10

