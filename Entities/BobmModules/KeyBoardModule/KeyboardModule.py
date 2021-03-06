import random

from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image


class KeyboardModule(BobmModule):
    """Модуль бомбы с символами (клавиатура)"""

    def init(self):
        self.isdefused = False
        self.blocks_defused = 0
        self.module_img_off = load_image(r"Bomb/keyboard_module/keyboard_background_off.png")
        self.module_img_on = load_image(r"Bomb/keyboard_module/keyboard_background_on.png")
        self.module_img = self.module_img_on
        self.choose_set()
        self.generate()
        return self

    def choose_set(self):
        self.image_set = random.randint(1, 6)  # Выбор группы с картинками
        image_numbers = [1, 2, 3, 4, 5, 6, 7]
        # Выбираем из серии 4 изображения (изображения имеют названия от 1 до 7)
        random.shuffle(image_numbers)
        self.img_1 = image_numbers.pop()
        random.shuffle(image_numbers)
        self.img_2 = image_numbers.pop()
        random.shuffle(image_numbers)
        self.img_3 = image_numbers.pop()
        random.shuffle(image_numbers)
        self.img_4 = image_numbers.pop()

        # Обезвреживать необходимо кнопки с наименьшим числом
        self.answer = sorted([self.img_1, self.img_2, self.img_3, self.img_4])

    def generate(self):
        # Цифры - положение кнопки относительно модуля
        self.position_btn = [
            [self.x + 75, self.y + 95],
            [self.x + 155, self.y + 95],
            [self.x + 75, self.y + 175],
            [self.x + 155, self.y + 175],
        ]
        # Цифры - положение изображения на кнопке относительно модуля
        self.position_btn_img = [
            [self.x + 85, self.y + 105],
            [self.x + 165, self.y + 105],
            [self.x + 85, self.y + 185],
            [self.x + 165, self.y + 185],
        ]

        self.btn_standard = load_image("Bomb/keyboard_module/key_standard.png").convert()
        self.btn_correct = load_image("Bomb/keyboard_module/key_correct.png").convert()
        self.btn_mistake = load_image("Bomb/keyboard_module/key_mistake.png").convert()

        """ img_1, first_btn, first_btn_img взаимосвязаны 
        img_1 - показывает номер картинки которая загружается в first_btn_img, 
        а так же отвечает за изменения бэкграунда, то есть first_btn на ошибочный (btn_mistake) """
        self.first_btn = self.btn_standard
        self.second_btn = self.btn_standard
        self.third_btn = self.btn_standard
        self.fourth_btn = self.btn_standard

        # Словарь: номер кнопки — сколько кадров она показывала ошибку
        self.is_mistake = {
            "1": None,
            "2": None,
            "3": None,
            "4": None,
        }

        # Загрузка картинок на кнопках
        self.first_btn_img = load_image(f"Bomb/keyboard_module/{self.image_set} set/{self.img_1}.png")
        self.second_btn_img = load_image(f"Bomb/keyboard_module/{self.image_set} set/{self.img_2}.png")
        self.third_btn_img = load_image(f"Bomb/keyboard_module/{self.image_set} set/{self.img_3}.png")
        self.fourth_btn_img = load_image(f"Bomb/keyboard_module/{self.image_set} set/{self.img_4}.png")

    def draw(self, screen):
        screen.blit(self.module_img, (self.x, self.y))

        self.first_btn_rect = screen.blit(self.first_btn, self.position_btn[0])
        self.second_btn_rect = screen.blit(self.second_btn, self.position_btn[1])
        self.third_btn_rect = screen.blit(self.third_btn, self.position_btn[2])
        self.fourth_btn_rect = screen.blit(self.fourth_btn, self.position_btn[3])

        screen.blit(self.first_btn_img, self.position_btn_img[0])
        screen.blit(self.second_btn_img, self.position_btn_img[1])
        screen.blit(self.third_btn_img, self.position_btn_img[2])
        screen.blit(self.fourth_btn_img, self.position_btn_img[3])

    def update(self):
        if self.blocks_defused == 4:
            self.module_img = self.module_img_off
            self.isdefused = True

        # Возврат кнопки с ошибкой в нейтральное состояние
        for num, time in self.is_mistake.items():
            if time is not None:
                self.is_mistake[num] += 1
            if time == 75:
                if num == "1":
                    if self.first_btn != self.btn_correct:
                        self.first_btn = self.btn_standard
                elif num == "2":
                    if self.second_btn != self.btn_correct:
                        self.second_btn = self.btn_standard
                elif num == "3":
                    if self.third_btn != self.btn_correct:
                        self.third_btn = self.btn_standard
                elif num == "4":
                    if self.fourth_btn != self.btn_correct:
                        self.fourth_btn = self.btn_standard
                self.is_mistake[num] = None

    def LKM_down(self, x, y):
        # Проверка на нажатие по кнопкам
        if self.first_btn_rect.collidepoint((x, y)) and self.first_btn != self.btn_correct:
            if self.answer[0] == self.img_1:
                # Если нажатие верное
                self.blocks_defused += 1
                self.first_btn = self.btn_correct
                del self.answer[0]
            else:
                self.first_btn = self.btn_mistake
                self.is_mistake["1"] = 0
                self.bomb.gs.mistakes += 1
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.second_btn_rect.collidepoint((x, y)) and self.second_btn != self.btn_correct:
            if self.answer[0] == self.img_2:
                self.blocks_defused += 1
                self.second_btn = self.btn_correct
                del self.answer[0]
            else:
                self.second_btn = self.btn_mistake
                self.is_mistake["2"] = 0
                self.bomb.gs.mistakes += 1
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.third_btn_rect.collidepoint((x, y)) and self.third_btn != self.btn_correct:
            if self.answer[0] == self.img_3:
                self.blocks_defused += 1
                self.third_btn = self.btn_correct
                del self.answer[0]
            else:
                self.third_btn = self.btn_mistake
                self.is_mistake["3"] = 0
                self.bomb.gs.mistakes += 1
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()

        elif self.fourth_btn_rect.collidepoint((x, y)) and self.fourth_btn != self.btn_correct:
            if self.answer[0] == self.img_4:
                self.blocks_defused += 1
                self.fourth_btn = self.btn_correct
                del self.answer[0]
            else:
                self.fourth_btn = self.btn_mistake
                self.is_mistake["4"] = 0
                self.bomb.gs.mistakes += 1
                if self.bomb.gs.mistakes >= 3:
                    self.bomb.gs.lose()
