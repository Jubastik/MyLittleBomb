import pygame
from image_loader import load_image
from CONSTANTS import BOMB_IMG_X, BOMB_IMG_Y, SERIAL_NUM_IMG_FONT_SIZE, SERIAL_NUM_IMG_FONT, SERIAL_NUM_IMG_X, SERIAL_NUM_IMG_Y


class Bomb:
    """Класс бомбы"""

    def __init__(self, stage, level):
        self.serial_number = level.serial_number
        self.modules = level.modules
        self.stage = stage
        self.bomb_image = load_image(r"bomb.png")

    def draw(self):
        self.draw_bomb()
        self.draw_serial_number()
        self.draw_modules()

    def draw_bomb(self, screen):
        screen.blit(self.background, (BOMB_IMG_X, BOMB_IMG_Y))

    def draw_serial_number(self, screen):
        font = pygame.font.Font(SERIAL_NUM_IMG_FONT, SERIAL_NUM_IMG_FONT_SIZE)
        text = font.render("Hello, Pygame!", True, (100, 255, 100))
        screen.blit(text, (SERIAL_NUM_IMG_X, SERIAL_NUM_IMG_Y))

    def draw_modules(self):
        for module in self.modules:
            module.draw()

    def update(self):
        for module in self.modules:
            module.update()

    def click_LKM(self, x, y):
        """Определяем модуль и перенаправляем инфу в модуль
        pos - координаты клика относительно начала координат"""
        res_module = None
        for module in self.modules:
            if module.x <= x <= module.x2 and module.y <= y <= module.y2:
                res_module = module
                break
        else:
            return
        res_module.click_LKM(x, y)
