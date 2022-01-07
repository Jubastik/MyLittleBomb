from random import choice, randint

from CONSTANTS import MODULES_COORDS, FPS
from Entities.BobmModules.BigButtonModule.BigButtonModule import BigButtonModule
from Entities.BobmModules.KeyBoardModule.KeyboardModule import KeyboardModule
from Entities.BobmModules.NoneModule.NoneModule import NoneModule
from Entities.BobmModules.TimerModule.TimerModule import TimerModule
from Entities.BobmModules.WiresModule.WiresModule import WiresModule
from Entities.BobmModules.ButtonsModule.ButtonsModule import ButtonsModule
from Resources.BombGenerateInfo.BombSerialNum import (
    SERIAL_NUMBERS_FIRST_SECTOR,
    SERIAL_NUMBERS_THIRD_SECTOR,
)


class Level4:
    """Уровень 1. Содержит универсальную информацию о уровне."""

    def __init__(self):
        self.mistakes = 0
        self.time = 300 * FPS

    def generate_serial_number(self):
        first = str(choice(SERIAL_NUMBERS_FIRST_SECTOR))
        second = str(randint(1001, 9999))
        third = str(choice(SERIAL_NUMBERS_THIRD_SECTOR))
        fourth = str(randint(1001, 9999))
        return [first, second, third, fourth]

    def generate_modules(self, bomb):
        # 6 модулей обязательно, обязательно в этом порядке.
        modules = [
            TimerModule(bomb, MODULES_COORDS[0]).init(),
            WiresModule(bomb, MODULES_COORDS[1]).init(),
            KeyboardModule(bomb, MODULES_COORDS[2]).init(),
            BigButtonModule(bomb, MODULES_COORDS[3]).init(),
            ButtonsModule(bomb, MODULES_COORDS[4]).init(),
            NoneModule(bomb, MODULES_COORDS[5]).init(),
        ]
        return modules

    def generate_indicators(self):
        return [randint(0, 1) == 0, randint(0, 1) == 0]

    def generate_battery(self):
        return randint(1, 3)
