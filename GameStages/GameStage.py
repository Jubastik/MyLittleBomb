import pygame
from GameStages.Stage import Stage
from Entities.Bomb import Bomb
from image_loader import load_image
from CONSTANTS import BOMB_X, BOMB_Y, BOMB_X2, BOMB_Y2, FPS


class GameStage(Stage):
    """Игровая стадия. Чтобы объект класса был готов к работе надо обязательно использовать метод 'set_level'"""

    def init(self):
        self.ispause = False
        self.bomb = None
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.draw_background(screen)
        self.draw_hud(screen)
        self.bomb.draw(screen)
        if self.ispause:
            pass

    def process_event(self, event):
        if self.ispause:
            self.pause()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_click_LKM(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.ispause = not self.ispause

    def on_click_LKM(self, pos):
        x, y = pos
        if BOMB_X <= x <= BOMB_X2 and BOMB_Y <= y <= BOMB_Y2:
            self.bomb.click_LKM(x, y)

    def update(self):
        self.time -= 1
        if self.time <= 0:
            self.gm.change_stage('result')
        if self.ispause:
            pass
        else:
            self.bomb.update()

    def draw_hud(self, screen):
        pass

    def draw_background(self, screen):
        screen.fill((0, 0, 0))

    def stage_launch(self):
        self.pause = False
        self.win = False
        self.lose = False
        self.mistakes = 0
        self.time = FPS * 300

    def set_level(self, level):
        print(level)
        # self.bomb = Bomb(self, level)

    def pause(self):
        pass
