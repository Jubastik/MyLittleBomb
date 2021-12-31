import pygame
from random import choice, randint
from Entities.BobmModules.TimerModule import TimerModule
from Entities.BobmModules.WiresModule import WiresModule
from Entities.BobmModules.NoneModule import NoneModule
from CONSTANTS import MODULES_COORDS
from Resources.BombGenerateInfo.BombSerialNum import SERIAL_NUMBERS_FIRST_SECTOR, SERIAL_NUMBERS_THIRD_SECTOR


class Level1:
    """Уровень 1. Содержит универсальную информацию о уровне."""

    def __init__(self, bomb):
        # 6 аргументов обязательно, обязательно в этом порядке.
        self.modules = [
            TimerModule(bomb, MODULES_COORDS[0]).init(),
            WiresModule(bomb, MODULES_COORDS[1]).init(),
            NoneModule(bomb, MODULES_COORDS[2]).init(),
            NoneModule(bomb, MODULES_COORDS[3]).init(),
            NoneModule(bomb, MODULES_COORDS[4]).init(),
            NoneModule(bomb, MODULES_COORDS[5]).init(),
        ]
        self.serial_number = self.generate_serial_number()

    def generate_serial_number(self):
        first = str(choice(SERIAL_NUMBERS_FIRST_SECTOR))
        second = str(randint(1001, 9999))
        third = str(choice(SERIAL_NUMBERS_THIRD_SECTOR))
        fourth = str(randint(1001, 9999))
        return [first, second, third, fourth]