import pygame


class SoundManager:
    def __init__(self):
        self.sound_dic = {}
        self.volume_dic = {}
        self.is_off = False

    def load(self, name, path):
        self.volume_dic[name] = 1.0
        self.sound_dic[name] = pygame.mixer.Sound(path)

    def play(self, name):
        self.sound_dic[name].play()

    def stop(self, name):
        self.sound_dic[name].stop()

    def set_volume(self, name, volume):
        if not self.is_off:
            self.sound_dic[name].set_volume(volume)
        self.volume_dic[name] = volume

    def turn_off(self):
        self.is_off = True
        for name in self.sound_dic.keys():
            self.sound_dic[name].set_volume(0)

    def turn_on(self):
        self.is_off = False
        for name in self.sound_dic.keys():
            self.sound_dic[name].set_volume(self.volume_dic[name])
