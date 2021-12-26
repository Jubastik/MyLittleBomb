import pygame
import pygame_gui
from GameStages.Stage import Stage


class LevelChooseStage(Stage):
    """Выбор уровня"""

    def init(self):
        self.ui_manager = self.gm.ui_manager
        self.WIDTH_BLOCK = (self.width - 200 - 20 * 3) // 3
        self.page = 1
        self.page1_ui_group = []
        self.page2_ui_group = []
        self.init_gui()
        return self

    def draw(self, screen):
        screen.fill((100, 100, 100))
        if self.page == 1:
            self.draw_first_page(screen)
        else:
            self.draw_second_page(screen)

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self.button_processing(event)

    def button_processing(self, event):
        if event.ui_element == self.next_button:
            if self.page == 1:
                self.change_page(2)
        elif event.ui_element == self.back_button:
            if self.page == 2:
                self.change_page(1)
        elif event.ui_element == self.btn_first_lvl:
            self.start_first_lvl()
        elif event.ui_element == self.btn_second_lvl:
            self.start_second_lvl()
        elif event.ui_element == self.btn_third_lvl:
            self.start_third_lvl()

    def change_page(self, page):
        self.page = page
        if page == 1:
            for ui in self.page2_ui_group:
                ui.visible = False
            for ui in self.page1_ui_group:
                ui.visible = True
        else:
            for ui in self.page2_ui_group:
                ui.visible = True
            for ui in self.page1_ui_group:
                ui.visible = False

    def update(self):
        pass

    def init_gui(self):
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 75, self.height // 2), (50, 100)),
            text='>',
            manager=self.ui_manager)
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, self.height // 2), (50, 100)),
            text='<',
            manager=self.ui_manager)
        self.own_lvl_gui()
        self.first_lvl_gui()
        self.second_lvl_gui()
        self.third_lvl_gui()
        self.change_page(1)

    # ------------------------------------------------------------------------------------------------------------------

    def draw_first_page(self, screen):
        self.draw_own_lvl(screen)
        self.draw_first_lvl(screen)
        self.draw_second_lvl(screen)

    def draw_second_page(self, screen):
        self.draw_third_lvl(screen)
        self.draw_fourth_lvl(screen)
        self.draw_fifth_lvl(screen)

    # ------------------------------------------------------------------------------------------------------------------

    def start_own_lvl(self):
        print("Старт своего уровня")

    def start_first_lvl(self):
        print("Старт 1го уровня")  # переключение стейджа и запуск 1го уровня
        self.end()

    def start_second_lvl(self):
        print("Старт 2го уровня")

    def start_third_lvl(self):
        print("Старт 3го уровня")

    def start_fourth_lvl(self):
        print("Старт 5го уровня")

    def start_fifth_lvl(self):
        print("Старт 5го уровня")

    # ------------------------------------------------------------------------------------------------------------------

    def own_lvl_gui(self):
        pass

    def first_lvl_gui(self):
        self.btn_first_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((850, 950), (250, 50)),
                                                          text='1 уровень',
                                                          manager=self.ui_manager)
        self.lbl_first_lvl = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((800, 200), (300, 50)),
                                                         text='Перые шаги',
                                                         manager=self.ui_manager,
                                                         object_id="#game_title")
        self.txt_first_lvl = pygame_gui.elements.UITextBox(
            """<p>Первого уровня <strong>не будет</strong>, кодеры приняли <strong>ислам</strong></p>""",
            relative_rect=pygame.Rect((800, 300), (400, 50)),
            manager=self.ui_manager)
        self.page1_ui_group.extend([self.btn_first_lvl, self.lbl_first_lvl, self.txt_first_lvl])

    def second_lvl_gui(self):
        self.btn_second_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1450, 950), (250, 50)),
                                                           text='2 уровень',
                                                           manager=self.ui_manager)
        self.page1_ui_group.extend([self.btn_second_lvl])

    def third_lvl_gui(self):
        self.btn_third_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 950), (250, 50)),
                                                          text='3 уровень',
                                                          manager=self.ui_manager)
        self.page2_ui_group.extend([self.btn_third_lvl])

    def fourth_lvl_gui(self):
        pass

    def fifth_lvl_gui(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def draw_own_lvl(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (100, 20, self.WIDTH_BLOCK, self.height - 40))  # ширина 550pt

    def draw_first_lvl(self, screen):
        pygame.draw.rect(screen, (0, 20, 0), (self.width // 3 + 50, 20, self.WIDTH_BLOCK, self.height - 40))

    def draw_second_lvl(self, screen):
        pygame.draw.rect(screen, (0, 30, 0), (self.width // 3 * 2, 20, self.WIDTH_BLOCK, self.height - 40))

    def draw_third_lvl(self, screen):
        pygame.draw.rect(screen, (100, 0, 0), (100, 20, self.WIDTH_BLOCK, self.height - 40))

    def draw_fourth_lvl(self, screen):
        pygame.draw.rect(screen, (100, 20, 0), (self.width // 3 + 50, 20, self.WIDTH_BLOCK, self.height - 40))

    def draw_fifth_lvl(self, screen):
        pygame.draw.rect(screen, (100, 30, 0), (self.width // 3 * 2, 20, self.WIDTH_BLOCK, self.height - 40))

    def end(self):
        self.next_button.kill()
        self.back_button.kill()
        for ui in self.page1_ui_group:
            ui.kill()
        for ui in self.page2_ui_group:
            ui.kill()
