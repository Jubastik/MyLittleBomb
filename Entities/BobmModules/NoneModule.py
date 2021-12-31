import pygame
from Entities.BobmModules.BobmModule import BobmModule


class NoneModule(BobmModule):
    """Пустой Модуль бомбы"""

    def init(self):
        self.isdefused = True
        return self
    
    def draw(self, screen):
        pass

    def click_LKM(self, x, y):
        pass
