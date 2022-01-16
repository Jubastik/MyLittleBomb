import ctypes
import os
import pygame
from CONSTANTS import FPS, WIDTH, HEIGHT
from GameManager import GameManager
import ctypes


def launch():
    """Запускает игру"""
    # меняем иконку в панели задач
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    if os.name == "nt":
        ctypes.windll.user32.SetProcessDPIAware()  # игнорирование масштабирования Windows
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.FULLSCREEN
    pygame.display.set_caption("Voice neutralization")
    gm = GameManager(screen, FPS)
    gm.loop()
    pygame.quit()


if __name__ == "__main__":
    launch()
