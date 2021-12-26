import pygame
from Entities.BobmModules.Timer import Timer
from Entities.BobmModules.Wires import Wires
from Entities.BobmModules.NoneModule import NoneModule


class Level1:
    """Уровень 1. Содержит универсальную информацию о уровне."""

    def __init__(self):
        # 6 штук обязательно
        self.modules = {
            'timer': Timer().init(),
            'wires': Wires().init(),
            'NoneModule': NoneModule().init(),
        }