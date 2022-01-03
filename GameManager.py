import pygame
from pygame_gui import UIManager

from GameStages.EndStage import EndStage
from GameStages.GameStage import GameStage
from GameStages.InitStage import InitStage
from GameStages.LevelChooseStage import LevelChooseStage
from GameStages.MenuStage import MenuStage
from GameStages.SettingsStage import SettingsStage
from MusicManager import MusicManager


class GameManager:
    '''Осуществляет управление игрой'''

    def __init__(self, screen, fps, current_stage='init'):
        self.ui_manager = UIManager(screen.get_size(), "Resources/ui_theme.json")
        self.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])
        self.current_stage = current_stage
        self.screen = screen
        self.fps = fps
        self.stages = {
            'init': InitStage(self).init(),
            'menu': MenuStage(self).init(),
            'settings': SettingsStage(self).init(),
            'choose_lvl': LevelChooseStage(self).init(),
            'game': GameStage(self).init(),
            'result': EndStage(self).init(),
        }
        self.music_manager = MusicManager()
        self.music_manager.change_volume(-80)

    def change_stage(self, name):
        self.current_stage = name
        stage = self.stages[self.current_stage]
        stage.stage_launch()
        self.music_manager.start_music(name)

    def loop(self):
        self.run = True
        clock = pygame.time.Clock()
        while self.run:
            frame_time = clock.tick(self.fps)
            time_delta = min(frame_time / 1000.0, 0.1)
            stage = self.stages[self.current_stage]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                self.ui_manager.process_events(event)
                stage.process_event(event)
            stage.update()
            self.ui_manager.update(time_delta)
            stage.draw(self.screen)
            self.ui_manager.draw_ui(self.screen)
            self.update_fps(clock)
            pygame.display.flip()

    # ----------------------------------------------------------------------------------------------------------------------
    # Служебная часть

    def update_fps(self, clock):
        font = pygame.font.SysFont("Arial", 30)
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        self.screen.blit(fps_text, (10, 0))
