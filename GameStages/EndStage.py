import random

import pygame
import pygame_gui

from CONSTANTS import WIDTH, HEIGHT
from GameStages.Stage import Stage
from image_loader import load_image


class EndStage(Stage):
    """Подсчёт результатов"""

    def init(self):
        self.ui_manager = self.gm.ui_manager
        self.background = pygame.Surface((self.width, self.height))
        self.init_gui()
        self.gui_off()

        return self

    def load_data(self, is_win, time):
        self.is_win = is_win
        minuts = round((time / 30) // 60)
        sec = (time / 30) % 60
        self.time = f'{int(minuts)}:{int(sec)}'

    def draw(self, screen):
        self.background.fill((255, 255, 255))
        self.all_sprites.draw(self.background)
        screen.blit(self.background, (0, 0))
        txt = 'Game over'
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 80)
        res = font.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 130, 260))

        txt = '1. Identifier'
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 30)
        res = font.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 360))

        txt = '2. Bomb parameters'
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 30)
        res = font.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 440))

        txt = '3. Result'
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 30)
        res = font.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 520))
        if self.is_win:
            txt = 'DEFUSED'
            res = font.render(txt, True, (0, 255, 0))
        else:
            txt = 'EXPLODED'
            res = font.render(txt, True, (255, 0, 0))
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 55)
        screen.blit(res, (WIDTH / 2 - 100, 550))

        txt = 'Time left'
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 40)
        res = font.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 80, 600))
        txt = f'{self.time}'
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 55)
        res = font.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 45, 640))

    def init_gui(self):
        # создание кнопки "выбор уровня"
        self.choose_lvl = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 800), (190, 60)),
            text='Вернуться',
            manager=self.ui_manager
        )
        # создание кнопки "заново"
        self.repeat = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((950, 800), (190, 60)),
            text='Зановово',
            manager=self.ui_manager
        )

    def stage_launch(self):
        # включаем кнопки, создаем группу для спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.one_sprite = pygame.sprite.Group()
        self.timer = 30
        self.gui_on()

    def update(self):
        # когда проходит 2 сек создаем 16 бомб в рандомных местах
        if self.timer == 0:
            for _ in range(16):
                # //////////////////////////////////////////////////////
                if self.is_win:
                    bomb = Vin(self.one_sprite)
                else:
                    bomb = Lose(self.one_sprite)
                # //////////////////////////////////////////////////////
                if pygame.sprite.spritecollideany(bomb, self.all_sprites) is None:
                    self.all_sprites.add(bomb)
                # обнуляем таймер
            self.timer = 30
        # обновляем положение всех спрайтов
        self.all_sprites.update()
        self.timer -= 1

    def process_event(self, event):
        if not self.is_win:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for el in self.all_sprites.sprites():
                    if isinstance(el, Lose):
                        el.process_click(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # если нажата кнопка выбора уровня
                # переходим на след. окно
                if event.ui_element == self.choose_lvl:
                    self.gm.change_stage('choose_lvl')
                    self.gui_off()
                # кнопка настроек
                if event.ui_element == self.repeat:
                    self.gm.change_stage("game")
                    self.gui_off()
                # кнопка выхода

    # включаем кнопки (делаем их доступными)
    def gui_on(self):
        self.choose_lvl.visible = True
        self.repeat.visible = True

    # выключаем кнопки
    def gui_off(self):
        self.choose_lvl.visible = False
        self.repeat.visible = False


class Vin(pygame.sprite.Sprite):
    image = load_image('vin_cubok.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Vin.image
        self.v = 4
        self.r = random.randint(50, 1000)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(-200, -45)

    def update(self):
        # меняем координаты по y
        self.rect.y += self.v
        # когда спрайт опустился за экран, удаляем спрайт
        if self.rect.y >= 1120:
            self.kill()


class Lose(pygame.sprite.Sprite):
    image = load_image('girl_scelet3.png')
    image_boom = load_image('boy_scelet3.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Lose.image
        self.v = 4
        self.r = random.randint(50, 1000)
        self.rect = self.image.get_rect()
        self.fortune = random.randint(1, 100)
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(-200, -45)

    def update(self):
        # меняем координаты по y
        self.rect.y += self.v
        # удаляем сами рандомные бомбы
        if self.fortune % 5 == 0 \
                or self.fortune % 2 == 0 \
                or self.fortune % 3 == 0 \
                or self.fortune % 7 == 0:
            if self.rect.y == HEIGHT - self.r:
                self.image = self.image_boom
        # когда спрайт опустился за экран, удаляем спрайт
        if self.rect.y >= 1120:
            self.kill()

    def process_click(self, *args):
        # при нажатии на спрайт меняем картинку спрайта
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom
