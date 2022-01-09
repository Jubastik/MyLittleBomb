import pygame
from GameStages.Stage import Stage
from Entities.Bomb import Bomb
from Entities.BobmModules.NoneModule.NoneModule import NoneModule
from image_loader import load_image
from CONSTANTS import BOMB_X, BOMB_Y, BOMB_X2, BOMB_Y2, FPS


# Порядок переключения на другой уровень:
# 1. Создаём объект бомбы
# 2. Создаём объект уровня
# 3. Передаём в бомбу объект уровня используя метод Bomb.load_level(level)
# 4. Передаём бомбу в GameStage исползуя метод GameStage.set_bomb(bomb)
# 5. Производим лаунч GameStage используя метод GameStage.stage_launch()
# 6. Меняем текущий стейдж игры в GameManager используя метод GameManager.change_stage()
class GameStage(Stage):
    """Игровая стадия.
    Перед использованием класс обязательно передаём объект бомбы в self.set_bomb"""

    def init(self):
        return self

    def stage_launch(self):
        self.ispause = False
        self.mistakes = 0

    def set_bomb(self, bomb):
        self.bomb = bomb

    # ------------------------------------------------------------------------------------------------------------------
    def update(self):
        self.time -= 1
        # Проверка на поражение по времени
        if self.time <= 0:
            self.lose()
        # Паузы наверное не будет, пока что просто существует.
        if self.ispause:
            pass
        else:
            self.bomb.update()

    def process_event(self, event):
        if self.ispause:
            self.pause()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.LKM_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.LKM_up(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.ispause = not self.ispause

    def LKM_down(self, pos):
        # Проверка места нажатия, если кликнули на бомбу, обработка будет продолжена в бомбе
        x, y = pos
        if BOMB_X <= x <= BOMB_X2 and BOMB_Y <= y <= BOMB_Y2:
            self.bomb.LKM_down(x, y)

    def LKM_up(self, pos):
        x, y = pos
        self.bomb.LKM_up(x, y)

    # ------------------------------------------------------------------------------------------------------------------

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.draw_background(screen)
        self.draw_hud(screen)
        self.bomb.draw(screen)
        if self.ispause:
            pass

    def draw_hud(self, screen):
        # Возможно не нужно, пока что просто существует
        pass

    def draw_background(self, screen):
        screen.fill((0, 0, 0))

    # ------------------------------------------------------------------------------------------------------------------

    def lose(self):
        # Соединение с EndStage
        all_time = self.bomb.level.time
        name_lvl = self.bomb.name_lvl
        modules_count = 6
        for module in self.bomb.modules:
            if isinstance(module, NoneModule):
                modules_count -= 1
        self.gm.stages["result"].load_data(
            False, self.time, self.mistakes, all_time, modules_count, name_lvl
        )
        self.gm.change_stage("result")

    def win(self):
        # Соединение с EndStage
        all_time = self.bomb.level.time
        name_lvl = self.bomb.name_lvl
        modules_count = 6
        for module in self.bomb.modules:
            if isinstance(module, NoneModule):
                modules_count -= 1
        self.gm.stages["result"].load_data(
            True, self.time, self.mistakes, all_time, modules_count, name_lvl
        )
        self.gm.change_stage("result")

    # ------------------------------------------------------------------------------------------------------------------

    def pause(self):
        # Паузы наверное не будет, пока что просто существует.
        pass
