import random
from random import choice

import pygame
from CONSTANTS import DIGITS, PLUS_MINUS, DIVIDE_MULTIPLY, SYMBOLS, DIGITS_FOR_LAST_DIGIT
from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image


class AhmedModule(BobmModule):
    """Моудуль Ахмеда"""

    def init(self):
        # множество для чисел
        self.list_digits = set()
        # шрифт
        self.font22 = pygame.font.Font(r'Resources/Pixeboy.ttf', 22)
        self.font60 = pygame.font.Font(r'Resources/Pixeboy.ttf', 60)
        # переменная для подходящего условия
        self.what_conditional = 0

        self.isdefused = False
        self.click = False
        # кол-во батареек на бомбе
        self.BATTERY_COUNT = self.bomb.batteries
        # какой индикатор горит
        self.INDICATORS_COUNT = self.bomb.indicators
        self.module_img_off = load_image(r"Bomb/Ahmed_module/ahmed_module_off.png")
        self.module_img_on = load_image(r"Bomb/Ahmed_module/ahmed_module_on.png")
        self.module_img = self.module_img_on
        # переходим в функцию для рисования книпки, слов, полосок
        self.generate_example()
        return self

    def draw(self, screen):
        # отрисовываем сам модуль
        self.draw_background(screen)

        self.first_btn_rect = screen.blit(self.first_btn, self.position_btn[0])
        self.second_btn_rect = screen.blit(self.second_btn, self.position_btn[1])
        self.third_btn_rect = screen.blit(self.third_btn, self.position_btn[2])
        self.fourth_btn_rect = screen.blit(self.fourth_btn, self.position_btn[3])
        self.fifth_btn_rect = screen.blit(self.fifth_btn, self.position_btn[4])
        self.sixth_btn_rect = screen.blit(self.sixth_btn, self.position_btn[5])
        self.seventh_btn_rect = screen.blit(self.seventh_btn, self.position_btn[6])
        self.eighth_btn_rect = screen.blit(self.eighth_btn, self.position_btn[7])
        self.ninth_btn_rect = screen.blit(self.ninth_btn, self.position_btn[8])

        # рисуем сам пример
        txt = self.math_example
        res = self.font60.render(txt, True, (255, 255, 255))
        screen.blit(res, self.position_example)

        count = 0
        for el in self.random_position_for_digits:
            txt = str(el)
            res = self.font22.render(txt, True, (255, 255, 255))
            screen.blit(res, self.position_answers[count])
            count += 1

    def check_conditional(self):
        self.what_conditional = 0
        b = False
        # проверяем условия
        serial_num = self.bomb.serial_number
        symb = list(serial_num[0] + serial_num[2])
        if self.BATTERY_COUNT == 3:
            self.what_conditional = 1
            self.right_answer = self.conditional_one
        elif self.INDICATORS_COUNT[0] and not self.INDICATORS_COUNT[1]:
            self.what_conditional = 2
            self.right_answer = self.conditional_two
        elif self.INDICATORS_COUNT[1] and not self.INDICATORS_COUNT[0] and self.BATTERY_COUNT == 1:
            self.what_conditional = 3
            self.right_answer = self.conditional_three
        elif self.what_conditional == 0:
            for s in SYMBOLS:
                if s in symb:
                    b = True
                    self.what_conditional = 5
                    self.right_answer = self.conditional_five
                    break
            if not b:
                self.what_conditional = 4
                self.right_answer = self.conditional_four
        else:
            self.what_conditional = 5
            self.right_answer = self.conditional_five
        if self.right_answer not in self.random_position_for_digits:
            self.random_position_for_digits.pop(-1)
            self.random_position_for_digits.append(self.right_answer)

    def draw_background(self, screen):
        # проверка на то, разминирован модуль или нет
        if self.isdefused:
            # если да, меняем модуль с красной кнопкой
            # на модуль с синей кнопкой
            screen.blit(self.module_img_off, (self.x, self.y))
        else:
            screen.blit(self.module_img_on, (self.x, self.y))

    def generate_example(self):
        # рандомно выбираем цифры
        self.first_digit = choice(DIGITS)
        self.second_digit = choice(DIGITS)
        self.third_digit = choice(DIGITS_FOR_LAST_DIGIT)

        # рандомно выбираем символы
        self.first_operation = choice(PLUS_MINUS)
        self.second_operation = choice(DIVIDE_MULTIPLY)
        self.generate()

    def generate(self):
        # собираем пример для вывода на экран
        # генерируем 'случайные' цифры
        self.math_example = f'{self.first_digit} {self.first_operation} {self.second_digit}' \
                            f'{self.second_operation} {self.third_digit} '
        if int(eval(self.math_example)) == eval(self.math_example):
            self.math_example_1 = int(eval(self.math_example))
        else:
            while int(eval(self.math_example)) != eval(self.math_example) or \
                    (self.first_digit == 1 and self.second_digit == 1 and self.third_digit == 1):
                self.generate_example()
        self.math_example_1 = eval(self.math_example)
        self.math_example = f'{self.first_digit} {self.first_operation} {self.second_digit}' \
                            f' {self.second_operation} {self.third_digit} '
        self.math_example_1 = int(eval(self.math_example))

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.math_example_1)

        # первое условие
        if self.first_operation == '+':
            self.conditional_one = f'{self.first_digit} - {self.second_digit}' \
                                   f' {self.second_operation} {self.third_digit} '
        else:
            self.conditional_one = f'{self.first_digit} + {self.second_digit}' \
                                   f' {self.second_operation} {self.third_digit} '
        self.conditional_one = eval(self.conditional_one)
        if self.conditional_one != int(self.conditional_one):
            self.conditional_one = round(self.conditional_one, 1)
        else:
            self.conditional_one = int(self.conditional_one)

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.conditional_one)

        # второе условие
        if self.second_operation == '*':
            self.conditional_two = f'{self.first_digit} {self.first_operation} {self.second_digit}' \
                                   f' / {self.third_digit} '
        else:
            self.conditional_two = f'{self.first_digit} {self.first_operation} {self.second_digit}' \
                                   f' * {self.third_digit} '
        self.conditional_two = eval(self.conditional_two)
        if self.conditional_two != int(self.conditional_two):
            self.conditional_two = round(self.conditional_two, 1)
        else:
            self.conditional_two = int(self.conditional_two)

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.conditional_two)

        # третье условие
        self.conditional_three = f'{self.first_digit} {self.first_operation} {self.second_digit}' \
                                 f' {self.second_operation} 10 '
        self.conditional_three = eval(self.conditional_three)
        if self.conditional_three != int(self.conditional_three):
            self.conditional_three = round(self.conditional_three, 1)
        else:
            self.conditional_three = int(self.conditional_three)

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.conditional_three)

        # четвертое условие
        self.conditional_four = f'0 {self.first_operation} {self.second_digit}' \
                                f' {self.second_operation} {self.third_digit} '
        self.conditional_four = eval(self.conditional_four)
        if self.conditional_four != int(self.conditional_four):
            self.conditional_four = round(self.conditional_four, 1)
        else:
            self.conditional_four = int(self.conditional_four)

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.conditional_four)

        # пятое условие
        self.conditional_five = f'{self.first_digit} {self.first_operation} 10' \
                                f'{self.second_operation} {self.third_digit} '
        self.conditional_five = eval(self.conditional_five)
        if self.conditional_five != int(self.conditional_five):
            self.conditional_five = round(self.conditional_five, 1)
        else:
            self.conditional_five = int(self.conditional_five)

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.conditional_five)

        # шестая кнопка
        self.six_answ = self.math_example_1 + 1
        # если у нас совпадают цифры на кнопках, то мы прибавляем к цифре на кнопке 1
        # пока число не станет уникальным
        c = 0
        if self.six_answ == self.math_example_1 or self.six_answ == self.conditional_one or \
                self.six_answ == self.conditional_two or self.six_answ == self.conditional_three or \
                self.six_answ == self.conditional_four or self.six_answ == self.conditional_five:
            while self.six_answ == self.math_example_1 or self.six_answ == self.conditional_one or \
                    self.six_answ == self.conditional_two or self.six_answ == self.conditional_three or \
                    self.six_answ == self.conditional_four or self.six_answ == self.conditional_five:
                c += 1
                self.six_answ = self.math_example_1 + c
        if self.six_answ != int(self.six_answ):
            self.six_answ = round(self.six_answ, 1)
        else:
            self.six_answ = int(self.six_answ)
        c = 0

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.six_answ)

        # седьмая кнопка
        self.seven_answ = self.conditional_four * -1
        if self.seven_answ == self.math_example_1 or self.seven_answ == self.conditional_one or \
                self.seven_answ == self.conditional_two or self.seven_answ == self.conditional_three or \
                self.seven_answ == self.conditional_four or self.seven_answ == self.conditional_five or \
                self.seven_answ == self.six_answ:
            while self.seven_answ == self.math_example_1 or self.seven_answ == self.conditional_one or \
                    self.seven_answ == self.conditional_two or self.seven_answ == self.conditional_three or \
                    self.seven_answ == self.conditional_four or self.seven_answ == self.conditional_five or \
                    self.seven_answ == self.six_answ:
                c += 1
                self.seven_answ = self.conditional_four * -c
        if self.seven_answ != int(self.seven_answ):
            self.six_answ = round(self.seven_answ, 1)
        else:
            self.seven_answ = int(self.seven_answ)
        c = 0
        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.seven_answ)

        # восьмая кнопка

        self.eight_answ = self.conditional_two - 1
        if self.eight_answ == self.math_example_1 or self.eight_answ == self.conditional_one or \
                self.eight_answ == self.conditional_two or self.eight_answ == self.conditional_three or \
                self.eight_answ == self.conditional_four or self.eight_answ == self.conditional_five or \
                self.eight_answ == self.six_answ or self.eight_answ == self.seven_answ:
            while self.eight_answ == self.math_example_1 or self.eight_answ == self.conditional_one or \
                    self.eight_answ == self.conditional_two or self.eight_answ == self.conditional_three or \
                    self.eight_answ == self.conditional_four or self.eight_answ == self.conditional_five or \
                    self.eight_answ == self.six_answ or self.eight_answ == self.seven_answ:
                c += 1
                self.eight_answ = self.conditional_two - c
        if self.eight_answ != int(self.eight_answ):
            self.eight_answ = round(self.eight_answ, 1)
        else:
            self.eight_answ = int(self.eight_answ)
        c = 0

        # добавляем в список со всеми цифрами получившееся значение
        self.list_digits.add(self.eight_answ)

        # девятая кнопка
        self.nine_answ = self.conditional_five + 1
        if self.nine_answ == self.math_example_1 or self.nine_answ == self.conditional_one or \
                self.nine_answ == self.conditional_two or self.nine_answ == self.conditional_three or \
                self.nine_answ == self.conditional_four or self.nine_answ == self.conditional_five or \
                self.nine_answ == self.six_answ or self.nine_answ == self.seven_answ or \
                self.nine_answ == self.eight_answ:
            while self.nine_answ == self.math_example_1 or self.nine_answ == self.conditional_one or \
                    self.nine_answ == self.conditional_two or self.nine_answ == self.conditional_three or \
                    self.nine_answ == self.conditional_four or self.nine_answ == self.conditional_five or \
                    self.nine_answ == self.six_answ or self.nine_answ == self.seven_answ or \
                    self.nine_answ == self.eight_answ:
                c += 1
                self.nine_answ = self.conditional_five + c
        if self.nine_answ != int(self.nine_answ):
            self.nine_answ = round(self.nine_answ, 1)
        else:
            self.nine_answ = int(self.nine_answ)

            # добавляем в список со всеми цифрами получившееся значение
            self.list_digits.add(self.nine_answ)

        # позиции относительно модуля
        self.position_btn = [
            [self.x + 69, self.y + 110],
            [self.x + 122, self.y + 110],
            [self.x + 176, self.y + 110],
            [self.x + 69, self.y + 161],
            [self.x + 122, self.y + 161],
            [self.x + 176, self.y + 161],
            [self.x + 69, self.y + 213],
            [self.x + 122, self.y + 213],
            [self.x + 176, self.y + 213],
        ]

        self.position_answers = [
            [self.x + 80, self.y + 125],
            [self.x + 132, self.y + 125],
            [self.x + 184, self.y + 125],
            [self.x + 80, self.y + 178],
            [self.x + 132, self.y + 178],
            [self.x + 184, self.y + 178],
            [self.x + 80, self.y + 231],
            [self.x + 132, self.y + 231],
            [self.x + 184, self.y + 231],
        ]

        self.position_example = [self.x + 50, self.y + 32]

        self.btn_standard = load_image("Bomb/Ahmed_module/ahmed_module_buttons_2.png")
        self.btn_hold = load_image("Bomb/Ahmed_module/ahmed_module_buttons_hold_2.png")

        self.first_btn = self.btn_standard
        self.second_btn = self.btn_standard
        self.third_btn = self.btn_standard
        self.fourth_btn = self.btn_standard
        self.fifth_btn = self.btn_standard
        self.sixth_btn = self.btn_standard
        self.seventh_btn = self.btn_standard
        self.eighth_btn = self.btn_standard
        self.ninth_btn = self.btn_standard

        # сли у нас все цифры уникальные, то перемешиваем их
        # иначе удаляем все повторяющиеся элементы и добавляем рандомные
        self.list_digits = set(self.list_digits)
        if len(self.list_digits) == 9:
            self.random_position_for_digits = random.sample(self.list_digits, 9)
        else:
            while len(self.list_digits) < 9:
                self.list_digits.add(random.randint(min(self.list_digits), max(self.list_digits)))
        self.random_position_for_digits = random.sample(self.list_digits, 9)

        self.check_conditional()

    def LKM_down(self, x, y):
        # индекс позиции правильного элемента в списке
        ind = self.random_position_for_digits.index(self.right_answer)
        # кнопка нажата
        # проверка на нажатие по кнопкам
        if self.first_btn_rect.collidepoint((x, y)):
            self.first_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 1:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.second_btn_rect.collidepoint((x, y)):
            self.second_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 1:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.third_btn_rect.collidepoint((x, y)):
            self.third_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 2:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.fourth_btn_rect.collidepoint((x, y)):
            self.fourth_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 3:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.fifth_btn_rect.collidepoint((x, y)):
            self.fifth_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 4:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.sixth_btn_rect.collidepoint((x, y)):
            self.sixth_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 5:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.seventh_btn_rect.collidepoint((x, y)):
            self.seventh_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 6:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.eighth_btn_rect.collidepoint((x, y)):
            self.eighth_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 7:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.ninth_btn_rect.collidepoint((x, y)):
            self.ninth_btn = self.btn_hold
            # если индекс кнопки верный, то модуль обезвржен
            if ind == 8:
                self.isdefused = True
            else:
                # если нет, то добавляем к ошибкам + 1
                # print('fail')
                self.bomb.gs.mistakes += 1
                # проверяем, если мы допустили >= 3 ошибки, тогда игра заканчивается
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

    def LKM_up(self, x, y):
        self.first_btn = self.btn_standard
        self.second_btn = self.btn_standard
        self.third_btn = self.btn_standard
        self.fourth_btn = self.btn_standard
        self.fifth_btn = self.btn_standard
        self.sixth_btn = self.btn_standard
        self.seventh_btn = self.btn_standard
        self.eighth_btn = self.btn_standard
        self.ninth_btn = self.btn_standard
