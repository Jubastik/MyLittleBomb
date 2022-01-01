import pygame
from Entities.BobmModules.BobmModule import BobmModule
from image_loader import load_image
from CONSTANTS import FPS


class TimerModule(BobmModule):
    """Моудуль бомбы с таймером"""

    def init(self):
        self.isdefused = True
        self.module_image = load_image(r"timer.png")
        self.mistake_red = load_image(r"mistake_red.png")
        self.mistake_gray = load_image(r"mistake_gray.png")
        # Числа получены вручную
        self.section1_x = self.x + 65
        self.section1_y = self.y + 40
        self.section2_x = self.x + 125
        self.section2_y = self.y + 40
        self.section3_x = self.x + 185
        self.section3_y = self.y + 40
        self.section4_x = self.x + 77
        self.section4_y = self.y + 142
        return self

    def draw(self, screen):
        self.draw_module(screen)
        self.draw_sections(screen)

    def draw_module(self, screen):
        screen.blit(self.module_image, (self.x, self.y))

    def draw_sections(self, screen):
        # Ошибки
        if self.bomb.gs.mistakes == 0:
            screen.blit(self.mistake_gray, (self.section3_x, self.section3_y))
        if self.bomb.gs.mistakes <= 1:
            screen.blit(self.mistake_gray, (self.section2_x, self.section2_y))
        if self.bomb.gs.mistakes <= 2:
            screen.blit(self.mistake_gray, (self.section1_x, self.section1_y))
        # 35x135 270x190
        # Время
        time = self.bomb.gs.time // FPS  # Получаем оставшееся время в секундах
        minutes = str(time // 60)
        if len(minutes) == 1:
            minutes = '0' + minutes
        seconds = str(time % 60)
        if len(seconds) == 1:
            seconds = '0' + seconds
        txt = f'{minutes} : {seconds}'
        font = pygame.font.Font(r'Resources\Pixeboy.ttf', 60)
        res = font.render(txt, True, (255, 0, 0))
        screen.blit(res, (self.section4_x, self.section4_y))


    def update(self):
        # Время и ошибки учитывает GS, поэтому тут ничего не делаем.
        pass

    def click_LKM(self, x, y):
        pass
