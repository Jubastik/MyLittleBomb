from random import choice

import pygame

from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image


class BigButtonModule(BobmModule):
    """Моудуль бомбы с большой кнопкой"""

    def init(self):
        self.isdefused = False
        self.click = False
        self.BATTERY_COUNT = self.bomb.batteries
        self.INDICATORS_COUNT = self.bomb.indicators
        self.module_img_off = load_image(r"Bomb/BigButton_module/BigButton_module_img_off.png").convert()
        self.module_img_on = load_image(r"Bomb/BigButton_module/BigButton_module_img_on.png").convert()
        self.module_img = self.module_img_on
        self.generate()
        return self

    def draw(self, screen):
        self.draw_background(screen)
        if not self.click:
            self.button = screen.blit(self.button_default, self.position_button)
        if self.click:
            self.button = screen.blit(self.button_pressed, self.position_button)
        self.strip = screen.blit(self.strip_color, self.strip_position)
        txt = self.button_words
        font = pygame.font.Font(r'Resources/Pixeboy.ttf', 60)
        res = font.render(txt, True, (255, 255, 255))
        screen.blit(res, self.position_inscription)

    def draw_background(self, screen):
        if self.isdefused:
            screen.blit(self.module_img_off, (self.x, self.y))

        else:
            screen.blit(self.module_img_on, (self.x, self.y))

    def generate(self):
        self.position_button = [self.x + 54, self.y + 99]
        self.position_inscription = [self.x + 50, self.y + 32]
        self.strip_position = [self.x + 240, self.y + 135]
        self.button_color = choice(COLORS_BUTTON)
        self.strip_color = 'black'
        self.strip_color = load_image(f'Bomb/BigButton_module/BigButton_strip_{self.strip_color}.png').convert()
        self.button_default = load_image(
            f"Bomb/BigButton_module/button_default/BigButton_default_{self.button_color}.png").convert()
        self.button_pressed = load_image(
            f"Bomb/BigButton_module/button_pressed/BigButton_pressed_{self.button_color}.png").convert()
        self.button_words = choice(WORDS)

    def LKM_down(self, x, y):
        self.click = True
        if self.isdefused:
            return
        self.time = pygame.time.get_ticks()
        if self.button.collidepoint((x, y)) and self.module_img != self.module_img_off:
            if self.button_words == 'boom':
                pass
            elif self.BATTERY_COUNT > 2 and \
                    self.INDICATORS_COUNT[0] is False and \
                    self.INDICATORS_COUNT[1] is True:
                pass
            elif self.button_color == 'red' and self.button_words == 'hold':
                pass
            else:
                self.strip_color = choice(COLORS_STRIP)
                self.c = self.strip_color
                self.strip_color = load_image(f'Bomb/BigButton_module/BigButton_strip_{self.strip_color}.png')

    def LKM_up(self, x, y):
        self.click = False
        if self.isdefused:
            return
        digits = ''
        if_hold = False
        current_time = self.bomb.gs.time
        minuts = round((current_time / 30) // 60)
        sec = (current_time / 30) % 60
        sec = int(sec)
        digits += str(minuts)
        digits += str(sec)
        self.strip_color = 'black'
        self.strip_color = load_image(f'Bomb/BigButton_module/BigButton_strip_{self.strip_color}.png')
        self.self_time_release = pygame.time.get_ticks()
        time = (self.self_time_release - self.time) / 1000
        time1 = (self.self_time_release - self.time) / 100
        # Проверка на нажатие по кнопкам
        if self.button.collidepoint((x, y)) and self.module_img != self.module_img_off:
            if self.button_color == 'blue' and self.button_words == 'break':
                if_hold = True
            elif self.button_words == 'boom':
                if time1 <= 1.5:
                    print('you win')
                    self.isdefused = True
                else:
                    print('fail')
                    self.bomb.gs.mistakes += 1
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
            elif self.button_color == 'green' and \
                    self.INDICATORS_COUNT[0] is True and \
                    self.INDICATORS_COUNT[1] is False:
                if_hold = True
            elif self.BATTERY_COUNT > 2 and \
                    self.INDICATORS_COUNT[0] is False and \
                    self.INDICATORS_COUNT[1] is True:
                if time1 <= 1.5:
                    print('you win')
                    self.isdefused = True
                else:
                    print('fail')
                    self.bomb.gs.mistakes += 1
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
            elif self.button_color == 'yellow':
                if_hold = True
            elif self.button_color == 'red' and self.button_words == 'hold':
                if time1 <= 1.5:
                    print('you win')
                    self.isdefused = True
                else:
                    print('fail')
                    self.bomb.gs.mistakes += 1
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
            else:
                if_hold = True
            if if_hold:
                if self.c == 'blue':
                    if '4' in digits:
                        print('win')
                        self.isdefused = True
                    else:
                        print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()
                elif self.c == 'white':
                    if '1' in digits:
                        print('win')
                        self.isdefused = True
                    else:
                        print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()
                elif self.c == 'yellow':
                    if '5' in digits:
                        print('win')
                        self.isdefused = True
                    else:
                        print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()
                elif self.c == 'violet':
                    if '1' in digits:
                        print('win')
                        self.isdefused = True
                    else:
                        print('fail')
                        self.bomb.gs.mistakes += 1
                        if self.bomb.gs.mistakes >= 3:
                            self.bomb.gs.lose()


COLORS_BUTTON = ['red', 'yellow', 'green', 'blue']
COLORS_STRIP = ['blue', 'violet', 'white', 'yellow']
WORDS = ['break', 'boom', 'hold']
