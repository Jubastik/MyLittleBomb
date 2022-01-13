import random

import webbrowser
import pygame
import pygame_gui

from CONSTANTS import WIDTH, HEIGHT
from GameStages.Stage import Stage
from image_loader import load_image


class MenuStage(Stage):
    """Меню игры"""

    def init(self):
        self.ui_manager = self.gm.ui_manager
        self.background = pygame.Surface((self.width, self.height))
        self.init_gui()
        self.gui_off()
        self.volume_font = pygame.font.Font(r'Resources/Pixeboy.ttf', 60)
        self.volume_font_small = pygame.font.Font(r'Resources/Pixeboy.ttf', 50)
        return self

    def draw(self, screen):
        self.background.fill((255, 255, 255))
        self.all_sprites.draw(self.background)
        screen.blit(self.background, (0, 0))
        self.draw_volume(screen)

    def draw_volume(self, screen):
        # Отрисовка блока громкости
        volume = str(int(self.gm.music_manager.volume * 100))
        res = self.volume_font.render(volume, True, (255, 0, 0))
        screen.blit(res, (self.width - 180, self.height - 90))

        txt = "volume"
        res = self.volume_font_small.render(txt, True, (255, 0, 0))
        screen.blit(res, (self.width - 225, self.height - 135))

    def init_gui(self):
        # создание кнопки "выбор уровня"
        self.choose_lvl = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((880, 440), (170, 50)),
            text='Выбор уровня',
            manager=self.ui_manager
        )
        # создание кнопки "инструкция"
        self.instruction = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((880, 500), (170, 50)),
            text='Инструкция',
            manager=self.ui_manager
        )
        # создание кнопки "выход"
        self.leave_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((880, 560), (170, 50)),
            text='Выход',
            manager=self.ui_manager
        )
    def init_music_block(self):
        self.volume_up = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 100, self.height - 100), (50, 50)),
            text='+',
            manager=self.ui_manager
        )
        self.volume_down = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 250, self.height - 100), (50, 50)),
            text='-',
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
                bomb = Bomb(self.one_sprite)
                if pygame.sprite.spritecollideany(bomb, self.all_sprites) is None:
                    self.all_sprites.add(bomb)
                # обнуляем таймер
            self.timer = 30
        # обновляем положение всех спрайтов
        self.all_sprites.update()
        self.timer -= 1

    def process_event(self, event):
        # по нажатии на кнопку идем в метод спрайтов
        if event.type == pygame.MOUSEBUTTONDOWN:
            for el in self.all_sprites.sprites():
                if isinstance(el, Bomb):
                    el.process_click(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # если нажата кнопка выбора уровня
                # переходим на след. окно
                if event.ui_element == self.choose_lvl:
                    self.gm.change_stage('choose_lvl')
                    self.gui_off()
                # кнопка настроек
                if event.ui_element == self.instruction:
                    webbrowser.open(
                        'https://docs.google.com/document/d/10K39vNIL9V1iu4_iRRIUM3-GUT3xu5T9xGU2inMUlX4/edit#heading=h.e8v6mr9vk98s',
                        new=1)
                # кнопка выхода
                if event.ui_element == self.leave_game:
                    self.gui_off()
                    self.gm.run = False
                if event.ui_element == self.volume_up:
                    self.gm.music_manager.change_volume(+5)
                if event.ui_element == self.volume_down:
                    self.gm.music_manager.change_volume(-5)

    # включаем кнопки (делаем их доступными)
    def gui_on(self):
        self.leave_game.visible = True
        self.choose_lvl.visible = True
        self.instruction.visible = True
        self.volume_up.visible = True
        self.volume_down.visible = True

    # выключаем кнопки
    def gui_off(self):
        self.leave_game.visible = False
        self.choose_lvl.visible = False
        self.instruction.visible = False
        self.volume_up.visible = False
        self.volume_down.visible = False


class Bomb(pygame.sprite.Sprite):
    image = load_image('pixil-frame-0 (3).png')
    image_boom = load_image('pixel_boom.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
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
            self.rect.x -= 25
            self.rect.y -= 20
