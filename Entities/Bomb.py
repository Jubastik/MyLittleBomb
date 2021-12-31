import pygame
from image_loader import load_image
from CONSTANTS import BOMB_IMG_X, BOMB_IMG_Y, SERIAL_NUM_IMG_FONT_SIZE, SERIAL_NUM_IMG_FONT, SERIAL_NUM_IMG_X, SERIAL_NUM_IMG_Y


class Bomb:
    """Класс бомбы"""

    def __init__(self, stage):
        self.stage = stage
        self.bomb_image = load_image(r"bomb.png")
    
    def load_level(self, level):
        self.serial_number = level.serial_number
        self.modules = level.modules

    def draw(self, screen):
        self.draw_bomb(screen)
        self.draw_serial_number(screen)
        self.draw_modules(screen)

    def draw_bomb(self, screen):
        screen.blit(self.bomb_image, (BOMB_IMG_X, BOMB_IMG_Y))

    def draw_serial_number(self, screen):
        font = pygame.font.Font(SERIAL_NUM_IMG_FONT, SERIAL_NUM_IMG_FONT_SIZE)
        text = font.render('-'.join(self.serial_number), True, (255, 255, 255))
        screen.blit(text, (SERIAL_NUM_IMG_X, SERIAL_NUM_IMG_Y))

    def draw_modules(self, screen):
        for module in self.modules:
            module.draw(screen)

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
