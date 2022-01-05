import pygame
from random import randint
from image_loader import load_image
from CONSTANTS import (
    BOMB_IMG_W,
    BOMB_IMG_H,
    BOMB_IMG_X,
    BOMB_IMG_Y,
    SERIAL_NUM_IMG_FONT_SIZE,
    SERIAL_NUM_IMG_FONT,
    SERIAL_NUM_IMG_X,
    SERIAL_NUM_IMG_Y,
    LIGHTNING_SPEED,
)


class Bomb:
    """Класс бомбы. Перед использованием обязательно передаём объект бомбы через метод self.load_level(level).
    Подробнее в файле с GameStage"""

    def __init__(self, gs):
        self.pressed_module = None
        self.gs = gs
        self.bomb_image_on = load_image(r"Bomb/bomb_on.png").convert()
        self.bomb_image_off = load_image(r"Bomb/bomb_off.png").convert()
        self.battery_image = load_image(r"Bomb/battery.png").convert()
        self.lightning_speed = LIGHTNING_SPEED[0]
        self.lightning_now = 0
        self.timer = -1
        self.bomb_image = load_image(r"Bomb/bomb.png").convert()

    def load_level(self, level):
        self.serial_number = level.generate_serial_number()
        self.indicators = level.generate_indicators()
        self.batteries = level.generate_battery()
        self.modules = level.generate_modules(self) # Запускать последним тк могут быть баги

    def draw(self, screen):
        # Картинка рисуется послойно
        self.draw_bomb(screen)
        self.draw_serial_number(screen)
        self.draw_modules(screen)
        self.draw_indicators(screen)
        self.draw_batteries(screen)

    def draw_bomb(self, screen):
        if self.timer <= 0:
            self.lightning_now = (self.lightning_now + 1) % 2
            self.timer = LIGHTNING_SPEED[(self.gs.time // 1000) - 1][self.lightning_now]
        if self.lightning_now == 0:
            screen.blit(self.bomb_image_off, (BOMB_IMG_X, BOMB_IMG_Y))
        else:
            screen.blit(self.bomb_image_on, (BOMB_IMG_X, BOMB_IMG_Y))
        self.timer -= 1

    def draw_serial_number(self, screen):
        font = pygame.font.Font(SERIAL_NUM_IMG_FONT, SERIAL_NUM_IMG_FONT_SIZE)
        text = font.render("-".join(self.serial_number), True, (255, 255, 255))
        screen.blit(text, (SERIAL_NUM_IMG_X, SERIAL_NUM_IMG_Y))

    def draw_modules(self, screen):
        """Запрос на отрисовку модулям"""
        for module in self.modules:
            module.draw(screen)

    def draw_indicators(self, screen):
        if not self.indicators[0]:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                pygame.Rect(BOMB_IMG_X + 135, BOMB_IMG_Y + 45, 15, 15),
                width=0,
            )
        elif not self.indicators[1]:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                pygame.Rect(BOMB_IMG_X + 135, BOMB_IMG_Y + 90, 15, 15),
                width=0,
            )

    def draw_batteries(self, screen):
        x, y = BOMB_IMG_X + BOMB_IMG_W, BOMB_IMG_Y
        for i in range(self.batteries):
            screen.blit(self.battery_image, (x, y))
            y += 100

    def update(self):
        for module in self.modules:
            module.update()
        # Проверка на победу
        for module in self.modules:
            if not module.isdefused:
                break
        else:
            self.gs.win()

    def LKM_down(self, x, y):
        """Определяем модуль и перенаправляем инфу в модуль"""
        res_module = None
        for module in self.modules:
            if module.x <= x <= module.x2 and module.y <= y <= module.y2:
                res_module = module
                break
        else:
            return
        res_module.LKM_down(x, y)
        self.pressed_module = res_module

    def LKM_up(self, x, y):
        if self.pressed_module is not None:
            self.pressed_module.LKM_up(x, y)
            self.pressed_module = None
