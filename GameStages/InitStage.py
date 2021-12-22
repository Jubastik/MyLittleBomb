import pygame
from GameStages.Stage import Stage
from image_loader import  load_image
from CONSTANTS import WIDTH, HEIGHT

class InitStage(Stage):
    """Загрузка игры"""

    def init(self):
        self.background = load_image('ScreenSelector.bmp')
        self.timer = 90
        return self

    def draw(self, screen):
        screen.blit(self.background, (WIDTH // 4 - 35, HEIGHT // 4))

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.gm.change_stage("menu")
