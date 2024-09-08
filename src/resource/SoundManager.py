import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.typingSound = pygame.mixer.Sound("Assets/sounds/typing.wav")
        self.mainTrack = pygame.mixer.Sound("Assets/sounds/themesong.wav")
        self.levelSound = pygame.mixer.Sound("Assets/sounds/point.wav")
        
    def playMainTrack(self):
        self.mainTrack.play(-1)
        
    def stopMainTrack(self):
        self.mainTrack.stop()
    
    def playTyping(self):
        self.typingSound.play()

    def stopTyping(self):
        self.typingSound.stop()

    def playLevelUp(self):
        self.levelSound.play()
        
    def stopLevelUp(self):
        self.levelSound.stop()