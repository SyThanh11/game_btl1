import pygame
from src.controllers.ImageManager import ImageManager
from src.controllers.SoundManager import SoundManager


class Game:
    def __init__(self, screen_width, screen_height, scene_type_lst, fps=60):
        pygame.init()
        pygame.mixer.init()
        self.display = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps

        self.image = ImageManager()
        self.sound = SoundManager()

        self.engine_variable = dict()

        is_first = True
        self.scene_dic = {}
        self.active_scene_name_lst = []
        for scene_type in scene_type_lst:
            scene = scene_type()
            scene.attach_manager(self)
            scene.preload()
            self.scene_dic[scene.get_name()] = scene
            if is_first:
                self.active_scene_name_lst.append(scene.get_name())
                scene.create()
                is_first = False

    def get_screen_size(self):
        return tuple([self.screen_width, self.screen_height])

    def add_variable(self, name, value):
        self.engine_variable[name] = value

    def get_variable(self, name):
        return self.engine_variable[name]

    def set_variable(self, name, value):
        self.engine_variable[name] = value

    def sort_scene_lst(self):
        self.active_scene_name_lst.sort(key=lambda x: self.scene_dic[x].get_depth())

    def stop(self, name):
        if name in self.active_scene_name_lst:
            self.scene_dic[name].clear()
            self.active_scene_name_lst.remove(name)

    def start(self, name):
        if name in self.scene_dic.keys():
            for active_name in self.active_scene_name_lst:
                self.scene_dic[active_name].clear()
            self.active_scene_name_lst.clear()
            self.active_scene_name_lst.append(name)
            self.scene_dic[name].set_is_paused(False)
            self.scene_dic[name].create()
            self.scene_dic[name].set_alpha(255)

    def launch(self, name):
        if name in self.scene_dic.keys():
            if name not in self.active_scene_name_lst:
                self.active_scene_name_lst.append(name)
                self.scene_dic[name].create()
                self.scene_dic[name].set_alpha(255)
                self.sort_scene_lst()

    def pause(self, name):
        if name in self.active_scene_name_lst:
            self.scene_dic[name].set_is_paused(True)

    def resume(self, name):
        if name in self.active_scene_name_lst:
            self.scene_dic[name].set_is_paused(False)

    def run(self):
        clock = pygame.time.Clock()
        last_time = pygame.time.get_ticks()
        while True:
            current_time = pygame.time.get_ticks()
            for name in self.active_scene_name_lst:
                if not self.scene_dic[name].is_paused():
                    self.scene_dic[name].preupdate(current_time - last_time)
                self.scene_dic[name].render()
            pygame.display.update()
            clock.tick(self.fps)
            print(current_time - last_time)
            last_time = current_time
