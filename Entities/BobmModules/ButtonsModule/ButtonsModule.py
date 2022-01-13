# from typing_extensions import ParamSpecKwargs
import pygame
from random import shuffle
from image_loader import load_image
from Entities.BobmModules.BobmModule import BobmModule
from Entities.BobmModules.ButtonsModule.Button import Button
from CONSTANTS import SYMBOLS, TRANSLATE, COLORS, FPS


class ButtonsModule(BobmModule):
    """Модуль бомбы с 4 кнопками"""

    def init(self):
        self.isdefused = False
        self.correct_answer, self.info = self.generate()  # info - все цвета
        # Анимация
        self.show = [self.info[0]]  # show - все цвета которые показываем сейчас
        # self.info[0] - текущий цвет кнопки; -1 - таймер до смены на другую кнопк; False - светится/не светится
        self.button_now = [self.info[0], 30, False]
        self.step = 0
        # Логика
        self.correct_answers = 0  # Количество полных правильных оветов
        self.answer_step = 1  # Текущий ответ (отсчёт с 1)
        self.answer = []  # Ответ игрока на текущей стадии
        # Картиночки и цыганская магия x2
        path = lambda p: f"Bomb/Buttons_module/{p}.png"
        image = lambda p: load_image(path(p)).convert()  # Так красивше
        self.module_img_red_on = image("module_red_on")
        self.module_img_gray_on = image("module_gray_on")
        self.module_img_green_on = image("module_green_on")
        self.module_img_gray_off = image("module_gray_off")
        # Создание спрайтов
        # Циферки взяты с картинки
        positions = [
            [self.x + 80, self.y + 80],
            [self.x + 160, self.y + 80],
            [self.x + 80, self.y + 160],
            [self.x + 160, self.y + 160],
        ]
        self.buttons = {}
        self.btn_group = pygame.sprite.Group()
        for pos, color in zip(positions, COLORS):
            self.buttons[color] = Button(self.btn_group, color, pos)
        # Анимация реакции модуля на нажатие
        self.module_img_red_timer = 0
        self.module_img_green_timer = 0
        return self

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
        print(answer)
        return answer, show

    # ------------------------------------------------------------------------------------------------------------------

    def update(self):
        # Обработка анимации
        if self.isdefused:
            for btn in self.buttons.values():
                btn.change_image(islightning=False)
        elif self.button_now[1] > 0:
            self.button_now[1] -= 1
        else:
            if self.button_now[2]:
                self.buttons[self.button_now[0]].change_image(islightning=False)
                self.step = (self.step + 1) % len(self.show)
                self.button_now = [self.show[self.step], (1 * FPS) - 1, False]
            else:
                self.button_now = [self.show[self.step], (1 * FPS) - 1, True]
                self.buttons[self.button_now[0]].change_image(islightning=True)

    # ------------------------------------------------------------------------------------------------------------------

    def draw(self, screen):
        self.draw_module(screen)
        self.draw_buttons(screen)

    def draw_module(self, screen):
        if self.isdefused:
            screen.blit(self.module_img_gray_off, (self.x, self.y))
        elif self.module_img_green_timer > 0:  # Анимация верного ответа
            screen.blit(self.module_img_green_on, (self.x, self.y))
            self.module_img_green_timer -= 1
        elif self.module_img_red_timer > 0:  # Анимация неверного ответа
            screen.blit(self.module_img_red_on, (self.x, self.y))
            self.module_img_red_timer -= 1
        else:
            screen.blit(self.module_img_gray_on, (self.x, self.y))

    def draw_buttons(self, screen):
        self.btn_group.draw(screen)

    # ------------------------------------------------------------------------------------------------------------------

    def LKM_down(self, x, y):
        # Получаем ответ
        answer = "on module"
        
        for btn in self.buttons.values():
            if btn.check_click(x, y):
                answer = btn.color
                break

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
                    # Сброс
                    self.answer = []
                    self.answer_step = 1
                    self.correct_answers = 0
                    self.bomb.gs.mistakes += 1
                    if self.bomb.gs.mistakes >= 3:
                        self.bomb.gs.lose()
                    self.module_img_red_timer += FPS // 2
                    self.show = self.info[: self.correct_answers + 1]
                    return
            else:
                if len(self.answer) == 4:  # 4 - длина полного правильного ответа
                    self.isdefused = True
                elif len(self.answer) == self.correct_answers + 1:
                    # Следующий этап разминирования
                    self.answer = []
                    self.correct_answers += 1
                    self.answer_step = 1
                else:
                    # Следующий этап разминирования текущего этапа
                    self.answer_step += 1
                # Общие действия при правильном ответе
                self.module_img_green_timer += (
                    FPS // 2
                )  # Использую деление тк умножение может давать не целые числа
                self.show = self.info[: self.correct_answers + 1]
