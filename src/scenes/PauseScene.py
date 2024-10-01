import pygame
import pytweening
import sys
from enum import Enum

from src.const.const import SCREEN_WIDTH
from src.scenes.Scene import Scene


class PauseSceneState(Enum):
    HIDDEN = 0
    APPEARING = 1
    STANDING = 2
    DISAPPEARING_MENU = 3
    DISAPPEARING_REPLAY = 4


class PauseScene (Scene):
    def __init__(self):
        super().__init__('pause')

        self.background = None
        self.ui_top = None
        self.title_panel = None
        self.volume_panel = None
        self.control_panel = None

        self.pause_text = None
        self.hitted_num_text = None

        self.menu_button = None
        self.replay_button = None
        self.volume_button = None

        self.pointer_pos = None

        self.appearing_interval = 600
        self.disappearing_interval = 600
        self.time_ratio = 1.0

        self.state = PauseSceneState.HIDDEN

    def create(self):
        self.background = self.add_image("game-play-background")
        self.ui_top = self.add_image("pause-ui-top")
        self.title_panel = self.add_image("title")
        self.volume_panel = self.add_image("result")
        self.control_panel = self.add_image("result")

        self.pause_text = self.add_text("PAUSE")
        self.pause_text.set_is_bold(True)
        self.hitted_num_text = self.add_text("HITTED NUMBER: " + str(self.manager.get_variable("result")),
                                             font_size=30,
                                             color="BLACK")
        self.hitted_num_text.set_is_bold(True)
        self.hitted_num_text.set_depth(100)

        self.menu_button = self.add_image("menu-button")
        self.replay_button = self.add_image("replay-button")

        self.title_panel.set_origin(0.5, 0.5)
        self.title_panel.set_pos(SCREEN_WIDTH // 2, 60)

        self.pause_text.set_origin(0.5, 0.5)
        self.pause_text.set_pos(SCREEN_WIDTH // 2, 70)
        self.hitted_num_text.set_origin(0.5, 0.5)
        self.hitted_num_text.set_pos(SCREEN_WIDTH // 2, 335)

        self.ui_top.set_origin(0.5, 0.5)
        self.ui_top.set_pos(SCREEN_WIDTH // 2, 230)
        self.ui_top.set_depth(11)

        self.volume_panel.set_origin(0.5, 0.5)
        self.volume_panel.set_pos(SCREEN_WIDTH // 2, 320)
        self.volume_panel.set_depth(10)

        self.control_panel.set_origin(0.5, 0.5)
        self.control_panel.set_pos(SCREEN_WIDTH // 2, 445)

        self.menu_button.set_origin(0.5, 0.5)
        self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 460)
        self.replay_button.set_origin(0.5, 0.5)
        self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 460)

        self.time_ratio = 1.0
        self.set_state(PauseSceneState.APPEARING)

    def set_state(self, state):
        self.state = state

    def proceed_time(self, time_interval, total_time):
        if self.time_ratio < (time_interval / total_time):
            self.time_ratio = 1.0
            return False
        else:
            self.time_ratio -= time_interval / total_time
            return True

    def update(self, time_interval):
        if self.state == PauseSceneState.APPEARING:
            if self.proceed_time(time_interval, self.appearing_interval):
                ratio = pytweening.easeOutBack(1 - self.time_ratio)
                self.title_panel.set_pos(SCREEN_WIDTH // 2, 60 * ratio)
                self.pause_text.set_pos(SCREEN_WIDTH // 2, 70 * ratio)
                self.hitted_num_text.set_pos(SCREEN_WIDTH // 2, 335 * ratio)
                self.ui_top.set_pos(SCREEN_WIDTH // 2, 230 * ratio)
                self.volume_panel.set_pos(SCREEN_WIDTH // 2, 320 * ratio)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, 445 * ratio)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 460 * ratio)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 460 * ratio)
            else:
                self.title_panel.set_pos(SCREEN_WIDTH // 2, 60)
                self.pause_text.set_pos(SCREEN_WIDTH // 2, 70)
                self.hitted_num_text.set_pos(SCREEN_WIDTH // 2, 335)
                self.ui_top.set_pos(SCREEN_WIDTH // 2, 230)
                self.volume_panel.set_pos(SCREEN_WIDTH // 2, 320)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, 445)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 460)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 460)
                self.set_state(PauseSceneState.STANDING)
        elif self.state == PauseSceneState.STANDING:
            pygame.mouse.set_visible(True)
            self.pointer_pos = pygame.mouse.get_pos()

            if self.menu_button.is_over(self.pointer_pos):
                self.menu_button.set_texture(self.manager.image.get("menu-button-over"))
            else:
                self.menu_button.set_texture(self.manager.image.get("menu-button"))

            if self.replay_button.is_over(self.pointer_pos):
                self.replay_button.set_texture(self.manager.image.get("replay-button-over"))
            else:
                self.replay_button.set_texture(self.manager.image.get("replay-button"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menu_button.is_over(self.pointer_pos):
                            self.manager.sound.play("click")
                            self.set_state(PauseSceneState.DISAPPEARING_MENU)
                        elif self.replay_button.is_over(self.pointer_pos):
                            self.manager.sound.play("click")
                            self.set_state(PauseSceneState.DISAPPEARING_REPLAY)
        elif self.state == PauseSceneState.DISAPPEARING_MENU:
            if self.proceed_time(time_interval, self.disappearing_interval):
                self.set_alpha(255 * self.time_ratio)
                ratio = pytweening.easeInBack(self.time_ratio)
                self.title_panel.set_pos(SCREEN_WIDTH // 2, 160 * ratio - 100)
                self.pause_text.set_pos(SCREEN_WIDTH // 2, 170 * ratio - 100)
                self.hitted_num_text.set_pos(SCREEN_WIDTH // 2, 435 * ratio - 100)
                self.ui_top.set_pos(SCREEN_WIDTH // 2, 330 * ratio - 100)
                self.volume_panel.set_pos(SCREEN_WIDTH // 2, 420 * ratio - 100)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, 545 * ratio - 100)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 560 * ratio - 100)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 560 * ratio - 100)
            else:
                self.title_panel.set_pos(SCREEN_WIDTH // 2, -100)
                self.pause_text.set_pos(SCREEN_WIDTH // 2, -100)
                self.hitted_num_text.set_pos(SCREEN_WIDTH // 2, -100)
                self.ui_top.set_pos(SCREEN_WIDTH // 2, -100)
                self.volume_panel.set_pos(SCREEN_WIDTH // 2, -100)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, -100)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, -100)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, -100)
                self.set_state(PauseSceneState.HIDDEN)
                self.manager.start("menu")
        elif self.state == PauseSceneState.DISAPPEARING_REPLAY:
            if self.proceed_time(time_interval, self.disappearing_interval):
                ratio = pytweening.easeInBack(self.time_ratio)
                self.title_panel.set_pos(SCREEN_WIDTH // 2, 160 * ratio - 100)
                self.pause_text.set_pos(SCREEN_WIDTH // 2, 170 * ratio - 100)
                self.hitted_num_text.set_pos(SCREEN_WIDTH // 2, 435 * ratio - 100)
                self.ui_top.set_pos(SCREEN_WIDTH // 2, 330 * ratio - 100)
                self.volume_panel.set_pos(SCREEN_WIDTH // 2, 420 * ratio - 100)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, 545 * ratio - 100)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 560 * ratio - 100)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 560 * ratio - 100)
            else:
                self.title_panel.set_pos(SCREEN_WIDTH // 2, -100)
                self.pause_text.set_pos(SCREEN_WIDTH // 2, -100)
                self.hitted_num_text.set_pos(SCREEN_WIDTH // 2, -100)
                self.ui_top.set_pos(SCREEN_WIDTH // 2, -100)
                self.volume_panel.set_pos(SCREEN_WIDTH // 2, -100)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, -100)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, -100)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, -100)
                self.set_state(PauseSceneState.HIDDEN)
                self.manager.stop("pause")
                self.manager.resume("game-play")
