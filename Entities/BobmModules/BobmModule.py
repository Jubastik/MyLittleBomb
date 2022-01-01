import pygame


class BobmModule:
    """Материнский класс модуля бомбы, так же является затычкой"""

    def __init__(self, bomb, cords):
        """cords - координаты модуля"""
        self.x, self.y, self.x2, self.y2 = cords
        self.isdefused = False
        self.bomb = bomb

    def draw(self, screen):
        pass

    def update(self):
        pass
