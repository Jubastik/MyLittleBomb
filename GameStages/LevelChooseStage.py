import pygame
import pygame_gui
from GameStages.Stage import Stage
from image_loader import load_image
from Levels.Level1 import Level1
from Entities.Bomb import Bomb


class LevelChooseStage(Stage):
    """Выбор уровня"""

    def init(self):
        self.ui_manager = self.gm.ui_manager
        self.background_lvl_active = load_image("level_selection.png")
        self.background_lvl_inactive = load_image("level_selection_2.png")
        self.WIDTH_BLOCK = (self.width - 200 - 20 * 3) // 3
        self.page = 1
        self.page1_ui_group = []
        self.page2_ui_group = []
        self.init_gui()
        self.end()
        return self

    def stage_launch(self):
        self.start()
        self.change_page(1)
        self.sprite_time = 0

        self.sprite_own = self.background_lvl_inactive
        self.sprite_first = self.background_lvl_inactive
        self.sprite_second = self.background_lvl_inactive
        self.sprite_third = self.background_lvl_inactive
        self.sprite_fourth = self.background_lvl_inactive
        self.sprite_fifth = self.background_lvl_inactive

    def update(self):
        try:
            if self.page == 1:
                if self.rect_own.collidepoint(pygame.mouse.get_pos()):
                    self.sprite_time += 1
                    if self.sprite_time == 30:
                        self.sprite_time = 0
                        self.sprite_own = self.background_changing(self.sprite_own)
                elif self.rect_first.collidepoint(pygame.mouse.get_pos()):
                    self.sprite_time += 1
                    if self.sprite_time == 30:
                        self.sprite_time = 0
                        self.sprite_first = self.background_changing(self.sprite_first)
                elif self.rect_second.collidepoint(pygame.mouse.get_pos()):
                    self.sprite_time += 1
                    if self.sprite_time == 30:
                        self.sprite_time = 0
                        self.sprite_second = self.background_changing(self.sprite_second)
            elif self.page == 2:
                if self.rect_third.collidepoint(pygame.mouse.get_pos()):
                    self.sprite_time += 1
                    if self.sprite_time == 30:
                        self.sprite_time = 0
                        self.sprite_third = self.background_changing(self.sprite_third)
        except:
            print("err")

    def draw(self, screen):
        screen.fill((90, 90, 90))
        if self.page == 1:
            self.draw_first_page(screen)
        else:
            self.draw_second_page(screen)

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self.button_processing(event)

    def background_changing(self, background):
        if background == self.background_lvl_inactive:
            return self.background_lvl_active
        else:
            return self.background_lvl_inactive

    def button_processing(self, event):
        if event.ui_element == self.next_button:
            if self.page == 1:
                self.change_page(2)
        elif event.ui_element == self.back_button:
            if self.page == 2:
                self.change_page(1)
        elif event.ui_element == self.menu_button:
            self.end()
            self.gm.change_stage("menu")
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

    def init_gui(self):
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 75, self.height // 2), (50, 100)),
            text='>',
            manager=self.ui_manager)
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, self.height // 2), (50, 100)),
            text='<',
            manager=self.ui_manager)
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 50), (75, 50)),
            text='Меню',
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
        '''переключение стейджа и запуск уровня'''
        self.end()
        bomb = Bomb(self.gm.stages["game"])
        level = Level1(bomb)
        bomb.load_level(level)
        self.gm.stages["game"].stage_launch()
        self.gm.stages["game"].set_bomb(bomb)
        self.gm.change_stage("game")

    def start_second_lvl(self):
        '''переключение стейджа и запуск уровня'''
        print("Старт 2го уровня")

    def start_third_lvl(self):
        '''переключение стейджа и запуск уровня'''
        print("Старт 3го уровня")

    def start_fourth_lvl(self):
        '''переключение стейджа и запуск уровня'''
        print("Старт 5го уровня")

    def start_fifth_lvl(self):
        '''переключение стейджа и запуск уровня'''
        print("Старт 5го уровня")

    # ------------------------------------------------------------------------------------------------------------------

    def own_lvl_gui(self):
        pass

    def first_lvl_gui(self):
        self.btn_first_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((850, 944), (231, 35)),
                                                          text='1 уровень',
                                                          manager=self.ui_manager)
        self.lbl_first_lvl = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((800, 100), (300, 50)),
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
        self.rect_own = screen.blit(self.sprite_own, (100, 20))

    def draw_first_lvl(self, screen):
        self.rect_first = screen.blit(self.sprite_first, (self.width // 3 + 50, 20))

    def draw_second_lvl(self, screen):
        self.rect_second = screen.blit(self.sprite_second, (self.width // 3 * 2, 20))

    def draw_third_lvl(self, screen):
        self.rect_third = screen.blit(self.sprite_third, (100, 20))

    def draw_fourth_lvl(self, screen):
        self.rect_fourth = screen.blit(self.sprite_fourth, (self.width // 3 + 50, 20))

    def draw_fifth_lvl(self, screen):
        self.rect_fifth = screen.blit(self.sprite_fifth, (self.width // 3 * 2, 20))

    def start(self):
        self.menu_button.visible = True
        self.back_button.visible = True
        self.next_button.visible = True
        for ui in self.page2_ui_group:
            ui.visible = True
        for ui in self.page1_ui_group:
            ui.visible = True

    def end(self):
        self.back_button.visible = False
        self.next_button.visible = False
        self.menu_button.visible = False
        for ui in self.page2_ui_group:
            ui.visible = False
        for ui in self.page1_ui_group:
            ui.visible = False
