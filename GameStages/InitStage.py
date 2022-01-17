import pygame
from GameStages.Stage import Stage
from image_loader import load_image


class InitStage(Stage):
    """Загрузка игры"""

    def init(self):
        self.background = load_image('image_1.png')
        self.timer = 90 # Временно давайте секунду, по 100 раз запускаться не кайф (было 90)
        return self

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.gm.change_stage("menu")

    def process_event(self, event):
        pass