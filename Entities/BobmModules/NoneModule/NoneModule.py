import pygame
from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image


class NoneModule(BobmModule):
    """Пустой Модуль бомбы"""

    def init(self):
        self.isdefused = True
        self.module_image = load_image(r"Bomb/none.png").convert()
        return self

    def draw(self, screen):
        screen.blit(self.module_image, (self.x, self.y))

    def LKM_down(self, x, y):
        pass
