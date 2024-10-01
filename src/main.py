from controllers.Game import Game
from const.const import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.IntroScene import IntroScene
from scenes.MenuScene import MenuScene
from scenes.GamePlayScene import GamePlayScene
from scenes.PauseScene import PauseScene
from scenes.GameOverScene import GameOverScene

if __name__ == '__main__':
    game = Game(SCREEN_WIDTH,
                SCREEN_HEIGHT,
                [IntroScene, MenuScene, GamePlayScene, PauseScene, GameOverScene],
                FPS)
    game.run()
