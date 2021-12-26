import pygame
from random import choice, randint
from Entities.BobmModules.Wires import Wires
from Resources.BombGenerateInfo.BombSerialNum import SERIAL_NUMBERS_FIRST_SECTOR, SERIAL_NUMBERS_THIRD_SECTOR

class Bomb:
    """Класс бомбы"""

    def __init__(self, level):
        self.level = level
        self.serial_number = self.generate_serial_number()
        self.modules = level.modules
    
    def generate_serial_number(self):
        first = choice(SERIAL_NUMBERS_FIRST_SECTOR)
        second = randint(1001, 9999)
        third = choice(SERIAL_NUMBERS_THIRD_SECTOR)
        fourth = randint(1001, 9999)
        return [first, second, third, fourth]
    
    def draw(self):
        self.draw_background()
        self.draw_bomb()
        self.draw_modules()

    def draw_bomb(self):
        pass

    def draw_background(self):
        pass

    def draw_modules(self):
        pass
    
    def update(self):
        pass

    def on_click(self, pos):
        pass
