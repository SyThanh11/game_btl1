import pygame
import sys
from enum import Enum
from src.const.const import SCREEN_WIDTH, SCREEN_HEIGHT
from src.scenes.Scene import Scene


class MenuSceneState(Enum):
    HIDDEN = 0
    STANDING = 1
    DISAPPEARING = 2


class MenuScene (Scene):
    def __init__(self):
        super().__init__('menu')
        self.background = None
        self.logo = None

        self.play_button = None
        self.play_text = None

        self.quit_button = None
        self.quit_text = None

        self.pointer_pos = None

        self.disappearing_interval = 1000
        self.time_ratio = 1.0

        self.state = MenuSceneState.HIDDEN

    def create(self):
        self.manager.sound.stop("theme")
        self.manager.sound.play("theme")

        self.background = self.add_image("menu-background")
        self.logo = self.add_image("official-logo")
        self.logo.set_pos(50, 120)
        self.logo.set_scale(0.4, 0.4)

        self.play_button = self.add_image("button")
        self.play_text = self.add_text("PLAY")
        self.play_text.set_is_bold(True)

        self.quit_button = self.add_image("button")
        self.quit_text = self.add_text("QUIT")
        self.quit_text.set_is_bold(True)

        self.background.set_origin(0.5, 0.5)
        self.background.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.play_button.set_origin(0.5, 0.5)
        self.play_text.set_origin(0.5, 0.5)
        self.play_button.set_pos(200, SCREEN_HEIGHT // 2)
        self.play_text.set_pos(200, SCREEN_HEIGHT // 2)

        self.quit_button.set_origin(0.5, 0.5)
        self.quit_text.set_origin(0.5, 0.5)
        self.quit_button.set_pos(200, SCREEN_HEIGHT // 2 + 200)
        self.quit_text.set_pos(200, SCREEN_HEIGHT // 2 + 200)

        self.time_ratio = 1.0
        self.set_state(MenuSceneState.STANDING)

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
        if self.state == MenuSceneState.STANDING:
            self.pointer_pos = pygame.mouse.get_pos()

            if self.play_button.is_over(self.pointer_pos):
                self.play_button.set_texture(self.manager.image.get("button-over"))
                self.play_text.set_color("BLACK")
            else:
                self.play_button.set_texture(self.manager.image.get("button"))
                self.play_text.set_color("WHITE")

            if self.quit_button.is_over(self.pointer_pos):
                self.quit_button.set_texture(self.manager.image.get("button-over"))
                self.quit_text.set_color("BLACK")
            else:
                self.quit_button.set_texture(self.manager.image.get("button"))
                self.quit_text.set_color("WHITE")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.play_button.is_over(self.pointer_pos):
                            self.manager.sound.play("click")
                            self.set_state(MenuSceneState.DISAPPEARING)
                        elif self.quit_button.is_over(self.pointer_pos):
                            self.manager.sound.play("click")
                            pygame.quit()
                            sys.exit()
        elif self.state == MenuSceneState.DISAPPEARING:
            if self.proceed_time(time_interval, self.disappearing_interval):
                self.set_alpha(255 * self.time_ratio)
            else:
                self.manager.start("game-play")
