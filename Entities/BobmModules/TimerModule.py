import pygame
from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image
from CONSTANTS import FPS


class TimerModule(BobmModule):
    """Моудуль бомбы с таймером"""

    def init(self):
        self.module_image = load_image(r"timer.png")
        return self
    
    def draw(self, screen):
        screen.blit(self.module_image, (self.x, self.y))

    def update(self):
        pass
    
    def click_LKM(self, x, y):
        pass