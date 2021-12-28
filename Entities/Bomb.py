import pygame
from Resources.BombGenerateInfo.BombSerialNum import (
    SERIAL_NUMBERS_FIRST_SECTOR,
    SERIAL_NUMBERS_THIRD_SECTOR,
)
from CONSTANTS import BOMB_X, BOMB_Y, BOMB_X2, BOMB_Y2


class Bomb:
    """Класс бомбы"""

    def __init__(self, stage, level):
        self.serial_number = level.serial_number
        self.modules = level.modules
        self.stage = stage

    def draw(self):
        self.draw_bomb()
        self.draw_serial_number()
        self.draw_modules()

    def draw_bomb(self):
        pass

    def draw_serial_number(self):
        pass

    def draw_modules(self):
        for module in self.modules:
            module.draw()

    def update(self):
        for module in self.modules:
            module.update()

    def bomb_click_LKM(self, pos):
        """Определяем модуль и перенаправляем инфу в модуль
        pos - координаты клика относительно начала координат"""
        x, y = pos # x, y - место клика
        res_module = None
        for module in self.modules:
            if module.x <= x <= module.x2 and module.y <= y <= module.y2:
                res_module = module
                break
        else:
            return
        res_module.click_LKM()