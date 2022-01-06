import pygame

from image_loader import load_image

RANDOM_BTN_POS = (385, 252)
TIME_REDUCE_BTN_POS = (91, 504)
TIME_INCREASE_BTN_POS = (371, 504)
MODULES_REDUCE_BTN_POS = (91, 644)
MODULES_INCREASE_BTN_POS = (371, 644)
TIME_POS = (226, 518)
MODULES_POS = (260, 658)
BANANA_POS = (98, 812)


class OwnLevel:
    def __init__(self, x, y):
        self.font = pygame.font.Font(r'Resources/Pixeboy.ttf', 60)
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.init_img()
        self.sprite_time = 0
        self.banana_time = 0
        self.lamp_on = False
        self.lvl_time = 300
        self.lvl_modules = 3

    def init_img(self):
        self.main_images = load_image("LevelChooseImg/own_lvl_main.png").convert()
        self.random_btn = load_image("LevelChooseImg/random_btn.png").convert()
        self.lamp_image = load_image("LevelChooseImg/own_lvl_lamp.png")
        self.reduce_btn = load_image("LevelChooseImg/reduce_button.png").convert()
        self.increase_btn = load_image("LevelChooseImg/increase_button.png").convert()
        self.banana_left = load_image("LevelChooseImg/banana1.png")
        self.banana_right = load_image("LevelChooseImg/banana2.png")
        self.banana = self.banana_left

    def draw(self, screen):
        screen.blit(self.main_images, self.pos)
        if self.lamp_on:
            screen.blit(self.lamp_image, self.pos)
        self.draw_btn(screen)
        self.draw_time(screen)
        self.draw_modules(screen)
        screen.blit(self.banana, (self.x + BANANA_POS[0], self.y + BANANA_POS[1]))

    def draw_btn(self, screen):
        self.random_btn_rect = screen.blit(self.random_btn, (self.x + RANDOM_BTN_POS[0], self.y + RANDOM_BTN_POS[1]))
        self.time_reduce_rect = screen.blit(
            self.reduce_btn, (self.x + TIME_REDUCE_BTN_POS[0], self.y + TIME_REDUCE_BTN_POS[1]))
        self.time_increase_rect = screen.blit(
            self.increase_btn, (self.x + TIME_INCREASE_BTN_POS[0], self.y + TIME_INCREASE_BTN_POS[1]))
        self.modules_reduce_rect = screen.blit(
            self.reduce_btn, (self.x + MODULES_REDUCE_BTN_POS[0], self.y + MODULES_REDUCE_BTN_POS[1]))
        self.modules_increase_rect = screen.blit(
            self.increase_btn, (self.x + MODULES_INCREASE_BTN_POS[0], self.y + MODULES_INCREASE_BTN_POS[1]))

    def draw_time(self, screen):
        time = f'{self.lvl_time // 60}:{self.lvl_time % 60}'.ljust(4, "0")
        res = self.font.render(time, True, (255, 0, 0))
        screen.blit(res, (self.x + TIME_POS[0], self.y + TIME_POS[1]))

    def draw_modules(self, screen):
        res = self.font.render(str(self.lvl_modules), True, (255, 0, 0))
        screen.blit(res, (self.x + MODULES_POS[0], self.y + MODULES_POS[1]))

    def update(self):
        self.banana_time += 1
        if self.banana_time == 20:
            self.next_banana()
            self.banana_time = 0

    def next_banana(self):
        if self.banana == self.banana_left:
            self.banana = self.banana_right
        else:
            self.banana = self.banana_left

    def LKM_down(self, x, y):
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

    def start_random_mode(self):
        print("random mode")

    def on_sprite(self):
        self.sprite_time += 1
        if self.sprite_time == 20:
            self.lamp_on = not self.lamp_on
            self.sprite_time = 0

    def time_reduce(self):
        print("time -1")
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
