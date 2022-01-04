import pygame
from random import randint, choice
from Entities.BobmModules.BobmModule import BobmModule
from Entities.Bomb import Bomb
from image_loader import load_image


class BigButtonModule(BobmModule):
    """Моудуль бомбы с большой кнопкой"""

    def init(self):
        self.isdefused = False
        self.click = False
        self.BATTERY_COUNT = self.bomb.batteries
        self.INDICATORS_COUNT = self.bomb.indicators
        print(self.BATTERY_COUNT)
        print(self.INDICATORS_COUNT)
        self.module_img_off = load_image(r"Bomb/BigButton_module/BigButton_module_img_off.png")
        self.module_img_on = load_image(r"Bomb/BigButton_module/BigButton_module_img_on.png")
        self.module_img = self.module_img_on
        self.generate()
        return self

    def draw(self, screen):
        self.draw_background(screen)
        if not self.click:
            self.button = screen.blit(self.button_default, self.position_button)
        if self.click:
            self.button = screen.blit(self.button_pressed, self.position_button)
        self.click = False
        self.inscription = screen.blit(self.image_inscription, self.position_inscription)
        if self.click:
            pass

    def draw_background(self, screen):
        if self.isdefused:
            screen.blit(self.module_img_off, (self.x, self.y))

        else:
            screen.blit(self.module_img_on, (self.x, self.y))

    def generate(self):
        self.position_button = [self.x + 54, self.y + 99]
        self.position_inscription = [self.x + 2, self.y - 120]
        self.button_color = choice(COLORS)
        self.button_default = load_image(
            f"Bomb/BigButton_module/button_default/BigButton_default_{self.button_color}.png")
        self.button_pressed = load_image(
            f"Bomb/BigButton_module/button_pressed/BigButton_pressed_{self.button_color}.png")
        self.button_words = choice(WORDS)
        if self.button_words == 'прервать':
            self.image_inscription = load_image(
                "Bomb/BigButton_module/BigButton_inscription_prervat.png"
            )
        elif self.button_words == 'взорвать':
            self.image_inscription = load_image(
                "Bomb/BigButton_module/BigButton_inscription_vzorvat.png"
            )
        elif self.button_words == 'держать':
            self.image_inscription = load_image(
                "Bomb/BigButton_module/BigButton_inscription_derzat.png"
            )
            self.position_inscription = [self.x + 10, self.y + 10]

    def click_LKM(self, x, y):
        # Проверка на нажатие по кнопкам
        if self.button.collidepoint((x, y)) and self.module_img != self.module_img_off:
            if self.button_color == 'blue' and self.button_words == 'прервать':
                print('conditional 1')
            elif self.button_words == 'взорвать':
                print('conditionfl 2')
            elif self.button_color == 'green' and \
                    self.INDICATORS_COUNT[0] is True and \
                    self.INDICATORS_COUNT[1] is False:
                print('conditional 3')
            elif self.BATTERY_COUNT > 2 and \
                    self.INDICATORS_COUNT[0] is False and \
                    self.INDICATORS_COUNT[1] is True:
                print('conditional 4')
            elif self.button_color == 'yellow':
                print('conditional 5')
            elif self.button_color == 'red' and self.button_words == 'держать':
                print('conditional 6')
            else:
                print('conditional else')
            self.click = True


COLORS = ['red', 'yellow', 'green', 'blue']
WORDS = ['прервать', 'взорвать', 'держать']
