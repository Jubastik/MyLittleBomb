import pygame
from random import randint, choice
from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image


class WiresModule(BobmModule):
    """Модуль бомбы с проводами"""

    def init(self):
        self.isdefused = False
        self.module_img_off = load_image(r"Bomb\wires_module\wiremodule_off.png")
        self.module_img_on = load_image(r"Bomb\wires_module\wiremodule_off.png")
        self.wires, self.answer = self.generate()
        return self

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_wires(screen)

    def draw_background(self, screen):
        if self.isdefused:
            screen.blit(self.module_img_off, (self.x, self.y))
        else:
            screen.blit(self.module_img_on, (self.x, self.y))

    def draw_wires(self, screen):
        for wire in self.wires:
            wire.draw(screen)

    def generate(self):
        # Расчёт координат проводов
        # WH провода: 175x25
        # Цифры - положение провода относительно модуля
        position = [
            [self.x + 60, self.y + 55],
            [self.x + 60, self.y + 95],
            [self.x + 60, self.y + 135],
            [self.x + 60, self.y + 175],
            [self.x + 60, self.y + 215],
        ]
        # Генерация бомбы
        wire_count = randint(4, 5)
        wires = []
        for i in range(wire_count):
            color = choice(COLORS)
            form = choice(FORMS)
            wire = Wire(color, form, position[i], i)
            wires.append(wire)

        # Поиск верного ответа
        answer = None
        if wire_count == 4:
            # Считаем провода по цветам
            red_count = 0
            blue_count = 0
            yellow_count = 0
            for wire in wires:
                if wire.color == "red":
                    red_count += 1
                elif wire.color == "blue":
                    blue_count += 1
                elif wire.color == "yellow":
                    yellow_count += 1

            # Проверяем по условиям
            if red_count > 1 and (int(self.bomb.serial_number[3]) % 2) == 1:
                red = None
                for wire in wires:
                    if wire.color == "red":
                        red = wire.num
            elif wires[-1].color == "yellow" and red_count == 0:
                answer = 0
            elif blue_count == 1:
                answer = 0
            elif yellow_count > 1:
                answer = 3
            else:
                answer = 1
        else:
            # Считаем провода по цветам
            red_count = 0
            blue_count = 0
            yellow_count = 0
            black_count = 0
            for wire in wires:
                if wire.color == "red":
                    red_count += 1
                elif wire.color == "blue":
                    blue_count += 1
                elif wire.color == "yellow":
                    yellow_count += 1
                elif wire.color == "black":
                    black_count += 1

            # Проверяем по условиям
            if (
                wires[-1].color == "black"
                and (int(self.bomb.serial_number[3]) % 2) == 1
            ):
                answer = 3
            elif red_count == 1 and yellow_count > 1:
                answer = 0
            elif black_count == 0:
                answer = 1
            else:
                answer = 0
        return wires, answer

    def click_LKM(self, x, y):
        # Получаем провод по которому кликнули
        answer = None
        # Проверяем
        if answer == "on module":
            pass
        elif answer == self.answer:
            self.isdefused = True        
        else:
            self.bomb.gs.mistakes += 1
            if self.bomb.gs.mistakes >= 3:
                self.bomb.gs.lose()


class Wire:
    def __init__(self, color, form, pos, num):
        self.wire_img_full = load_image(
            rf"Bomb\wires_module\wire_{form}_{color}_full.png"
        )
        self.wire_img_cut = load_image(
            rf"Bomb\wires_module\wire_{form}_{color}_full.png"
        )
        self.color = color
        self.x, self.y = pos
        self.num = num  # порядковый номер в модуле
        self.iscut = False

    def draw(self, screen):
        if self.iscut:
            screen.blit(self.wire_img_cut, (self.x, self.y))
        else:
            screen.blit(self.wire_img_full, (self.x, self.y))


COLORS = ["red", "yellow", "blue", "black"]
FORMS = ["standart"]
