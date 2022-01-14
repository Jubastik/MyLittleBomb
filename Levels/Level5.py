from CONSTANTS import MODULES_COORDS, FPS
from Entities.BobmModules.KeyBoardModule.KeyboardModule import KeyboardModule
from Entities.BobmModules.TimerModule.TimerModule import TimerModule
from Levels.LevelClass import Level


class Level5(Level):
    def __init__(self):
        self.name = "5"
        self.mistakes = 0
        self.time = 300 * FPS

    def generate_modules(self, bomb):
        # 6 модулей обязательно, обязательно в этом порядке.
        modules = [
            TimerModule(bomb, MODULES_COORDS[0]).init(),
            KeyboardModule(bomb, MODULES_COORDS[1]).init(),
            KeyboardModule(bomb, MODULES_COORDS[2]).init(),
            KeyboardModule(bomb, MODULES_COORDS[3]).init(),
            KeyboardModule(bomb, MODULES_COORDS[4]).init(),
            KeyboardModule(bomb, MODULES_COORDS[5]).init(),
        ]
        return modules
