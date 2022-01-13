from random import randint

import pygame
from Levels.FreeGame import FreeLevel
from Entities.Bomb import Bomb
from image_loader import load_image

# Позиции элементов относительно модуля
RANDOM_BTN_POS = (385, 252)
TIME_REDUCE_BTN_POS = (91, 504)
TIME_INCREASE_BTN_POS = (371, 504)
MODULES_REDUCE_BTN_POS = (91, 644)
MODULES_INCREASE_BTN_POS = (371, 644)
TIME_POS = (226, 518)
MODULES_POS = (260, 658)
BANANA_POS = (98, 812)
START_BTN_POS = (336, 812)


class OwnLevel:
    def __init__(self, x, y):
        self.font = pygame.font.Font(r'Resources/Pixeboy.ttf', 60)
        # Координаты блока
        self.x = x
        self.y = y
        self.pos = (x, y)

        self.init_img()
        self.init_start_btn()
        self.sprite_time = 0  # Время нахождения курсора на блоке
        self.banana_time = 0  # Время нахождения банана в одном из состояний
        self.lamp_on = False
        self.hard_mode = False
        self.lvl_time = 300
        self.lvl_modules = 3

    def init_img(self):
        # Инициализация изображений
        self.main_images = load_image("LevelChooseImg/own_lvl_main.png").convert()
        self.random_btn = load_image("LevelChooseImg/random_btn.png").convert()
        self.lamp_image = load_image("LevelChooseImg/own_lvl_lamp.png")
        self.reduce_btn = load_image("LevelChooseImg/reduce_button.png").convert()
        self.increase_btn = load_image("LevelChooseImg/increase_button.png").convert()
        self.banana_left = load_image("LevelChooseImg/banana1.png")
        self.banana_right = load_image("LevelChooseImg/banana2.png")
        self.banana = self.banana_left

    def init_start_btn(self):
        self.all = pygame.sprite.Group()
        self.start_btn = StartBtn(self, self.all, self.x, self.y)

    def draw(self, screen):
        screen.blit(self.main_images, self.pos)
        if self.lamp_on:
            screen.blit(self.lamp_image, self.pos)
        self.draw_btn(screen)
        self.draw_time(screen)
        self.draw_modules(screen)
        self.all.draw(screen)

    def draw_btn(self, screen):
        # Отрисовка и сохранения прямоугольников кнопок
        self.random_btn_rect = screen.blit(self.random_btn, (self.x + RANDOM_BTN_POS[0], self.y + RANDOM_BTN_POS[1]))
        self.time_reduce_rect = screen.blit(
            self.reduce_btn, (self.x + TIME_REDUCE_BTN_POS[0], self.y + TIME_REDUCE_BTN_POS[1]))
        self.time_increase_rect = screen.blit(
            self.increase_btn, (self.x + TIME_INCREASE_BTN_POS[0], self.y + TIME_INCREASE_BTN_POS[1]))
        self.modules_reduce_rect = screen.blit(
            self.reduce_btn, (self.x + MODULES_REDUCE_BTN_POS[0], self.y + MODULES_REDUCE_BTN_POS[1]))
        self.modules_increase_rect = screen.blit(
            self.increase_btn, (self.x + MODULES_INCREASE_BTN_POS[0], self.y + MODULES_INCREASE_BTN_POS[1]))
        self.banana_rect = screen.blit(self.banana, (self.x + BANANA_POS[0], self.y + BANANA_POS[1]))

    def draw_time(self, screen):
        # Отрисовка времени игры
        time = f'{self.lvl_time // 60}:{self.lvl_time % 60}'.ljust(4, "0")
        res = self.font.render(time, True, (255, 0, 0))
        screen.blit(res, (self.x + TIME_POS[0], self.y + TIME_POS[1]))

    def draw_modules(self, screen):
        # Отрисовка количества модулей
        res = self.font.render(str(self.lvl_modules), True, (255, 0, 0))
        screen.blit(res, (self.x + MODULES_POS[0], self.y + MODULES_POS[1]))

    def update(self):
        self.banana_time += 1
        if self.banana_time == 20:  # 20 просто число
            self.next_banana()
            self.banana_time = 0

    def next_banana(self):
        if self.banana == self.banana_left:
            self.banana = self.banana_right
        else:
            self.banana = self.banana_left

    def LKM_down(self, x, y):
        self.button_processing(x, y)

    def button_processing(self, x, y):
        if self.random_btn_rect.collidepoint((x, y)):
            self.start_random_mode()
        if self.time_reduce_rect.collidepoint((x, y)):
            self.time_reduce()
        if self.time_increase_rect.collidepoint((x, y)):
            self.time_increase()
        if self.modules_reduce_rect.collidepoint((x, y)):
            self.modules_reduce()
        if self.modules_increase_rect.collidepoint((x, y)):
            self.modules_increase()
        if self.banana_rect.collidepoint((x, y)):
            self.hard_mode = not self.hard_mode
            self.start_btn.hard_mode()
        self.start_btn.check((x, y))

    def start_random_mode(self):
        hard_mode, modules, time = self.random_bomb_generation()
        time = (time // 30) * 30  # Округление времени
        # Время на 1 модуль должно находиться в границах от 20 до 120 сек
        if time // modules >= 20 and time // modules <= 120:
            pass
            # hard_mode, modules, time = self.hard_mode, self.lvl_time, self.lvl_modules
            # bomb = Bomb(self.gm.stages["game"])
            # level = FreeLevel(time, modules, hardmode=hard_mode)
            # bomb.load_level(level)
            # self.gm.stages["game"].set_bomb(bomb)
            # self.gm.change_stage("game")
        else:
            self.start_random_mode()

    def start_game(self):
        pass
        # hard_mode, modules, time = self.hard_mode, self.lvl_time, self.lvl_modules
        # bomb = Bomb(self.gm.stages["game"])
        # level = FreeLevel(time, modules, hardmode=hard_mode)
        # bomb.load_level(level)
        # self.gm.stages["game"].set_bomb(bomb)
        # self.gm.change_stage("game")


    def on_sprite(self):
        # Изменение времени нахождения курсора на блоке
        self.sprite_time += 1
        if self.sprite_time == 20:
            self.lamp_on = not self.lamp_on
            self.sprite_time = 0

    def time_reduce(self):
        if self.lvl_time - 30 >= 30:
            self.lvl_time -= 30

    def time_increase(self):
        if self.lvl_time + 30 <= 570:
            self.lvl_time += 30

    def modules_reduce(self):
        if self.lvl_modules - 1 >= 1:
            self.lvl_modules -= 1

    def modules_increase(self):
        if self.lvl_modules + 1 <= 5:
            self.lvl_modules += 1

    def random_bomb_generation(self):
        if randint(0, 20) == 15:
            hard_mode = True
        else:
            hard_mode = False
        return hard_mode, randint(1, 6), randint(30, 570)


class StartBtn(pygame.sprite.Sprite):
    image = {
        "red": load_image("LevelChooseImg/start_button_red.png"),
        "black": load_image("LevelChooseImg/start_button_black.png"),
    }

    def __init__(self, OL, group, x, y):
        super().__init__(group)
        self.OL = OL
        self.color = "red"
        self.image = StartBtn.image[self.color]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = START_BTN_POS[0] + x
        self.rect.y = START_BTN_POS[1] + y

    def hard_mode(self):
        if self.color == "red":
            self.color = "black"
        else:
            self.color = "red"
        self.image = StartBtn.image[self.color]

    def start(self):
        # При нажатии на кнопку активируется запуск  игры
        self.OL.start_game()

    def check(self, pos):
        try:
            if self.mask.get_at((pos[0] - self.rect.x, pos[1] - self.rect.y)):
                self.start()
        except IndexError:
            pass
