import pygame
import math
import random
import sys
from resource.ImageManager import ImageManager
from resource.SoundManager import SoundManager
from objects.Zombie import ZombieState, Zombie
from const.const import DELAY_BEFORE_REMOVAL, WHITE, SCREEN_WIDTH

class GamePlayScene:

    def __init__(self, display, game_state_manager):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager
        
        self.image = ImageManager()
        self.sounds = SoundManager()

        self.TIMER = 20  # game play duration
        self.timer_countdown = self.TIMER

        self.NUM_ROW = 3
        self.NUM_COL = 3

        self.setting_icon = pygame.transform.scale(
            self.image.setting_icon, (35, 37))
        self.setting_icon_rect = self.setting_icon.get_rect(center =(35, 35))

        self.cursor_img = self.image.sword
        self.cursor_img_rect = self.cursor_img.get_rect()

        self.font_main = pygame.font.SysFont('trashhand', 70)
        self.font_sub = pygame.font.SysFont('trashhand', 40)

        self.score_value = 0
        self.nb_of_click = 0

        self.zombies = []  # init a list to store current zombies on the screen

        self.ZOMBIE_LIFE_SPANS = 1 * 1000
        self.ZOMBIE_RADIUS = max(self.image.zombie.get_width(), self.image.zombie.get_height()) * 0.4
        self.GENERATE_ZOMBIE = pygame.USEREVENT + 1
        self.APPEAR_INTERVAL = 2 * 1000

        self.zombies_position = [(142, 125), (405, 125), (659, 125), (142, 372), (405, 372), (
            659, 372), (142, 620), (405, 620), (659, 620)]  # init a list to store position of zombie

        pygame.time.set_timer(self.GENERATE_ZOMBIE, self.APPEAR_INTERVAL)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def resetInitialState(self):
        self.timer_countdown = self.TIMER
        self.nb_of_click = 0
        self.score_value = 0

    def getScore(self):
        return self.score_value
    
    def getMissedClick(self):
        return self.nb_of_click - self.score_value

    def checkExist(self, pos):
        for zombie in self.zombies:
            if pos == (zombie.x, zombie.y):
                return True
        return False

    def generateNextEnemyPos(self):
        new_pos = ()  # init an empty tuple
        while True:
            # random a number from 0 to 8
            grid_index = random.randint(0, self.NUM_ROW * self.NUM_COL - 1)
            new_pos = self.zombies_position[grid_index]
            if not self.checkExist(new_pos):
                break
        # return position that able to generate new zombie and time
        return new_pos, pygame.time.get_ticks()

    def drawZombies(self):
        for zombie in self.zombies:
            zombie.draw()

    def checkCollision(self, clickX, clickY, enemyX, enemyY):
        zombie_rect = self.image.zombie.get_rect()
        enemy_center = (
            enemyX + zombie_rect.center[0] - 20, enemyY + zombie_rect.center[1] - 50)
        distance = math.sqrt(math.pow(
            enemy_center[0] - clickX, 2) + (math.pow(enemy_center[1] - clickY, 2)))
        return distance < self.ZOMBIE_RADIUS

    def checkZombiesCollision(self, click_pos):
        current_time = pygame.time.get_ticks()
        for zombie in self.zombies:
            if self.checkCollision(click_pos[0], click_pos[1], zombie.x, zombie.y) and zombie.state == ZombieState.GO_UP:
                self.score_value += 1
                zombie.change_state(ZombieState.IS_SLAMED)
                self.sounds.playLevelUp()
                zombie.draw()
                zombie.hit_time = current_time
            
    def removePreviousZombie(self):
        for zombie in self.zombies:
            current_time = pygame.time.get_ticks()
            if zombie.need_go_down():
                zombie.change_state(ZombieState.GO_DOWN)
                zombie.draw()
                zombie.go_down_time = current_time
            if current_time - zombie.go_down_time >= DELAY_BEFORE_REMOVAL and zombie.state == ZombieState.NONE:
                self.zombies.remove(zombie)
            if current_time - zombie.hit_time >= DELAY_BEFORE_REMOVAL and zombie.state == ZombieState.IS_SLAMED:
                self.zombies.remove(zombie)

    def displayMissedClicks(self):
        missed_clicks = self.font_sub.render(
            "M i s s e d :  " + str(self.nb_of_click - self.score_value), True, WHITE)
        text_rect = missed_clicks.get_rect(center=(120, 775))
        self.display.blit(missed_clicks, text_rect)

    def displayScore(self):
        score = self.font_sub.render(
            "S c o r e :  " + str(self.score_value), True, WHITE)
        text_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 775))
        self.display.blit(score, text_rect)

    def displayTime(self):
        time = self.font_sub.render(
            "T i m e :  " + str(self.timer_countdown), True, WHITE)
        text_rect = time.get_rect(center=(680, 775))
        self.display.blit(time, text_rect)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_pos = pygame.mouse.get_pos()
                    if self.setting_icon_rect.collidepoint(click_pos):
                        self.game_state_manager.setState('pause')
                    else:
                        self.nb_of_click += 1
                        self.checkZombiesCollision(click_pos)

            if event.type == self.GENERATE_ZOMBIE:
                self.removePreviousZombie()
                if len(self.zombies) < self.NUM_COL * self.NUM_ROW:
                    new_pos, time_of_birth = self.generateNextEnemyPos()
                    self.zombies.append(
                        Zombie(x=new_pos[0], y=new_pos[1], screen=self.display))

            if event.type == pygame.USEREVENT:
                self.timer_countdown -= 1
                if self.timer_countdown <= 0:
                    self.zombies.clear()
                    self.game_state_manager.setState('game_over')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game_state_manager.setState('pause')  

        self.display.blit(self.image.game_play_background, (0, 0))

        self.display.blit(self.setting_icon, self.setting_icon_rect)

        self.drawZombies()
        self.displayMissedClicks()
        self.displayScore()
        self.displayTime()

        # cursor customize
        pygame.mouse.set_visible(False)  # make cursor invisible
        self.cursor_img_rect.center = pygame.mouse.get_pos()
        self.display.blit(self.cursor_img, self.cursor_img_rect)