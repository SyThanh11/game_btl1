import pygame

class ImageManager:
    def __init__(self):
        self.menu = pygame.image.load('Assets/images/MENU_SCREEN.png').convert()
        self.game_play_background = pygame.image.load('Assets/images/GAME_SCREEN.png').convert()
        self.zombie = pygame.image.load("Assets/images/ZOMBIE.png").convert()
        self.play_game_button = pygame.image.load('Assets/images/PLAYGAME.png').convert_alpha()
        self.sword = pygame.image.load("Assets/images/SWORD.png").convert_alpha()
        self.setting_icon = pygame.image.load("Assets/images/SETTING_ICON.png").convert_alpha()
        self.game_over = pygame.image.load("Assets/images/GAME_OVER_SCREEN.png").convert_alpha()
        self.volume_on = pygame.image.load("Assets/images/VOLUME_ON_ICON.png").convert_alpha()
        self.volume_off = pygame.image.load("Assets/images/VOLUME_OFF_ICON.png").convert_alpha()
        
