import pygame

from src.objects.Image import Image
from src.objects.Text import Text


class Scene:
    def __init__(self, name):
        self.__name = name
        self.__obj_lst = []
        self.__is_paused = False
        self.__depth = 0
        self.__alpha = 0
        self.manager = None
        self.display = None
        self.film = None

    def fill(self, color):
        self.display.fill(color)

    def attach_manager(self, manager):
        self.manager = manager
        self.display = manager.display
        self.film = pygame.Surface(manager.get_screen_size())
        self.film.fill("BLACK")
        self.film.set_alpha(self.__alpha)

    def add(self, obj):
        obj.attach_scene(self)
        self.__obj_lst.append(obj)
        self.sort_obj_lst()

    def add_image(self, name, x=0, y=0):
        img = Image(self, self.manager.image.get(name))
        img.set_pos(x, y)
        return img

    def add_text(self, content, x=0, y=0, font_style="arial", font_size=50, color="WHITE"):
        text = Text(self, content, font_style, font_size, color)
        text.set_pos(x, y)
        return text

    def sort_obj_lst(self):
        self.__obj_lst.sort(key=lambda x: x.get_depth())

    def get_name(self):
        return self.__name

    def set_is_paused(self, status):
        self.__is_paused = status

    def is_paused(self):
        return self.__is_paused

    def set_depth(self, depth):
        self.__depth = depth
        self.manager.sort_scene_lst()

    def get_depth(self):
        return self.__depth

    def set_alpha(self, alpha):
        self.__alpha = 255 - alpha
        self.film.set_alpha(self.__alpha)

    def get_alpha(self):
        return self.__alpha

    def preload(self):
        pass

    def create(self):
        pass

    def preupdate(self, time_interval):
        for obj in self.__obj_lst:
            if obj.get_active():
                obj.update(time_interval)
        self.update(time_interval)

    def update(self, time_interval):
        pass

    def render(self):
        for obj in self.__obj_lst:
            if obj.get_active():
                obj.render()
        self.display.blit(self.film, (0, 0))

    def clear(self):
        self.__obj_lst.clear()
