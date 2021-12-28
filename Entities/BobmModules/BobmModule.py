import pygame


class BobmModule:
    """Материнский класс модуля бомбы, так же является затычкой"""

    def __init__(self, cords):
        '''crods - координаты модуля'''
        self.x, self.y, self.x2, self.y2 = cords
    
    def on_click(self, pos):
        pass
    
    def draw(self):
        pass

    def update(self):
        pass