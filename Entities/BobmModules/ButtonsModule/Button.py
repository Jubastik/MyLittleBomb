import pygame
from image_loader import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, group, color, pos):
        super().__init__(group)
        self.btn_img_on = load_image(rf"Bomb/Buttons_module/button_{color}_on.png").convert()
        self.btn_img_off = load_image(rf"Bomb/Buttons_module/button_{color}_off.png").convert()

        # Переменные
        self.image = self.btn_img_off
        self.color = color
        self.x, self.y = pos

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

    def change_image(self, islightning=False):
        """islightning - светится ли кнопка"""
        if islightning:
            self.image = self.btn_img_on
        else:
            self.image = self.btn_img_off
