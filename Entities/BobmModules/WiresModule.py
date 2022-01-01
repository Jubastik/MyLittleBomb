import pygame
from Entities.BobmModules.BobmModule import BobmModule


class WiresModule(BobmModule):
    """Моудуль бомбы с проводами"""

    def init(self):
        self.isdefused = False
        return self

    def draw(self, screen):
        pass

    def generate(self):
        pass

    def click_LKM(self, x, y):
        pass
