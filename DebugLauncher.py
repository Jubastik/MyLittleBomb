import ctypes

import pygame

from CONSTANTS import FPS, WIDTH, HEIGHT
from GameManager import GameManager


def launch():
    """Запускает игру, дебаг версия. Творим здесь что хотим :)"""

    ctypes.windll.user32.SetProcessDPIAware()  # игнорирование масштабирования Windows
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Voice neutralization")
    gm = GameManager(screen, FPS)
    gm.loop()
    pygame.quit()


if __name__ == "__main__":
    launch()
