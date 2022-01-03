import pygame
from image_loader import load_image


class Wire(pygame.sprite.Sprite):
    def __init__(self, group, color, form, pos, num):
        super().__init__(group)
        self.wire_img_full = load_image(
            rf"Bomb\wires_module\wire_{form}_{color}_full.png"
        )
        self.wire_img_cut = load_image(
            rf"Bomb\wires_module\wire_{form}_{color}_cut.png"
        )
        # Подстветка
        self.wire_img_lightning = load_image(rf"Bomb\wires_module\wire_{form}_lightning.png")
        # Картинка подсветки на 20 пикселей больше чем картинка провода. 20 // 2 = 10
        self.lightning_x = pos[0] - 10
        self.lightning_y = pos[1] - 10

        # Переменные
        self.image = self.wire_img_full
        self.color = color
        self.x, self.y = pos
        self.num = num  # порядковый номер в модуле
        self.iscut = False

        # Коллизия
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def check_click(self, x, y):
        try:
            if self.mask.get_at((x - self.rect.x, y - self.rect.y)):
                return True
        except IndexError:
            pass
        return False

    def update(self):
        pass

    def cut(self):
        self.image = self.wire_img_cut