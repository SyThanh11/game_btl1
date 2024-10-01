import sys
import pygame
import pytweening
from enum import Enum
from src.const.const import SCREEN_WIDTH, SCREEN_HEIGHT
from src.scenes.Scene import Scene


class IntroSceneState(Enum):
    HIDDEN = 0
    APPEARING = 1
    STANDING = 2
    DISAPPEARING = 3


class IntroScene (Scene):
    def __init__(self):
        super().__init__("intro")

        self.logo = None
        self.nametag = None

        self.appearing_interval = 1000
        self.standing_interval = 1000
        self.disappearing_interval = 2000
        self.time_ratio = 1.0

        self.state = IntroSceneState.HIDDEN

    def preload(self):
        self.manager.image.load("official-logo", "../assets/images/official-logo.png")
        self.manager.image.load("logo", "../assets/images/logo.png")
        self.manager.image.load("nametag", "../assets/images/nametag.png")
        self.manager.image.load("menu-background", "../assets/images/menu.png")
        self.manager.image.load("game-play-background", "../assets/images/map.png")
        self.manager.image.load("grave", "../assets/images/grave.png")
        self.manager.image.load("zombie", "../assets/images/zombie-1.png")
        self.manager.image.load("slamed", "../assets/images/slamed.png")
        self.manager.image.load("mallet", "../assets/images/mallet-1.png")
        self.manager.image.load("mallet-smash", "../assets/images/mallet-2.png")
        self.manager.image.load("setting-button-background", "../assets/images/setting-button-background.png")
        self.manager.image.load("setting-button", "../assets/images/setting-button.png")
        self.manager.image.load("volume-on", "../assets/images/volume-button-on.png")
        self.manager.image.load("volume-off", "../assets/images/volume-button-off.png")
        self.manager.image.load("title", "../assets/images/title.png")
        self.manager.image.load("result", "../assets/images/result.png")
        self.manager.image.load("info", "../assets/images/info.png")
        self.manager.image.load("menu-button", "../assets/images/menu-button.png")
        self.manager.image.load("menu-button-over", "../assets/images/menu-button-over.png")
        self.manager.image.load("replay-button", "../assets/images/replay-button.png")
        self.manager.image.load("replay-button-over", "../assets/images/replay-button-over.png")
        self.manager.image.load("button", "../assets/images/button.png")
        self.manager.image.load("button-over", "../assets/images/button-over.png")
        self.manager.image.load("pause-ui-top", "../assets/images/pause-ui-top.png")

        self.manager.sound.load("typing", "../assets/sounds/typing.wav")
        self.manager.sound.load("theme", "../assets/sounds/theme.wav")
        self.manager.sound.load("point", "../assets/sounds/point.wav")
        self.manager.sound.load("click", "../assets/sounds/click.wav")
        self.manager.sound.load("slash", "../assets/sounds/slash.mp3")

    def create(self):
        self.logo = self.add_image("logo")
        self.logo.set_scale(0.4, 0.4)
        self.logo.set_origin(0.5, 0.5)
        self.logo.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.nametag = self.add_image("nametag")
        self.nametag.set_scale(0.8, 0.8)
        self.nametag.set_angle(5)
        self.nametag.set_origin(0.5, 0.5)
        self.nametag.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)
        self.nametag.set_active(False)

        self.time_ratio = 1.0
        self.set_state(IntroSceneState.APPEARING)

        self.manager.add_variable("missed", 0)
        self.manager.add_variable("record", 0)
        self.manager.add_variable("result", 0)

    def set_state(self, state):
        if state == IntroSceneState.STANDING:
            self.nametag.set_active(True)
            self.nametag.set_scale(3, 3)
            self.nametag.set_alpha(0)
        self.state = state

    def proceed_time(self, time_interval, total_time):
        if self.time_ratio < (time_interval / total_time):
            self.time_ratio = 1.0
            return False
        else:
            self.time_ratio -= time_interval / total_time
            return True
        
    def update(self, time_interval):
        self.fill("BLACK")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if any(pygame.key.get_pressed()) or any(pygame.mouse.get_pressed()):
            self.manager.sound.play("click")
            self.manager.start('menu')

        if self.state == IntroSceneState.APPEARING:
            if self.proceed_time(time_interval, self.appearing_interval):
                ratio = pytweening.easeOutBack(1 - self.time_ratio)
                self.logo.set_pos(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) * ratio)
            else:
                self.logo.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                self.set_state(IntroSceneState.STANDING)
        elif self.state == IntroSceneState.STANDING:
            if self.proceed_time(time_interval, self.standing_interval):
                ratio = pytweening.easeOutQuart(self.time_ratio)
                self.nametag.set_alpha(255 * (1 - ratio))
                self.nametag.set_scale(2.2 * ratio + 0.8, 2.2 * ratio + 0.8)
            else:
                self.manager.sound.play("slash")
                self.nametag.set_alpha(255)
                self.nametag.set_scale(0.8, 0.8)
                self.set_state(IntroSceneState.DISAPPEARING)
        elif self.state == IntroSceneState.DISAPPEARING:
            if self.proceed_time(time_interval, self.disappearing_interval):
                self.set_alpha(255 * self.time_ratio)
            else:
                self.set_state(IntroSceneState.HIDDEN)
                self.manager.start('menu')
