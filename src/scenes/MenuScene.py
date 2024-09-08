import pygame
import sys
from const.const import DARK, WHITE, ORANGE, RED
from resource.ImageManager import ImageManager

class MenuScene:
    def __init__(self, display, game_state_manager):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager
        
        self.image = ImageManager()

        self.font_main = pygame.font.SysFont('trashhand', 70)
        self.font_sub = pygame.font.SysFont('trashhand', 40)

        self.text_play = self.font_main.render("P L A Y", True, DARK)
        self.text_game = self.font_main.render("G A M E",  True, DARK)

        self.text_how = self.font_sub.render("H O W", True, WHITE)
        self.text_to_play = self.font_sub.render("T O  P L A Y", True, WHITE)

        self.text_quit = self.font_sub.render("Q U I T", True, DARK)
        self.text_high_score = self.font_sub.render(
            "H I G H  S C O R E", True, DARK)

    def run(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if (mouse_pos[0] >= 297) and (mouse_pos[0] <= 730) and (mouse_pos[1] >= 577) and (mouse_pos[1] <= 746):  # play game button
                        self.game_state_manager.setState('game_play')

                    if (mouse_pos[0] >= 31) and (mouse_pos[0] <= 118) and (mouse_pos[1] >= 464) and (mouse_pos[1] <= 500):  # exit button
                        pygame.quit()
                        sys.exit()

        self.display.blit(self.image.menu, (0, 0))

        self.display.blit(self.text_play, (438, 597))
        self.display.blit(self.text_game, (425, 660))

        self.display.blit(self.text_how, (155, 558))
        self.display.blit(self.text_to_play, (116, 608))

        self.display.blit(self.text_quit, (31, 467))
        self.display.blit(self.text_high_score, (580, 456))

        if (mouse_pos[0] >= 297) and (mouse_pos[0] <= 730) and (mouse_pos[1] >= 577) and (mouse_pos[1] <= 746):
            self.display.blit(self.image.play_game_button, (289, 564))

        if (mouse_pos[0] >= 129) and (mouse_pos[0] <= 268) and (mouse_pos[1] >= 562) and (mouse_pos[1] <= 644):
            self.text_how = self.font_sub.render("H O W", True, DARK)
            self.text_to_play = self.font_sub.render(
                "T O  P L A Y", True, DARK)

        else:
            self.text_how = self.font_sub.render("H O W", True, WHITE)
            self.text_to_play = self.font_sub.render(
                "T O  P L A Y", True, WHITE)

        if (mouse_pos[0] >= 31) and (mouse_pos[0] <= 118) and (mouse_pos[1] >= 464) and (mouse_pos[1] <= 500):
            self.text_quit = self.font_sub.render("Q U I T", True, RED)

        else:
            self.text_quit = self.font_sub.render("Q U I T", True, DARK)

        if (mouse_pos[0] >= 580) and (mouse_pos[0] <= 772) and (mouse_pos[1] >= 457) and (mouse_pos[1] <= 491):
            self.text_high_score = self.font_sub.render(
                "H I G H  S C O R E", True, ORANGE)

        else:
            self.text_high_score = self.font_sub.render(
                "H I G H  S C O R E", True, DARK)