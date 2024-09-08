import pygame
from const.const import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT, FPS
from scenes.state import GameStateManager
from scenes.IntroScene import IntroScene
from scenes.MenuScene import MenuScene
from scenes.GamePlayScene import GamePlayScene
from scenes.PauseScene import PauseScene
from scenes.GameOverScene import GameOverScene

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TEXT)

        self.game_state_manager = GameStateManager('intro')
        
        self.intro = IntroScene(self.screen, self.game_state_manager)
        self.menu = MenuScene(self.screen, self.game_state_manager)
        self.game_play = GamePlayScene(self.screen, self.game_state_manager)
        self.pause = PauseScene(self.screen, self.game_state_manager, self.game_play)
        self.game_over = GameOverScene(self.screen, self.game_state_manager, self.game_play)
        
        self.states = {'intro': self.intro, 'menu': self.menu, 'game_play': self.game_play, 'pause': self.pause, 'game_over': self.game_over}
    
    def run(self):
        while True:
            self.states[self.game_state_manager.getState()].run()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()