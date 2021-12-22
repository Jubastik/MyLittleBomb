import pygame


class Stage:
    """Материнский класс стадии игры"""

    def __init__(self, gm):
        self.gm = gm

    def init(self):
        return self

    def process_event(self, event):
        pass

    def draw(self, screen):
        pass

    def update(self):
        pass
