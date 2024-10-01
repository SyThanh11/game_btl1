import pygame


class ImageManager:
    def __init__(self):
        self.image_dic = {}

    def load(self, name, path):
        self.image_dic[name] = pygame.image.load(path)

    def get(self, name):
        if name in self.image_dic.keys():
            return self.image_dic[name]
