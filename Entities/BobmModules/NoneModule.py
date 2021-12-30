import pygame
from BobmModules import BobmModule


class NoneModule(BobmModule):
    """Пустой Модуль бомбы"""

    def init(self):
        self.isdefused = True
        return self
    
    def draw(self):
        pass

    def click_LKM(self, x, y):
        pass
