import pygame
from CONSTANTS import *
from GameManager import GameManager
from CONSTANTS import FPS, WIDTH, HEIGHT

def launch():
    '''Запускает игру'''
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Voice neutralization')
    gm = GameManager(screen, FPS)
    gm.loop()
    pygame.quit()


if __name__ == '__main__':
    launch()