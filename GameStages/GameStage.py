import pygame
from GameStages.Stage import Stage
from Levels.Level1 import Level1
from Entities.Bomb import Bomb
from CONSTANTS import BOMB_X, BOMB_Y, BOMB_X2, BOMB_Y2


class GameStage(Stage):
    """Игровая стадия. Чтобы объект класса был готов к работе надо обязательно использовать метод 'set_level'"""

    def init(self):
        self.ispause = False
        self.bomb = None
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.draw_hud(screen)
        self.bomb.draw(screen)

    def process_event(self, event):
        if self.ispause:
            self.pause()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_click_LKM(event.pos)

    def on_click_LKM(self, pos):
        x, y = pos
        if BOMB_X <= x <= BOMB_X2 and BOMB_Y <= y <= BOMB_Y2:
            self.bomb.bomb_click_LKM(pos)

    def update(self):
        if self.pause:
            pass
        else:
            self.bomb.update()

    def draw_hud(self, screen):
        pass

    def draw_background(self, screen):
        pass

    def stage_launch(self):
        self.pause = False

    def set_level(self, level):
        self.bomb = Bomb(self, level)

    def pause(self):
        pass
