import pygame
import re

class Circle(pygame.sprite.Sprite):
    def __init__(self, surface, center_position2: pygame.Vector2, radius: float=10, width: float=0, color: str="#212529"):
        self.__surface = surface
        self.__position = center_position2
        self.__radius = radius
        self.__width = width
        self.__color = color

    def update(self, dt):
        pygame.draw.circle(self.__surface, self.__color, self.position, self.radius, self.__width)
    
    def set_rect_border(self, __bordered_surface: pygame.Surface):
        pass

    @property
    def x(self):
        return self.__position.x
    @x.setter
    def x(self, __x_value: float):
        self.__position.x = __x_value

    @property
    def y(self):
        return self.__position.y
    @y.setter
    def y(self, __y_value: float):
        self.__position.y = __y_value
    
    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self, __coordinate: tuple[float]):
        self.__position.x, self.__position.y = __coordinate

    @property
    def radius(self):
        return self.__radius
    @radius.setter
    def radius(self, __r_value):
        if __r_value>=0:
            self.__radius = __r_value
        else:
            raise ValueError("Radius must be a non-negative number")
        
    def set_color(self, __color_code: str):
        if bool(re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", __color_code)):
            self.__color = __color_code
        else:
            raise ValueError("Incorrect color code")