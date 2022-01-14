from CONSTANTS import MODULES_COORDS, FPS
from Entities.BobmModules.NoneModule.NoneModule import NoneModule
from Entities.BobmModules.TimerModule.TimerModule import TimerModule
from Entities.BobmModules.WiresModule.WiresModule import WiresModule
from Entities.BobmModules.ButtonsModule.ButtonsModule import ButtonsModule
from Levels.LevelClass import Level


class Level1(Level):
    def __init__(self):
        self.name = "1"
        self.mistakes = 0
        self.time = 300 * FPS

    def generate_modules(self, bomb):
        # 6 модулей обязательно, обязательно в этом порядке.
        modules = [
            TimerModule(bomb, MODULES_COORDS[0]).init(),
            WiresModule(bomb, MODULES_COORDS[1]).init(),
            ButtonsModule(bomb, MODULES_COORDS[2]).init(),
            NoneModule(bomb, MODULES_COORDS[3]).init(),
            NoneModule(bomb, MODULES_COORDS[4]).init(),
            NoneModule(bomb, MODULES_COORDS[5]).init(),
        ]
        return modules
