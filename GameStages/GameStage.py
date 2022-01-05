import pygame
import pygame_menu
from GameStages.Stage import Stage
from Entities.Bomb import Bomb
from image_loader import load_image
from CONSTANTS import BOMB_X, BOMB_Y, BOMB_X2, BOMB_Y2, FPS


# Порядок переключения на другой уровень:
# 1. Создаём объект бомбы
# 2. Создаём объект уровня
# 3. Передаём в бомбу объект уровня используя метод Bomb.load_level(level)
# 4. Передаём бомбу в GameStage исползуя метод GameStage.set_bomb(bomb)
# 5. Производим лаунч GameStage используя метод GameStage.stage_launch()
# 6. Меняем текущий стейдж игры в GameManager используя метод GameManager.change_stage()
class GameStage(Stage):
    """Игровая стадия.
    Перед использованием класс обязательно передаём объект бомбы в self.set_bomb"""

    def init(self):
        self.pause_check = False
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.pause_check:
            self.pause(screen)
        self.draw_background(screen)
        self.draw_hud(screen)
        self.bomb.draw(screen)
        if self.ispause:
            pass

    def process_event(self, event):
        if self.ispause:
            self.pause_check = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_click_LKM(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.ispause = not self.ispause

    def on_click_LKM(self, pos):
        # Проверка места нажатия, если кликнули на бомбу, обработка будет продолжена в бомбе
        x, y = pos
        if BOMB_X <= x <= BOMB_X2 and BOMB_Y <= y <= BOMB_Y2:
            self.bomb.click_LKM(x, y)

    def update(self):
        self.time -= 1
        # Проверка на поражение по времени
        if self.time <= 0:
            self.lose()
        # Паузы наверное не будет, пока что просто существует.
        if self.ispause:
            pass
        else:
            self.bomb.update()

    def draw_hud(self, screen):
        # Возможно не нужно, пока что просто существует
        pass

    def draw_background(self, screen):
        screen.fill((0, 0, 0))

    def stage_launch(self):
        self.ispause = False
        self.mistakes = 0
        self.time = FPS * 300

    def lose(self):
        # Соединение с EndStage
        print("lose")

    def win(self):
        # Соединение с EndStage
        print("win")

    def set_bomb(self, bomb):
        self.bomb = bomb

    def continue_game(self):
        self.ispause = False

    def pause(self, screen):
        menu = pygame_menu.Menu('Меню', 800, 500,
                                theme=pygame_menu.themes.THEME_DARK)

        menu.add.button('Продолжить', self.continue_game())
        menu.add.button('Главное меню')
        menu.add.button('Выход', pygame_menu.events.EXIT)

        menu.mainloop(screen)
