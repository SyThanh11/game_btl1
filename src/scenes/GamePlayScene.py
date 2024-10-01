import pygame
import random
import sys
from src.objects.Zombie import ZombieState, Zombie
from src.scenes.Scene import Scene
from src.const.const import COUNT_DOWN, ZOMBIE_GENERATING_INTERVAL


class GamePlayScene (Scene):
    def __init__(self):
        super().__init__('game-play')
        self.image = None
        self.sounds = None
        self.timer_countdown = None
        self.countdown_event = None
        self.zombie_generating_event = None

        self.grid_topleft_pos = None
        self.grid_width = None
        self.grid_height = None

        self.grave_grid = None
        self.zombie_grid = None

        self.back_ground = None
        self.mallet = None
        self.setting_button_background = None
        self.setting_button = None

        self.info_panel = None
        self.hitted_num_text = None
        self.missed_num_text = None
        self.time_left_text = None

        self.grave_pos_lst = None

        self.total_hitted = 0

        self.pointer_pos = None

    def create(self):
        self.timer_countdown = COUNT_DOWN

        self.total_hitted = 0
        self.manager.set_variable("missed", 0)

        self.countdown_event = pygame.USEREVENT
        self.zombie_generating_event = pygame.USEREVENT + 1

        pygame.time.set_timer(self.zombie_generating_event, ZOMBIE_GENERATING_INTERVAL)
        pygame.time.set_timer(self.countdown_event, 1000)

        self.grid_topleft_pos = (270, 200)
        self.grid_width = 86
        self.grid_height = 100

        self.back_ground = self.add_image("game-play-background")

        self.grave_grid = []
        for i in range(5):
            grave_lst = []
            for j in range(9):
                grave = self.add_image("grave")
                grave.set_pos(self.grid_topleft_pos[0] + self.grid_width * j,
                              self.grid_topleft_pos[1] + self.grid_height * i)
                grave.set_active(False)
                self.add(grave)
                grave_lst.append(grave)
            self.grave_grid.append(grave_lst)

        self.zombie_grid = []
        for i in range(5):
            zombie_lst = []
            for j in range(9):
                zombie = Zombie(self)
                zombie.set_pos(self.grid_topleft_pos[0] + self.grid_width * j + 30,
                               self.grid_topleft_pos[1] + self.grid_height * i + 51)
                zombie.set_origin(0.5, 0.5)
                zombie.set_state(ZombieState.HIDDEN)
                self.add(zombie)
                zombie_lst.append(zombie)
            self.zombie_grid.append(zombie_lst)

        self.mallet = self.add_image("mallet")
        self.mallet.set_origin(0.5, 0.5)
        self.mallet.set_depth(200)
        self.add(self.mallet)

        self.setting_button_background = self.add_image("setting-button-background", 45, 45)
        self.setting_button = self.add_image("setting-button", 63, 64)

        self.info_panel = self.add_image("button-over", 720, 10)
        self.info_panel.set_scale(1.5, 1.3)
        self.hitted_num_text = self.add_text("HITTED NUMBER: " + str(self.total_hitted),
                                             745, 30,
                                             font_size=30,
                                             color="BLACK")
        self.hitted_num_text.set_is_bold(True)
        self.missed_num_text = self.add_text("MISSED NUMBER: " + str(self.manager.get_variable("missed")),
                                             745, 72,
                                             font_size=30,
                                             color="BLACK")
        self.missed_num_text.set_is_bold(True)
        self.time_left_text = self.add_text("TIME LEFT: " + str(self.timer_countdown),
                                            745, 114,
                                            font_size=30,
                                            color="RED")
        self.time_left_text.set_is_bold(True)

        pos_lst = []
        for i in range(45):
            pos_lst.append((i // 9, i % 9))
        random.shuffle(pos_lst)
        self.grave_pos_lst = pos_lst[:10]
        for pos in self.grave_pos_lst:
            self.grave_grid[pos[0]][pos[1]].set_active(True)

    def check_zombies_collision(self):
        for pos in self.grave_pos_lst:
            zombie = self.zombie_grid[pos[0]][pos[1]]
            if zombie.is_over(self.pointer_pos) and zombie.state == ZombieState.STANDING:
                zombie.set_state(ZombieState.SLAMED)
                self.total_hitted += 1
                self.manager.set_variable("result", self.total_hitted)
                self.manager.sound.play("point")

    def update(self, time_interval):
        self.pointer_pos = pygame.mouse.get_pos()
        self.hitted_num_text.set_content("HITTED NUMBER: " + str(self.total_hitted))
        self.missed_num_text.set_content("MISSED NUMBER: " + str(self.manager.get_variable("missed")))
        self.time_left_text.set_content("TIME LEFT: " + str(self.timer_countdown))

        if self.setting_button.is_over(self.pointer_pos):
            pygame.mouse.set_visible(True)
            self.mallet.set_active(False)
            self.setting_button.set_alpha(200)
        else:
            pygame.mouse.set_visible(False)
            self.mallet.set_active(True)
            self.mallet.set_pos(self.pointer_pos[0],
                                self.pointer_pos[1])
            self.setting_button.set_alpha(255)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mallet.set_texture(self.manager.image.get("mallet-smash"))
                if event.button == 1:
                    if self.setting_button.is_over(self.pointer_pos):
                        self.manager.sound.play("click")
                        self.manager.launch("pause")
                        self.manager.pause("game-play")
                    else:
                        self.check_zombies_collision()

            if event.type == pygame.MOUSEBUTTONUP:
                self.mallet.set_texture(self.manager.image.get("mallet"))

            if event.type == self.zombie_generating_event:
                random.shuffle(self.grave_pos_lst)
                for pos in self.grave_pos_lst:
                    if not self.zombie_grid[pos[0]][pos[1]].get_active():
                        self.zombie_grid[pos[0]][pos[1]].set_state(ZombieState.APPEARING)
                        break

            if event.type == self.countdown_event:
                self.timer_countdown -= 1
                if self.timer_countdown <= 0:
                    if self.total_hitted > self.manager.get_variable("record"):
                        self.manager.set_variable("record", self.total_hitted)
                    self.manager.start('game-over')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.manager.start('pause')
