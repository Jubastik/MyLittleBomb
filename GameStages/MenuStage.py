import pygame
from GameStages.Stage import Stage


class MenuStage(Stage):
    """Меню игры"""

    def init(self):
        return self

    def draw(self, screen):
        screen.fill((0, 40, 0))