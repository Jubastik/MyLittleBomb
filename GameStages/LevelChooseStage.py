import pygame
import pygame_gui
from GameStages.Stage import Stage


class LevelChooseStage(Stage):
    """Выбор уровня"""

    def init(self):
        self.init_gui()
        self.width_block = (self.width - 200 - 20 * 3) // 3
        self.page = 1
        self.manager = self.manager_page1
        return self

    def init_gui(self):
        self.manager_lvl = pygame_gui.UIManager((self.width, self.height))
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 75, self.height // 2), (50, 100)),
            text='>',
            manager=self.manager_lvl)

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, self.height // 2), (50, 100)),
            text='<',
            manager=self.manager_lvl)

        self.manager_page1 = pygame_gui.UIManager((self.width, self.height))
        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                         text='Say Hello',
                                                         manager=self.manager_page1)
        self.manager_page2 = pygame_gui.UIManager((self.width, self.height))

    def draw(self, screen):
        screen.fill((100, 100, 100))
        if self.page == 1:
            self.draw_first_page(screen)
        else:
            self.draw_second_page(screen)
        self.manager_lvl.draw_ui(screen)
        self.manager.draw_ui(screen)

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.next_button:
                    if self.page == 1:
                        self.change_page(2)
                if event.ui_element == self.back_button:
                    if self.page == 2:
                        self.change_page(1)
                elif event.ui_element == self.hello_button:
                    print("урааа")

        self.manager_lvl.process_events(event)
        self.manager.process_events(event)

    def change_page(self, page):
        self.page = page
        if page == 1:
            self.manager = self.manager_page1
        else:
            self.manager = self.manager_page2

    def update(self):
        self.manager_lvl.update(0.03)
        self.manager.update(0.03)  # непонятно зачем нужно время с прошлого кадра, я вставил просто 30 / 1000

    def draw_first_page(self, screen):
        self.draw_own_level(screen)
        self.draw_first_level(screen)
        self.draw_second_level(screen)

    def draw_second_page(self, screen):
        self.draw_third_level(screen)
        self.draw_fourth_level(screen)
        self.draw_fifth_level(screen)

    def draw_own_level(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (100, 20, self.width_block, self.height - 40))

    def draw_first_level(self, screen):
        pygame.draw.rect(screen, (0, 20, 0), (self.width // 3 + 50, 20, self.width_block, self.height - 40))

    def draw_second_level(self, screen):
        pygame.draw.rect(screen, (0, 30, 0), (self.width // 3 * 2, 20, self.width_block, self.height - 40))

    def draw_third_level(self, screen):
        pygame.draw.rect(screen, (100, 0, 0), (100, 20, self.width_block, self.height - 40))

    def draw_fourth_level(self, screen):
        pygame.draw.rect(screen, (100, 20, 0), (self.width // 3 + 50, 20, self.width_block, self.height - 40))

    def draw_fifth_level(self, screen):
        pygame.draw.rect(screen, (100, 30, 0), (self.width // 3 * 2, 20, self.width_block, self.height - 40))
