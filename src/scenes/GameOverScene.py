import pygame
import sys
from resource.ImageManager import ImageManager  
from const.const import DARK, GREY, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE

class GameOverScene:
    def __init__(self, display, game_state_manager, game_play):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager
        self.game_play = game_play

        self.image = ImageManager()

        self.font_main = pygame.font.SysFont('jollylodger', 70)
        self.font_sub = pygame.font.SysFont('jollylodger', 54)

        self.game_over_center = self.image.game_over.get_rect().center
        self.position = 0
        self.transition_speed = 10

        self.new_record = self.font_main.render(
            "N e w  r e c o r d", True, DARK)
        self.game_over = self.font_main.render("G a m e  O v e r", True, DARK)
        self.play_again = self.font_sub.render(
            "P l a y  A g a i n", True, GREY)
        self.menu = self.font_sub.render("M e n u", True, GREY)

    def resetInitialState(self):
        self.position = 0

    def run(self):
        pygame.mouse.set_visible(True)  # make cursor invisible
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if (mouse_pos[0] >= 240) and (mouse_pos[0] <= 560) and (mouse_pos[1] >= 550) and (mouse_pos[1] <= 610):
                        self.game_play.resetInitialState()
                        self.resetInitialState()
                        self.game_state_manager.setState('game_play')

                    if (mouse_pos[0] >= 345) and (mouse_pos[0] <= 465) and (mouse_pos[1] >= 620) and (mouse_pos[1] <= 670):
                        self.game_play.resetInitialState()
                        self.resetInitialState()
                        self.game_state_manager.setState('menu')

        self.display.blit(self.image.game_play_background, (0, 0))
        self.display.blit(self.image.game_over, (SCREEN_WIDTH // 2 -
                          self.game_over_center[0], (SCREEN_HEIGHT - self.game_over_center[1]) - self.position))

        # transition effect continue to increase position every time
        if (SCREEN_HEIGHT - self.game_over_center[1] - self.position) > ((SCREEN_HEIGHT // 2 - self.game_over_center[1]) + 50):
            self.position += self.transition_speed

        else:
            new_record_rect = self.new_record.get_rect(
                center=(SCREEN_WIDTH // 2, 280))
            self.display.blit(self.new_record, new_record_rect)

            self.score = self.font_sub.render(
                "S c o r e :  " + str(self.game_play.getScore()), True, DARK)
            score_rect = self.score.get_rect(center=(SCREEN_WIDTH // 2, 390))
            self.display.blit(self.score, score_rect)

            self.missed_clicks = self.font_sub.render(
                "M i s s e d :  " + str(self.game_play.getMissedClick()), True, DARK)
            missed_clicks_rect = self.missed_clicks.get_rect(center=(SCREEN_WIDTH // 2, 450))
            self.display.blit(self.missed_clicks, missed_clicks_rect)

            play_again_rect = self.play_again.get_rect(
                center=(SCREEN_WIDTH // 2, 580))
            self.display.blit(self.play_again, play_again_rect)

            menu_rect = self.menu.get_rect(center=(SCREEN_WIDTH // 2, 645))
            self.display.blit(self.menu, menu_rect)

            if (mouse_pos[0] >= 240) and (mouse_pos[0] <= 560) and (mouse_pos[1] >= 550) and (mouse_pos[1] <= 610):
                self.play_again = self.font_sub.render(
                    "P l a y  A g a i n", True, WHITE)
            else:
                self.play_again = self.font_sub.render(
                    "P l a y  A g a i n", True, GREY)

            if (mouse_pos[0] >= 345) and (mouse_pos[0] <= 465) and (mouse_pos[1] >= 620) and (mouse_pos[1] <= 670):
                self.menu = self.font_sub.render("M e n u", True, WHITE)
            else:
                self.menu = self.font_sub.render("M e n u", True, GREY)