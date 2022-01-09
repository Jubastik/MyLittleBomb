import pygame
from random import randint, choice
from Entities.BobmModules.BobmModule import BobmModule
from Entities.BobmModules.WiresModule.Wire import Wire
from image_loader import load_image
from CONSTANTS import WIRES_COLORS as COLORS, WIRES_FORMS as FORMS


class WiresModule(BobmModule):
    """Модуль бомбы с проводами"""

    def init(self):
        self.isdefused = False
        path = lambda p: f"Bomb/wires_module/{p}.png"
        image = lambda p: load_image(path(p)).convert()
        self.module_img_off = image("wiremodule_off")
        self.module_img_on = image("wiremodule_on")
        self.wires_group, self.wires, self.answer = self.generate()
        return self

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
        wires_group = pygame.sprite.Group()
        for i in range(wire_count):
            color = choice(COLORS)
            form = choice(FORMS)
            wire = Wire(wires_group, color, form, position[i], i)
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
            yellow_count = 0
            black_count = 0
            for wire in wires:
                if wire.color == "red":
                    red_count += 1
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
        return wires_group, wires, answer

    # ------------------------------------------------------------------------------------------------------------------

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_wires(screen)

    def draw_background(self, screen):
        if self.isdefused:
            screen.blit(self.module_img_off, (self.x, self.y))
        else:
            screen.blit(self.module_img_on, (self.x, self.y))

    def draw_wires(self, screen):
        pos = pygame.mouse.get_pos()
        for wire in self.wires:
            x, y = pos
            if wire.check_click(x, y):
                screen.blit(
                    wire.wire_img_lightning, (wire.lightning_x, wire.lightning_y)
                )
        self.wires_group.draw(screen)

    # ------------------------------------------------------------------------------------------------------------------

    def LKM_down(self, x, y):
        # Получаем номер провода по месту клика
        answer = "on bomb"
        for wire in self.wires:
            if wire.check_click(x, y):
                answer = wire.num
                break
        # Проверяем
        if answer == "on bomb":
            return
        elif answer == self.answer:
            self.isdefused = True
        else:
            self.bomb.gs.mistakes += 1
            if self.bomb.gs.mistakes >= 3:
                self.bomb.gs.lose()
        self.wires[answer].cut()


