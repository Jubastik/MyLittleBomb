import pygame
from image_loader import load_image
from CONSTANTS import (
    BOMB_IMG_X,
    BOMB_IMG_Y,
    SERIAL_NUM_IMG_FONT_SIZE,
    SERIAL_NUM_IMG_FONT,
    SERIAL_NUM_IMG_X,
    SERIAL_NUM_IMG_Y,
)


class Bomb:
    """Класс бомбы. Перед использованием обязательно передаём объект бомбы через метод self.load_level(level).
    Подробнее в файле с GameStage"""

    def __init__(self, gs):
        self.gs = gs
        self.bomb_image = load_image(r"Bomb\bomb.png")

    def load_level(self, level):
        self.serial_number = level.generate_serial_number()
        self.modules = level.generate_modules(self)

    def draw(self, screen):
        # Картинка рисуется послойно
        self.draw_bomb(screen)
        self.draw_serial_number(screen)
        self.draw_modules(screen)

    def draw_bomb(self, screen):
        screen.blit(self.bomb_image, (BOMB_IMG_X, BOMB_IMG_Y))

    def draw_serial_number(self, screen):
        font = pygame.font.Font(SERIAL_NUM_IMG_FONT, SERIAL_NUM_IMG_FONT_SIZE)
        text = font.render("-".join(self.serial_number), True, (255, 255, 255))
        screen.blit(text, (SERIAL_NUM_IMG_X, SERIAL_NUM_IMG_Y))

    def draw_modules(self, screen):
        '''Запрос на отрисовку модулям'''
        for module in self.modules:
            module.draw(screen)

    def update(self):
        for module in self.modules:
            module.update()
        # Проверка на победу
        for module in self.modules:
            if not module.isdefused:
                break
        else:
            self.gs.win()

    def click_LKM(self, x, y):
        """Определяем модуль и перенаправляем инфу в модуль"""
        res_module = None
        for module in self.modules:
            if module.x <= x <= module.x2 and module.y <= y <= module.y2:
                res_module = module
                break
        else:
            return
        res_module.click_LKM(x, y)
