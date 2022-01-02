import pygame
from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image


class WiresModule(BobmModule):
    """Модуль бомбы с проводами"""

    def init(self):
        self.isdefused = False
        self.module_background = load_image(r"wires_background.png")
        # Координаты проводов
        self.wire1_x, self.wire1_y = self.x + 50, self.y + 47
        self.wire2_x, self.wire2_y = self.x + 50, self.y + 78
        self.wire3_x, self.wire3_y = self.x + 50, self.y + 110
        self.wire4_x, self.wire4_y = self.x + 50, self.y + 144
        self.wire5_x, self.wire5_y = self.x + 50, self.y + 178
        self.wire6_x, self.wire6_y = self.x + 50, self.y + 214
        self.wire1_img = load_image(r"wire1.png")
        self.wire2_img = load_image(r"wire2.png")
        self.wire3_img = load_image(r"wire3.png")
        # self.wire4_img = load_image(r"wire4.png")
        # self.wire5_img = load_image(r"wire5.png")
        # self.wire6_img = load_image(r"wire6.png")
        return self

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_wires(screen)

    def draw_background(self, screen):
        screen.blit(self.module_background, (self.x, self.y))
    
    def draw_wires(self, screen):
        screen.blit(self.wire1_img, (self.wire1_x, self.wire1_y))
        screen.blit(self.wire2_img, (self.wire2_x, self.wire2_y))
        screen.blit(self.wire3_img, (self.wire3_x, self.wire3_y))

    def generate(self):
        pass

    def click_LKM(self, x, y):
        pass
