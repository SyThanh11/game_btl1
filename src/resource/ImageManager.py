import pygame

class ImageManager:
    def __init__(self):
        self.menu = pygame.image.load('Assets/images/MENU_SCREEN.png')
        self.game_play_background = pygame.image.load('Assets/images/GAME_SCREEN.png')
        self.zombie = pygame.image.load("Assets/images/ZOMBIE.png")
        self.play_game_button = pygame.image.load('Assets/images/PLAYGAME.png')
        self.sword = pygame.image.load("Assets/images/SWORD.png")
        self.setting_icon = pygame.image.load("Assets/images/SETTING_ICON.png")
        self.game_over = pygame.image.load("Assets/images/GAME_OVER_SCREEN.png")
        self.volume_on = pygame.image.load("Assets/images/VOLUME_ON_ICON.png")
        self.volume_off = pygame.image.load("Assets/images/VOLUME_OFF_ICON.png")
