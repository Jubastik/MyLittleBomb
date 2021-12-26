import pygame
from pygame_gui import UIManager

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
        self.ui_manager = UIManager(screen.get_size(), "Resources/ui_theme.json")
        self.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                  {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                  {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])
        self.current_stage = 'choose_lvl'
        self.screen = screen
        self.fps = fps
        self.stages = {
            'init': InitStage(self).init(),
            'menu': MenuStage(self).init(),
            'settings': SettingsStage(self).init(),
            'choose_lvl': LevelChooseStage(self).init(),
            'game': LevelStage(self).init(),
            'result': EndStage(self).init(),
        }

    def change_stage(self, name):
        self.current_stage = name

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            frame_time = clock.tick(self.fps)
            time_delta = min(frame_time / 1000.0, 0.1)
            stage = self.stages[self.current_stage]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        print(event.pos)
                self.ui_manager.process_events(event)
                stage.process_event(event)
            stage.update()
            self.ui_manager.update(time_delta)
            stage.draw(self.screen)
            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()
