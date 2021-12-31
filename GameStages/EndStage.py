import pygame
from GameStages.Stage import Stage


class EndStage(Stage):
    """Подсчёт результатов"""

    def init(self):
        return self
    
    def process_event(self, event):
        pass