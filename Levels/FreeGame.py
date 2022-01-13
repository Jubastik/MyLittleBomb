from random import sample
from Entities.BobmModules.BigButtonModule.BigButtonModule import BigButtonModule
from Entities.BobmModules.KeyBoardModule.KeyboardModule import KeyboardModule
from Entities.BobmModules.NoneModule.NoneModule import NoneModule
from Entities.BobmModules.TimerModule.TimerModule import TimerModule
from Entities.BobmModules.WiresModule.WiresModule import WiresModule
from Entities.BobmModules.ButtonsModule.ButtonsModule import ButtonsModule
from Entities.BobmModules.Ahmed_module.AhmedModule import AhmedModule
from CONSTANTS import FPS, MODULES_COORDS
from Levels.LevelClass import Level


class FreeLevel(Level):
    """Уровень 1. Содержит универсальную информацию о уровне."""

    types = [BigButtonModule, KeyboardModule, WiresModule, ButtonsModule, AhmedModule]

    def __init__(self, time, modules_count, hardmode=False):
        self.name = "own"
        self.time = time * FPS
        self.modules_count = modules_count  # от 1 до 5
        self.mistakes = 2 if hardmode else 0

    def generate_modules(self, bomb):
        modules = [
            TimerModule(bomb, MODULES_COORDS[0]).init(),
            NoneModule(bomb, MODULES_COORDS[1]).init(),
            NoneModule(bomb, MODULES_COORDS[2]).init(),
            NoneModule(bomb, MODULES_COORDS[3]).init(),
            NoneModule(bomb, MODULES_COORDS[4]).init(),
            NoneModule(bomb, MODULES_COORDS[5]).init(),
        ]
        rand_modules = sample(self.types, self.modules_count)
        # Поясню: Есть список КЛАССОВ! не объектов, мы перебираем его в цикле и получаются разные модули.
        for m, module in zip(range(1, len(modules)), rand_modules):
            modules[m] = module(bomb, modules[m]._cords).init()
        return modules
