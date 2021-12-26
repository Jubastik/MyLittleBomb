import pygame
from BobmModules import BobmModule


class NoneModule(BobmModule):
    """Пустой Модуль бомбы"""

    def init(self):
        return self
    
    def draw(self):
        pass
