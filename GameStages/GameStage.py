import pygame
from GameStages.Stage import Stage
from Levels.Level1 import Level1
from Entities.Bomb import Bomb 


class GameStage(Stage):
    """Уровень"""

    def init(self, level):
        self.bomb = Bomb(level)
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.bomb.draw()

    def process_event(self, event):
        pass

    def update(self):
        self.bomb.update()