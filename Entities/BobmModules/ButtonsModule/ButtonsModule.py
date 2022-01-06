import pygame
from random import choice, shuffle
from image_loader import load_image
from Entities.BobmModules.BobmModule import BobmModule
from CONSTANTS import SYMBOLS, TRANSLATE, COLORS, FPS


class ButtonsModule(BobmModule):
    """Модуль бомбы с 4 кнопками"""

    def init(self):
        self.isdefused = False
        self.correct_answer, self.info = self.generate()  # info - все цвета
        # Анимация
        self.show = [self.info[0]]  # show - все цвета которые показываем сейчас
        self.button_now = [self.info[0], 30, None]  # 0 - номер кнопки, 30 - таймер
        self.step = 0
        # Логика
        self.correct_answers = 0  # Количество полных правильных оветов
        self.answer_step = 1  # Текущий ответ (отсчёт с 1)
        self.answer = []  # Отивет игрока на текущей стадии
        # Картиночки и цыганская магия x2
        path = lambda p: f"Bomb/Buttons_module/{p}.png"
        image = lambda p: load_image(path(p)).convert()  # Так красивше
        self.module_img_red_on = image("module_red_on")
        self.module_img_gray_on = image("module_gray_on")
        self.module_img_green_on = image("module_green_on")
        self.module_img_gray_off = image("module_gray_off")
        self.button_img_red = image("button_red")
        self.button_img_blue = image("button_blue")
        self.button_img_green = image("button_green")
        self.button_img_yellow = image("button_yellow")
        # Циферки взяты с картинки
        self.button_red_x, self.button_red_y = self.x + 80, self.y + 80
        self.button_blue_x, self.button_blue_y = self.x + 160, self.y + 80
        self.button_green_x, self.button_green_y = self.x + 80, self.y + 160
        self.button_yellow_x, self.button_yellow_y = self.x + 160, self.y + 160
        # Анимация нажатия
        self.module_img_red_on_timer = 0
        self.module_img_green_on_timer = 0
        return self

    def draw(self, screen):
        self.draw_module(screen)
        self.draw_buttons(screen)

    def draw_module(self, screen):
        if self.isdefused:
            screen.blit(self.module_img_gray_off, (self.x, self.y))
        elif self.module_img_green_on_timer > 0:  # Анимация верного ответа
            screen.blit(self.module_img_green_on, (self.x, self.y))
            self.module_img_green_on_timer -= 1
        elif self.module_img_red_on_timer > 0:  # Анимация неверного ответа
            screen.blit(self.module_img_red_on, (self.x, self.y))
            self.module_img_red_on_timer -= 1
        else:
            screen.blit(self.module_img_gray_on, (self.x, self.y))

    def draw_buttons(self, screen):
        if self.button_now[2] == "pause" or self.isdefused:
            self.button_now[1] -= 1
            # fmt: off
            screen.blit(self.button_img_red, (self.button_red_x, self.button_red_y))
            screen.blit(self.button_img_blue, (self.button_blue_x, self.button_blue_y))
            screen.blit(self.button_img_green, (self.button_green_x, self.button_green_y))
            screen.blit(self.button_img_yellow, (self.button_yellow_x, self.button_yellow_y))
            # fmt: on
            if self.button_now[1] <= 0:
                self.button_now[1] = 30
                self.button_now[2] = None  # Выкл паузу
        else:
            if self.button_now[1] <= 0:
                self.step = (self.step + 1) % len(self.show)
                self.button_now = [self.show[self.step], 30, "pause"]
                self.draw_buttons(screen)
            # fmt: off
            if self.button_now[0] != "r":
                screen.blit(self.button_img_red, (self.button_red_x, self.button_red_y))
            if self.button_now[0] != "b":
                screen.blit(self.button_img_blue, (self.button_blue_x, self.button_blue_y))
            if self.button_now[0] != "g":
                screen.blit(self.button_img_green, (self.button_green_x, self.button_green_y))
            if self.button_now[0] != "y":
                screen.blit(self.button_img_yellow, (self.button_yellow_x, self.button_yellow_y))
            self.button_now[1] -= 1
            # fmt: on

    def generate(self):
        # Выбираем перевод
        serial_num = self.bomb.serial_number
        symb = list(serial_num[0] + serial_num[2])
        translate = None
        for s in SYMBOLS:
            if s in symb:
                translate = TRANSLATE[0]
        else:
            translate = TRANSLATE[1]
        # Создаём последовательность
        show = COLORS[:]
        shuffle(show)
        # Находим для неё ответ
        answer = []
        for trans in translate:
            answ = []
            for color in show:
                answ.append(trans[color])
            answer.append(answ)
        return answer, show

    def LKM_down(self, x, y):
        # Получаем ответ
        answer = "on module"
        # Циферки взяты с картинки
        if (
            self.button_red_x <= x <= self.x + 135
            and self.button_red_y <= y <= self.y + 135
        ):
            answer = "r"
        elif (
            self.button_blue_x <= x <= self.x + 215
            and self.button_blue_y <= y <= self.y + 135
        ):
            answer = "b"
        elif (
            self.button_green_x <= x <= self.x + 135
            and self.button_green_y <= y <= self.y + 215
        ):
            answer = "g"
        elif (
            self.button_yellow_x <= x <= self.x + 215
            and self.button_yellow_y <= y <= self.y + 215
        ):
            answer = "y"

        # Проверяем ответ
        if answer == "on module":
            return
        else:
            self.answer.append(answer)
            correct_answer = self.correct_answer[self.bomb.gs.mistakes][
                : self.correct_answers + 1
            ]
            for i in range(self.answer_step):
                if correct_answer[i] != self.answer[i]:
                    self.answer = []
                    self.answer_step = 1
                    self.correct_answers = 0
                    self.bomb.gs.mistakes += 1
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
                    self.module_img_red_on_timer += FPS // 2
                    self.show = self.info[: self.correct_answers + 1]
                    return
            else:
                if len(self.answer) == 4:  # 4 - длина полного правильного ответа
                    self.isdefused = True
                elif len(self.answer) == self.correct_answers + 1:
                    self.answer = []
                    self.correct_answers += 1
                    self.answer_step = 1
                else:
                    self.answer_step += 1
                self.module_img_green_on_timer += FPS // 2
                self.show = self.info[: self.correct_answers + 1]
