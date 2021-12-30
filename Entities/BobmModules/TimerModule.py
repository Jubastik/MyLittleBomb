import pygame
from Entities.BobmModules import BobmModule
from CONSTANTS import FPS


class TimerModule(BobmModule):
    """Моудуль бомбы с таймером"""

    def init(self):
        return self
    
    def draw(self):
        pass

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            pass
    
    def click_LKM(self, x, y):
        pass