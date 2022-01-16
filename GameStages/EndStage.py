import random
import sqlite3
import pygame
import pygame_gui

from CONSTANTS import WIDTH, HEIGHT, FPS
from GameStages.Stage import Stage
from image_loader import load_image


class EndStage(Stage):
    """Подсчёт результатов"""

    def init(self):
        self.b = False
        self.db = self.gm.DATABASE
        self.ui_manager = self.gm.ui_manager
        self.background = pygame.Surface((self.width, self.height))
        self.init_gui()
        self.gui_off()
        return self

    def load_data(self, is_win, time, mistakes, all_time, modules_count, name_lvl):
        # загружаем инф об уровне
        self.name_lvl = name_lvl
        self.mistakes = mistakes
        # кол-во всего времени
        all_time = all_time // FPS
        self.minuts = str(all_time // 60)
        self.sec = str(all_time % 60)
        if len(self.minuts) == 1:
            self.minuts = "0" + self.minuts
        if len(self.sec) == 1:
            self.sec = "0" + self.sec
        self.all_time = f'{self.minuts}:{self.sec}'

        self.modules_count = modules_count - 1
        self.is_win = is_win

        # кол-во оставшегося времени
        time = time // FPS
        self.minuts = str(time // 60)
        self.sec = str(time % 60)
        # Если однозначное число минут/секунд докидываем 0 перед числом (для красоты)
        if len(self.minuts) == 1:
            self.minuts = "0" + self.minuts
        if len(self.sec) == 1:
            self.sec = "0" + self.sec
        self.time = f'{self.minuts}:{self.sec}'

        self.font80 = pygame.font.Font(r'Resources/Pixeboy.ttf', 80)
        self.font30 = pygame.font.Font(r'Resources/Pixeboy.ttf', 30)
        self.font38 = pygame.font.Font(r'Resources/Pixeboy.ttf', 38)
        self.font40 = pygame.font.Font(r'Resources/Pixeboy.ttf', 40)
        self.font55 = pygame.font.Font(r'Resources/Pixeboy.ttf', 55)
        if is_win:
            self.insert_into_db()

    def data_base(self):
        pass

    def draw(self, screen):
        # выводим информацию на экран
        self.background.fill((255, 255, 255))
        self.all_sprites.draw(self.background)
        screen.blit(self.background, (0, 0))
        txt = 'Game over'
        res = self.font80.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 130, 260))

        txt = '1. Identifier'
        res = self.font30.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 360))
        full_lvl_name = LEVELS[self.name_lvl]
        txt = f'{full_lvl_name} level'
        res = self.font38.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 390))

        txt = '2. Bomb parameters'
        res = self.font30.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 440))
        # елси у нас 3 символа во времени, значит время в правильном формате
        if not self.b:
            if len(self.all_time) == 3:
                self.b = True
                self.all_time = str(self.all_time)
                self.all_time += '0'
        # добавляем ноль к числу
            else:
                self.b = True
        self.b = False
        if self.modules_count > 1:
            if self.mistakes > 1 or self.mistakes == 0:
                txt = f'{self.all_time} | {self.modules_count} moduls | {self.mistakes} mistakes'
            else:
                txt = f'{self.all_time} | {self.modules_count} moduls | {self.mistakes} mistake'
        else:
            if self.mistakes > 1 or self.mistakes == 0:
                txt = f'{self.all_time} | {self.modules_count} modul | {self.mistakes} mistakes'
            else:
                txt = f'{self.all_time} | {self.modules_count} modul | {self.mistakes} mistake'
        res = self.font38.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 473))

        txt = '3. Result'
        res = self.font30.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 520))
        if self.is_win:
            txt = 'DEFUSED'
            res = self.font38.render(txt, True, (0, 255, 0))
        else:
            txt = 'EXPLODED'
            res = self.font38.render(txt, True, (255, 0, 0))
        screen.blit(res, (WIDTH / 2 - 100, 550))

        txt = 'Time left'
        res = self.font40.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 50, 600))
        txt = f'{self.time}'
        if self.time == '0:0':
            txt = '0:00'
        res = self.font55.render(txt, True, (0, 0, 0))
        screen.blit(res, (WIDTH / 2 - 15, 640))

    def init_gui(self):
        # создание кнопки "выбор уровня"
        self.choose_lvl = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((780, 770), (190, 50)),
            text='Вернуться',
            manager=self.ui_manager
        )
        # создание кнопки "заново"
        self.repeat = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((1000, 770), (190, 50)),
            text='Заново',
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
                # загружаем разный background в зависимомти от результата
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
                # кнопка овтора уровня
                if event.ui_element == self.repeat:
                    self.restart_lvl()
                    self.gui_off()

    # включаем кнопки (делаем их доступными)
    def gui_on(self):
        self.choose_lvl.visible = True
        self.repeat.visible = True

    # выключаем кнопки
    def gui_off(self):
        self.choose_lvl.visible = False
        self.repeat.visible = False

    def restart_lvl(self):
        if self.name_lvl == "own":
            self.gm.stages["choose_lvl"].OwnLevel.start_game()
        elif self.name_lvl == '1':
            self.gm.stages["choose_lvl"].start_first_lvl()
        elif self.name_lvl == '2':
            self.gm.stages["choose_lvl"].start_second_lvl()
        elif self.name_lvl == '3':
            self.gm.stages["choose_lvl"].start_third_lvl()
        elif self.name_lvl == '4':
            self.gm.stages["choose_lvl"].start_fourth_lvl()
        elif self.name_lvl == '5':
            self.gm.stages["choose_lvl"].start_fifth_lvl()
        else:
            pass

    def insert_into_db(self):
        try:
            if self.name_lvl == 'own':
                self.db.insert_words(6, self.minuts, self.sec)
            else:
                self.db.insert_words(int(self.name_lvl), self.minuts, self.sec)
        except Exception:
            pass


# класс спрайтов при обезвреживаниии бомбы
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


# класс спрайтов при зрыве бомбы
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


LEVELS = {'1': 'First', '2': 'Second', '3': 'Third', '4': 'Fourth', '5': 'Fifth', 'own': 'Own'}
