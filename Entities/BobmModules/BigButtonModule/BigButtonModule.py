from random import choice

import pygame
import CONSTANTS
from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image


class BigButtonModule(BobmModule):
    """Моудуль бомбы с большой кнопкой"""

    def init(self):
        self.isdefused = False
        self.click = False
        # кол-во батареек на бомбе
        self.BATTERY_COUNT = self.bomb.batteries
        # какой индикатор горит
        self.INDICATORS_COUNT = self.bomb.indicators
        self.module_img_off = load_image(r"Bomb/BigButton_module/BigButton_module_img_off.png")
        self.module_img_on = load_image(r"Bomb/BigButton_module/BigButton_module_img_on.png")
        self.module_img = self.module_img_on
        # переходим в функцию для рисования книпки, слов, полосок
        self.generate()
        return self

    def draw(self, screen):
        # отрисовываем сам модуль
        self.draw_background(screen)
        # если кнопка не нажата, то одно изображение
        if not self.click:
            self.button = screen.blit(self.button_default, self.position_button)
        # если кнопка нажата, то другое изображение
        if self.click:
            self.button = screen.blit(self.button_pressed, self.position_button)
        # рисуем нашу полоску
        self.strip = screen.blit(self.strip_color, self.strip_position)
        # вставлям текст который рандомно выбради из списка
        txt = self.button_words
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 60)
        res = font.render(txt, True, (255, 255, 255))
        screen.blit(res, self.position_inscription)

    def draw_background(self, screen):
        # проверка на то, разминирован муль или нет
        if self.isdefused:
            # если да, меняем модуль с красной кнопкой
            # на модуль с синей кнопкой
            screen.blit(self.module_img_off, (self.x, self.y))
        else:
            screen.blit(self.module_img_on, (self.x, self.y))

    def generate(self):
        # позиции относительно модуля
        self.position_button = [self.x + 54, self.y + 99]
        self.position_inscription = [self.x + 50, self.y + 32]
        self.strip_position = [self.x + 240, self.y + 135]
        # задаем рандомный цвет кнопки и загружаем картинку
        self.button_color = choice(COLORS_BUTTON)
        self.button_default = load_image(
            f"Bomb/BigButton_module/button_default/BigButton_default_{self.button_color}.png")
        self.button_pressed = load_image(
            f"Bomb/BigButton_module/button_pressed/BigButton_pressed_{self.button_color}.png")
        # вначале полоса должна быть черной
        # поэтому явно задаем цвет
        self.strip_color = 'black'
        self.strip_color = load_image(f'Bomb/BigButton_module/BigButton_strip_{self.strip_color}.png')
        # выбираем рандомное слова из списка
        self.button_words = choice(WORDS)

    def LKM_down(self, x, y):
        # кнопка нажата
        self.click = True
        # если модуль разминирован, то будет менятся только картинка нажатия на кнопку
        if self.isdefused:
            return
        self.time = pygame.time.get_ticks()
        # проверка на 2, 4 и 6 условия из инструкции
        # тк при этих условиях на кнопку надо быстро нажать
        # и нам не надо менять полоску при зажатии
        if self.button.collidepoint((x, y)) and self.module_img != self.module_img_off:
            if self.button_words == 'boom':
                pass
            elif self.BATTERY_COUNT > 2 and \
                    self.INDICATORS_COUNT[0] is False and \
                    self.INDICATORS_COUNT[1] is True:
                pass
            elif self.button_color == 'red' and self.button_words == 'hold':
                pass
            # если же условия 1, 3, 5 и 7
            # значит нам надо поменять полоску рядом с кнопкой на рандомный цвет из списка
            else:
                self.strip_color = choice(COLORS_STRIP)
                self.c = self.strip_color
                self.strip_color = load_image(f'Bomb/BigButton_module/BigButton_strip_{self.strip_color}.png')

    def LKM_up(self, x, y):
        # кнопку отпустили
        self.click = False
        # если модуль разминирован, то будет менятся только картинка нажатия на кнопку
        if self.isdefused:
            return
        digits = ''
        if_hold = False
        # тут мы считываем время с счетчика
        current_time = self.bomb.gs.time
        # время в кс, поэтому для секунд делим на 30 (300 секунд = 30 кадров в секунду)
        # (это 9000 - 5 минут) поэтому делим на 30 для секунд
        # для получения минут делим на 60
        minuts = round((current_time / 30) // 60)
        # для получения секунд берем остаток от деления на 60
        sec = (current_time / 30) % 60
        # в строку запсываем все цифры, которые у нас на таймере
        # (это надо для проверки условий разминирования)
        sec = int(sec)
        digits += str(minuts)
        digits += str(sec)
        # если кнопка не нажата, меняем полосу на черную
        self.strip_color = 'black'
        self.strip_color = load_image(f'Bomb/BigButton_module/BigButton_strip_{self.strip_color}.png')
        # сколько сек мы удерживали кнопку
        self.self_time_release = pygame.time.get_ticks()
        # время в мс для удобства
        time1 = (self.self_time_release - self.time) / 100
        # Проверка на нажатие по кнопкам
        if self.button.collidepoint((x, y)) and self.module_img != self.module_img_off:
            # 1 условие
            # если 1 условие меняем переменную if_hold
            # мы снизу будем проверять эти условия для оптимизации
            if self.button_color == 'blue' and self.button_words == 'break':
                if_hold = True
            # 2 условие
            elif self.button_words == 'boom':
                # проверяем быстроту клика
                # если быстрый то модуль разминирован
                if time1 <= 1.5:
                    # print('you win')
                    self.isdefused = True
                else:
                    # если нет, то добавляем к ошибкам + 1
                    # print('fail')
                    self.bomb.gs.mistakes += 1
                    # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
            # 3 условие
            elif self.button_color == 'green' and \
                    self.INDICATORS_COUNT[0] is True and \
                    self.INDICATORS_COUNT[1] is False:
                if_hold = True
            # 4 условие
            elif self.BATTERY_COUNT > 2 and \
                    self.INDICATORS_COUNT[0] is False and \
                    self.INDICATORS_COUNT[1] is True:
                if time1 <= 1.5:
                    # print('you win')
                    self.isdefused = True
                else:
                    # print('fail')
                    self.bomb.gs.mistakes += 1
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
            # 5 условие
            elif self.button_color == 'yellow':
                if_hold = True
            # 6 условие
            elif self.button_color == 'red' and self.button_words == 'hold':
                if time1 <= 1.5:
                    # print('you win')
                    self.isdefused = True
                else:
                    # print('fail')
                    self.bomb.gs.mistakes += 1
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
            # 7 усоовие(все другие случаи)
            else:
                if_hold = True
            # если для разминирования, кнопка должна удерживаться
            if if_hold:
                # то мы считываем цвет полосы справа от кнопки
                # взависимости от цвета, сверяем с нашим таймером цифры
                if self.c == 'blue':
                    # например если полоска синего цвета, то надо отпустить кнопку,
                    # когда любая цифра обратного таймера будет равна 4
                    # в digits у нас все цифры которые были на таймере, в момент когда игрок
                    # отпустил кнопку
                    if '4' in digits:
                        # мы смотрим, есть ли в этох цифрах 4
                        # print('win')
                        self.isdefused = True
                    else:
                        # print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()
                elif self.c == 'white':
                    if '1' in digits:
                        # print('win')
                        self.isdefused = True
                    else:
                        # print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()
                elif self.c == 'yellow':
                    if '5' in digits:
                        # print('win')
                        self.isdefused = True
                    else:
                        # print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()
                elif self.c == 'violet':
                    if '1' in digits:
                        # print('win')
                        self.isdefused = True
                    else:
                        # print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()


COLORS_BUTTON = ['red', 'yellow', 'green', 'blue']
COLORS_STRIP = ['blue', 'violet', 'white', 'yellow']
WORDS = ['break', 'boom', 'hold']
