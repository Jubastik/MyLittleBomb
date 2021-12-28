import pygame
import pygame_gui
import random
from CONSTANTS import WIDTH, HEIGHT
from GameStages.Stage import Stage
from image_loader import load_image


class MenuStage(Stage):
    """Меню игры"""

    def init(self):
        self.ui_manager = self.gm.ui_manager
        self.background = pygame.Surface((self.width, self.height))
        self.init_gui()
        self.gui_off()

        return self

    def draw(self, screen):
        self.background.fill((255, 255, 255))
        self.all_sprites.draw(self.background)
        screen.blit(self.background, (0, 0))

    def init_gui(self):
        self.choose_lvl = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((880, 450), (170, 50)),
            text='Выбор уровня',
            manager=self.ui_manager
        )
        self.settings = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((880, 510), (170, 50)),
            text='Настройки',
            manager=self.ui_manager
        )
        self.leave_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((880, 570), (170, 50)),
            text='Выход',
            manager=self.ui_manager
        )

    def stage_launch(self):
        self.all_sprites = pygame.sprite.Group()
        self.timer = 30
        self.gui_on()

    def update(self):
        if self.timer == 0:
            for _ in range(16):
                Bomb(self.all_sprites)
                self.timer = 30
        self.all_sprites.update()
        self.timer -= 1

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.all_sprites.update(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # если нажата кнопка выбора уровня
                if event.ui_element == self.choose_lvl:
                    self.gm.change_stage('choose_lvl')
                    self.gui_off()
                # кнопка настроек
                if event.ui_element == self.settings:
                    pass
                # кнопка выхода
                if event.ui_element == self.leave_game:
                    self.gui_off()
                    self.gm.run = False

    def gui_on(self):
        self.leave_game.visible = True
        self.choose_lvl.visible = True
        self.settings.visible = True

    def gui_off(self):
        self.leave_game.visible = False
        self.choose_lvl.visible = False
        self.settings.visible = False


class Bomb(pygame.sprite.Sprite):
    image = load_image('bomb.png')
    image_boom = load_image('boom.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.v = 4
        self.r = random.randint(50, 800)
        self.rect = self.image.get_rect()
        self.fortune = random.randint(1, 100)
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(-200, -45)

    def update(self, *args):
        self.rect.y += self.v
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom
        if self.fortune % 5 == 0 or self.fortune % 2 == 0 or self.fortune % 3 == 0:
            if self.rect.y == HEIGHT - self.r:
                self.image = self.image_boom
        if self.rect.y >= 1120:
            self.kill()
