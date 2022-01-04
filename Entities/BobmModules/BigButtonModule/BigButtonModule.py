import pygame
from Entities.BobmModules.BobmModule import BobmModule


class BigButtonModule(BobmModule):
    """Моудуль бомбы с большой кнопкой"""

    def init(self):
        self.isdefused = False
        return self

    def draw(self, screen):
        pass

    def generate(self):
        pass

    def LKM_down(self, x, y):
        pass

    def LKM_up(self, x, y):
        pass
