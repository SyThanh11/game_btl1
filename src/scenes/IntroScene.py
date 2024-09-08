import sys
import pygame
from const.const import CHAR_DELAY, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, TEXT

class IntroScene:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        
        # configurate time
        self.interval = 500 # time to display first letter
        self.char_delay = CHAR_DELAY # delay between characters
        self.current_time = pygame.time.get_ticks() # time now
        self.next_char_time = self.current_time + self.interval
        self.char_index = 0
        
        # fade out
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill(BLACK)
        self.fade_alpha = 0
        
        # font 
        self.font = pygame.font.SysFont('jollylodger', 50)
        
    def run(self):
        # Register Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if any(pygame.key.get_pressed()) or any(pygame.mouse.get_pressed()):
            self.game_state_manager.setState('menu') # Change New State 'MENU'
            
        # take time since the game run
        self.current_time = pygame.time.get_ticks()
        
        # character iterator
        if self.current_time >= self.next_char_time and self.char_index < len(TEXT):
            self.char_index += 1
            self.next_char_time = self.current_time + self.char_delay


        # output
        self.display.fill(BLACK)
        rendered_text = self.font.render(TEXT[:self.char_index], True, WHITE)
        text_rect = rendered_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.display.blit(rendered_text, text_rect)

        # fade to black ef
        if self.char_index >= len(TEXT):
            # increase opacity
            self.fade_alpha += 2
            self.fade_surface.set_alpha(self.fade_alpha)

            if self.fade_alpha > 255:
                self.game_state_manager.setState('menu')

            # output
            self.display.blit(self.fade_surface, (0, 0))
            