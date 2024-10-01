import pygame


class Text:
    def __init__(self, scene, content, font_style='arial', font_size=50, color='WHITE'):
        self.scene = scene
        self.__content = content
        self.__font = pygame.font.SysFont(font_style, font_size)
        self.__color = color
        self.__text = self.__font.render(self.__content, True, self.__color)
        self.__scale = (1, 1)
        self.__angle = 0
        self.__pos = (0, 0)
        self.__origin = (0, 0)
        self.__alpha = 255
        self.__is_active = True
        self.__depth = 0
        self.scene.add(self)

    def set_is_bold(self, status):
        self.__font.set_bold(status)
        self.__text = self.__font.render(self.__content, True, self.__color)

    def set_is_italic(self, status):
        self.__font.set_italic(status)
        self.__text = self.__font.render(self.__content, True, self.__color)

    def set_font(self, font_style, font_size=50):
        self.__font = pygame.font.SysFont(font_style, font_size)
        self.__text = self.__font.render(self.__content, True, self.__color)

    def set_color(self, color):
        self.__color = color
        self.__text = self.__font.render(self.__content, True, self.__color)

    def set_depth(self, depth):
        self.__depth = depth
        if self.scene:
            self.scene.sort_obj_lst()

    def get_depth(self):
        return self.__depth

    def attach_scene(self, scene):
        self.scene = scene

    def get_width(self):
        return self.__text.get_width()

    def get_height(self):
        return self.__text.get_height()

    def get_size(self):
        return tuple([self.get_width(), self.get_height()])

    def get_display_size(self):
        return tuple([self.get_display_width(), self.get_display_height()])

    def get_display_width(self):
        return self.get_width() * self.__scale[0]

    def get_display_height(self):
        return self.get_height() * self.__scale[1]

    def set_scale(self, scale_x, scale_y):
        self.__scale = (scale_x, scale_y)

    def set_angle(self, angle):
        self.__angle = angle

    def set_pos(self, x, y):
        self.__pos = (x, y)

    def get_pos(self):
        return self.__pos

    def set_origin(self, x, y):
        if x < 0:
            x = 0
        elif x > 1:
            x = 1

        if y < 0:
            y = 0
        elif y > 1:
            y = 1

        self.__origin = (x, y)

    def get_origin(self):
        return self.__origin

    def set_content(self, content):
        self.__content = content
        self.__text = self.__font.render(self.__content, True, self.__color)

    def set_alpha(self, alpha):
        if alpha < 0:
            alpha = 0
        elif alpha > 255:
            alpha = 255
        self.__alpha = alpha
        self.__text.set_alpha(self.__alpha)

    def get_alpha(self):
        return self.__alpha

    def set_active(self, status):
        self.__is_active = status

    def get_active(self):
        return self.__is_active

    def is_over(self, pointer_pos):
        topleft_pos = (self.__pos[0] - self.__origin[0] * self.get_display_width(),
                       self.__pos[1] - self.__origin[1] * self.get_display_height())
        if topleft_pos[0] < pointer_pos[0] < topleft_pos[0] + self.get_display_width():
            if topleft_pos[1] < pointer_pos[1] < topleft_pos[1] + self.get_display_height():
                return True
        return False

    def update(self, time_interval):
        pass

    def render(self):
        if self.scene:
            self.__text.set_alpha(self.__alpha)
            surface = pygame.Surface((self.get_width(), self.get_height()), pygame.SRCALPHA)
            surface.blit(self.__text, (0, 0))
            surface = pygame.transform.scale(surface, (self.__scale[0] * surface.get_width(),
                                                       self.__scale[1] * surface.get_height()))
            surface = pygame.transform.rotate(surface, self.__angle)
            self.scene.display.blit(surface,
                                    (self.__pos[0] - self.__origin[0] * self.get_display_width(),
                                     self.__pos[1] - self.__origin[1] * self.get_display_height()))
