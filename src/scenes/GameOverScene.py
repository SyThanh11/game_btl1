import pygame
import pytweening
import sys
from enum import Enum
from src.const.const import SCREEN_WIDTH, SCREEN_HEIGHT
from src.scenes.Scene import Scene


class GameOverSceneState(Enum):
    HIDDEN = 0
    APPEARING = 1
    STANDING = 2
    DISAPPEARING_MENU = 3
    DISAPPEARING_REPLAY = 4


class GameOverScene (Scene):
    def __init__(self):
        super().__init__('game-over')

        self.background = None
        self.title = None
        self.record = None
        self.result = None
        self.info_panel = None
        self.control_panel = None

        self.game_over_text = None
        self.record_text = None
        self.record_number = None
        self.result_text = None
        self.result_number = None

        self.menu_button = None
        self.replay_button = None

        self.pointer_pos = None

        self.appearing_interval = 600
        self.disappearing_interval = 800
        self.time_ratio = 1.0

        self.state = GameOverSceneState.HIDDEN

    def create(self):
        self.background = self.add_image("game-play-background")
        self.title = self.add_image("title")
        self.info_panel = self.add_image("info")
        self.control_panel = self.add_image("result")

        self.game_over_text = self.add_text("GAME OVER")
        self.game_over_text.set_is_bold(True)
        self.record_text = self.add_text("RECORD")
        self.record_text.set_is_bold(True)
        self.record_number = self.add_text(str(self.manager.get_variable("record")))
        self.record_number.set_is_bold(True)
        self.result_text = self.add_text("RESULT")
        self.result_text.set_is_bold(True)
        self.result_number = self.add_text(str(self.manager.get_variable("result")))
        self.result_number.set_is_bold(True)

        self.menu_button = self.add_image("menu-button")
        self.replay_button = self.add_image("replay-button")

        self.title.set_origin(0.5, 0.5)
        self.title.set_pos(SCREEN_WIDTH // 2, 60)

        self.game_over_text.set_origin(0.5, 0.5)
        self.game_over_text.set_pos(SCREEN_WIDTH // 2, 70)

        self.info_panel.set_origin(0.5, 0.5)
        self.info_panel.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.info_panel.set_depth(10)

        self.record_text.set_pos(200, 300)
        self.record_text.set_depth(11)
        self.record_number.set_color("YELLOW")
        self.record_number.set_pos(450, 300)
        self.record_number.set_depth(11)

        self.result_text.set_pos(200, 400)
        self.result_text.set_depth(11)
        self.result_number.set_color("YELLOW")
        self.result_number.set_pos(450, 400)
        self.result_number.set_depth(11)

        self.control_panel.set_origin(0.5, 0.5)
        self.control_panel.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 190)

        self.menu_button.set_origin(0.5, 0.5)
        self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 605)
        self.replay_button.set_origin(0.5, 0.5)
        self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 605)

        self.time_ratio = 1.0
        self.set_state(GameOverSceneState.APPEARING)

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
        if self.state == GameOverSceneState.APPEARING:
            if self.proceed_time(time_interval, self.appearing_interval):
                ratio = pytweening.easeOutBack(1 - self.time_ratio)
                self.title.set_pos(SCREEN_WIDTH // 2, 60 * ratio)
                self.game_over_text.set_pos(SCREEN_WIDTH // 2, 70 * ratio)
                self.info_panel.set_pos(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) * ratio)
                self.record_text.set_pos(200, 300 * ratio)
                self.record_number.set_pos(450, 300 * ratio)
                self.result_text.set_pos(200, 400 * ratio)
                self.result_number.set_pos(450, 400 * ratio)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2 + 190) * ratio)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 605 * ratio)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 605 * ratio)
            else:
                self.title.set_pos(SCREEN_WIDTH // 2, 60)
                self.game_over_text.set_pos(SCREEN_WIDTH // 2, 70)
                self.info_panel.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                self.record_text.set_pos(200, 300)
                self.record_number.set_pos(450, 300)
                self.result_text.set_pos(200, 400)
                self.result_number.set_pos(450, 400)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 190)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 605)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 605)
                self.set_state(GameOverSceneState.STANDING)
        elif self.state == GameOverSceneState.STANDING:
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
                            self.set_state(GameOverSceneState.DISAPPEARING_MENU)
                        elif self.replay_button.is_over(self.pointer_pos):
                            self.manager.sound.play("click")
                            self.set_state(GameOverSceneState.DISAPPEARING_REPLAY)
        elif self.state == GameOverSceneState.DISAPPEARING_MENU:
            if self.proceed_time(time_interval, self.disappearing_interval):
                self.set_alpha(255 * self.time_ratio)
                ratio = pytweening.easeInBack(self.time_ratio)
                self.title.set_pos(SCREEN_WIDTH // 2, 260 * ratio - 200)
                self.game_over_text.set_pos(SCREEN_WIDTH // 2, 270 * ratio - 200)
                self.info_panel.set_pos(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2 + 200) * ratio - 200)
                self.record_text.set_pos(200, 500 * ratio - 200)
                self.record_number.set_pos(450, 500 * ratio - 200)
                self.result_text.set_pos(200, 600 * ratio - 200)
                self.result_number.set_pos(450, 600 * ratio - 200)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2 + 390) * ratio - 200)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 805 * ratio - 200)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 805 * ratio - 200)
            else:
                self.title.set_pos(SCREEN_WIDTH // 2, -200)
                self.game_over_text.set_pos(SCREEN_WIDTH // 2, -200)
                self.info_panel.set_pos(SCREEN_WIDTH // 2, -200)
                self.record_text.set_pos(200, -200)
                self.record_number.set_pos(450, -200)
                self.result_text.set_pos(200, -200)
                self.result_number.set_pos(450, -200)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, -200)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, -200)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, -200)
                self.set_state(GameOverSceneState.HIDDEN)
                self.manager.start("menu")
        elif self.state == GameOverSceneState.DISAPPEARING_REPLAY:
            if self.proceed_time(time_interval, self.disappearing_interval):
                ratio = pytweening.easeInBack(self.time_ratio)
                self.title.set_pos(SCREEN_WIDTH // 2, 260 * ratio - 200)
                self.game_over_text.set_pos(SCREEN_WIDTH // 2, 270 * ratio - 200)
                self.info_panel.set_pos(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2 + 200) * ratio - 200)
                self.record_text.set_pos(200, 500 * ratio - 200)
                self.record_number.set_pos(450, 500 * ratio - 200)
                self.result_text.set_pos(200, 600 * ratio - 200)
                self.result_number.set_pos(450, 600 * ratio - 200)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2 + 390) * ratio - 200)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, 805 * ratio - 200)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, 805 * ratio - 200)
            else:
                self.title.set_pos(SCREEN_WIDTH // 2, -200)
                self.game_over_text.set_pos(SCREEN_WIDTH // 2, -200)
                self.info_panel.set_pos(SCREEN_WIDTH // 2, -200)
                self.record_text.set_pos(200, -200)
                self.record_number.set_pos(450, -200)
                self.result_text.set_pos(200, -200)
                self.result_number.set_pos(450, -200)
                self.control_panel.set_pos(SCREEN_WIDTH // 2, -200)
                self.menu_button.set_pos(SCREEN_WIDTH // 2 - 55, -200)
                self.replay_button.set_pos(SCREEN_WIDTH // 2 + 55, -200)
                self.set_state(GameOverSceneState.HIDDEN)
                self.manager.start("game-play")
