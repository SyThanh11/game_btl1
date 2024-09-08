import pygame
import sys
from resource.ImageManager import ImageManager
from resource.SoundManager import SoundManager
from const.const import SCREEN_HEIGHT, SCREEN_WIDTH, GREY, DARK, WHITE

class PauseScene:
    def __init__(self, display, game_state_manager, game_play):
        self.display = display
        self.game_state_manager = game_state_manager
        
        self.image = ImageManager()
        self.sound = SoundManager()

        self.game_play = game_play

        self.font_main = pygame.font.SysFont('jollylodger', 70)
        self.font_sub = pygame.font.SysFont('jollylodger', 54)

        self.game_over_center = self.image.game_over.get_rect().center
        self.position = 0
        self.transition_speed = 10

        self.pause_game = self.font_main.render("P a u s e  g a m e", True, DARK)
        self.pause_game_rect = self.pause_game.get_rect(
                center=(SCREEN_WIDTH // 2, 280))

        self.continue_game = self.font_sub.render("C o n t i n u e", True, DARK)
        self.continue_game_rect = self.continue_game.get_rect(center=(SCREEN_WIDTH // 2, 420))

        self.menu = self.font_sub.render("M e n u", True, GREY)
        self.menu_rect = self.menu.get_rect(center = (SCREEN_WIDTH // 2, 580))

        self.volume_icon = self.image.volume_on
        self.volume_icon_rect = self.volume_icon.get_rect(center = (SCREEN_WIDTH // 2, 645))

    def resetInitialState(self):
        self.position = 0

    def run(self):
        pygame.mouse.set_visible(True)  # make cursor invisible

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.resetInitialState()
                    self.game_state_manager.setState("game_play")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_pos[0] >= 290 and mouse_pos[0] <= 510 and mouse_pos[1] >= 395 and mouse_pos[1] <= 445:
                        self.game_state_manager.setState("game_play")

                    if mouse_pos[0] >= 340 and mouse_pos[0] <= 460 and mouse_pos[1] >= 555 and mouse_pos[1] <= 605:
                        self.game_play.resetInitialState()
                        self.game_state_manager.setState("menu")

                    if self.volume_icon_rect.collidepoint(mouse_pos):
                        if self.volume_icon == self.image.volume_on:
                            self.volume_icon = self.image.volume_off
                            self.sound.stopMainTrack()
                        else:
                            self.volume_icon = self.image.volume_on
                            self.sound.playMainTrack()

        self.display.blit(self.image.game_play_background, (0, 0))
        self.display.blit(self.image.game_over, (SCREEN_WIDTH // 2 -
                    self.game_over_center[0], (SCREEN_HEIGHT - self.game_over_center[1]) - self.position))

        if (SCREEN_HEIGHT - self.game_over_center[1] - self.position) > ((SCREEN_HEIGHT // 2 - self.game_over_center[1]) + 50):
            self.position += self.transition_speed
        
        else:
            self.display.blit(self.pause_game, self.pause_game_rect)
            self.display.blit(self.continue_game, self.continue_game_rect)
            self.display.blit(self.menu, self.menu_rect)
            self.display.blit(self.volume_icon, self.volume_icon_rect)

            if mouse_pos[0] >= 290 and mouse_pos[0] <= 510 and mouse_pos[1] >= 395 and mouse_pos[1] <= 445:
                self.continue_game = self.font_sub.render("C o n t i n u e", True, WHITE)
            else:
                self.continue_game = self.font_sub.render("C o n t i n u e", True, DARK)

            if mouse_pos[0] >= 340 and mouse_pos[0] <= 460 and mouse_pos[1] >= 555 and mouse_pos[1] <= 605:
                self.menu = self.font_sub.render("M e n u", True, WHITE)
            else: 
                self.menu = self.font_sub.render("M e n u", True, GREY)