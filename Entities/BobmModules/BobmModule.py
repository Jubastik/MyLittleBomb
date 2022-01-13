import pygame


class BobmModule:
    """Родительский класс модуля бомбы"""

    def __init__(self, bomb, cords):
        """cords - координаты модуля"""
        self.x, self.y, self.x2, self.y2 = cords
        self._cords = cords
        self.isdefused = False
        self.bomb = bomb

    def draw(self, screen):
        pass

    def update(self):
        pass

    def LKM_down(self, x, y):
        pass

    def LKM_up(self, x, y):
        pass
