import pygame
from CONSTANTS import *
from GameStages.SettingsStage import SettingsStage
from GameStages.MenuStage import MenuStage
from GameStages.LevelChooseStage import LevelChooseStage
from GameStages.LevelStage import LevelStage
from GameStages.InitStage import InitStage
from GameStages.EndStage import EndStage


class GameManager:
    '''Осуществляет управление игрой'''

    def __init__(self, screen, fps):
        self.stages = {
            'init': InitStage(self).init(),
            'menu': MenuStage(self).init(),
            'settings': SettingsStage(self).init(),
            'choose_lvl': LevelChooseStage(self).init(),
            'game': LevelStage(self).init(),
            'result': EndStage(self).init(),
        }
        self.current_stage = 'init'
        self.screen = screen
        self.fps = fps

    def change_stage(self, name):
        self.current_stage = name

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            stage = self.stages[self.current_stage]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                stage.process_event(event)
            stage.update()
            stage.draw(self.screen)
            pygame.display.flip()
            clock.tick(self.fps)
