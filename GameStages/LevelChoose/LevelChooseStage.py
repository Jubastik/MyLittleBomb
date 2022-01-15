import pygame
import pygame_gui

from CONSTANTS import WIDTH
from Entities.Bomb import Bomb
from GameStages.LevelChoose.LevelsDescript import *
from GameStages.LevelChoose.Own_lvl_menu import OwnLevel
from GameStages.Stage import Stage
from Levels.Level1 import Level1
from Levels.Level2 import Level2
from Levels.Level3 import Level3
from Levels.Level4 import Level4
from Levels.Level5 import Level5
from image_loader import load_image

OWN_LVL_X1 = 100
OWN_LVL_X2 = OWN_LVL_X1 + 553
OWN_LVL_Y1 = 20
OWN_LVL_Y2 = OWN_LVL_Y1 + 1036

FIRST_BLOCK_POS = (100, 20)
SECOND_BLOCK_POS = (WIDTH // 3 + 50, 20)
THIRD_BLOCK_POS = (WIDTH // 3 * 2, 20)

START_BUTTONS_POS = (161, 924)
START_BUTTONS_SIZE = (231, 35)

TITLE_POS = (60, 77)
BEST_TIME_TXT_POS = (55, 690)
BEST_TIME_POS = (210, 770)

TEXT_BOX_POS = (21, 210)
TEXT_BOX_SIZE = (511, 420)


class LevelChooseStage(Stage):
    """Выбор уровня"""

    def init(self):
        self.ui_manager = self.gm.ui_manager
        self.background_lvl_active = load_image("LevelChooseImg/level_selection.png").convert()
        self.background_lvl_inactive = load_image("LevelChooseImg/level_selection_2.png").convert()
        self.font_best_time = pygame.font.Font(r'Resources/Pixeboy.ttf', 80)
        self.font_best_time_txt = pygame.font.Font(r'Resources/pix-font.otf', 45)
        self.page = 1
        self.page1_ui_group = []  # Список всего gui страницы
        self.page2_ui_group = []
        self.init_gui()
        self.end()
        self.OwnLevel = OwnLevel(self, 100, 20)
        return self

    def stage_launch(self):
        self.get_lvl_results()

        self.start()
        self.change_page(1)
        self.sprite_time = 0  # Время нахождения курсора мыши на спрайте уровня

        # Текущие спрайты бэкграунда выбора уровня
        self.sprite_first = self.background_lvl_inactive
        self.sprite_second = self.background_lvl_inactive
        self.sprite_third = self.background_lvl_inactive
        self.sprite_fourth = self.background_lvl_inactive
        self.sprite_fifth = self.background_lvl_inactive

    def update(self):
        try:
            # Обновление бэкграунда (мигание лампочки)
            x, y = pygame.mouse.get_pos()
            if OWN_LVL_X1 <= x <= OWN_LVL_X2 and OWN_LVL_Y1 <= y <= OWN_LVL_Y2:
                self.OwnLevel.on_sprite()
            if self.page == 1:
                self.OwnLevel.update()
                if self.rect_first.collidepoint((x, y)):
                    self.sprite_time += 1
                    if self.sprite_time == 20:
                        self.sprite_time = 0
                        self.sprite_first = self.background_changing(self.sprite_first)
                elif self.rect_second.collidepoint((x, y)):
                    self.sprite_time += 1
                    if self.sprite_time == 20:
                        self.sprite_time = 0
                        self.sprite_second = self.background_changing(self.sprite_second)
            elif self.page == 2:
                if self.rect_third.collidepoint((x, y)):
                    self.sprite_time += 1
                    if self.sprite_time == 20:
                        self.sprite_time = 0
                        self.sprite_third = self.background_changing(self.sprite_third)
                elif self.rect_fourth.collidepoint((x, y)):
                    self.sprite_time += 1
                    if self.sprite_time == 20:
                        self.sprite_time = 0
                        self.sprite_fourth = self.background_changing(self.sprite_fourth)
                elif self.rect_fifth.collidepoint((x, y)):
                    self.sprite_time += 1
                    if self.sprite_time == 20:
                        self.sprite_time = 0
                        self.sprite_fifth = self.background_changing(self.sprite_fifth)
        except AttributeError:
            pass

    def background_changing(self, background):
        if background == self.background_lvl_inactive:
            return self.background_lvl_active
        else:
            return self.background_lvl_inactive

    def draw(self, screen):
        screen.fill((90, 90, 90))
        if self.page == 1:
            self.draw_first_page(screen)
        else:
            self.draw_second_page(screen)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if self.page == 1 and OWN_LVL_X1 <= x <= OWN_LVL_X2 and OWN_LVL_Y1 <= y <= OWN_LVL_Y2:
                    self.OwnLevel.LKM_down(x, y)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self.button_processing(event)

    def button_processing(self, event):
        # Обработка нажатий на кнопки
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
        elif event.ui_element == self.btn_fourth_lvl:
            self.start_fourth_lvl()
        elif event.ui_element == self.btn_fifth_lvl:
            self.start_fifth_lvl()

    def change_page(self, page):
        # Активация и деактивация gui связанного с уровнями
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
        # Первичная инициализация всего gui из библиотеки pygame_gui
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
        self.first_lvl_gui()
        self.second_lvl_gui()
        self.third_lvl_gui()
        self.fourth_lvl_gui()
        self.fifth_lvl_gui()
        self.change_page(self.page)

    def get_lvl_results(self):
        self.lvl_results = self.gm.DATABASE.get_best_time()

    # ------------------------------------------------------------------------------------------------------------------

    def draw_first_page(self, screen):
        self.OwnLevel.draw(screen)
        self.draw_first_lvl(screen)
        self.draw_second_lvl(screen)

    def draw_second_page(self, screen):
        self.draw_third_lvl(screen)
        self.draw_fourth_lvl(screen)
        self.draw_fifth_lvl(screen)

    # ------------------------------------------------------------------------------------------------------------------

    def start_first_lvl(self):
        '''переключение стейджа и запуск уровня'''
        self.end()
        bomb = Bomb(self.gm.stages["game"])
        level = Level1()
        bomb.load_level(level)
        self.gm.stages["game"].set_bomb(bomb)
        self.gm.change_stage("game")

    def start_second_lvl(self):
        self.end()
        bomb = Bomb(self.gm.stages["game"])
        level = Level2()
        bomb.load_level(level)
        self.gm.stages["game"].set_bomb(bomb)
        self.gm.change_stage("game")

    def start_third_lvl(self):
        self.end()
        bomb = Bomb(self.gm.stages["game"])
        level = Level3()
        bomb.load_level(level)
        self.gm.stages["game"].set_bomb(bomb)
        self.gm.change_stage("game")

    def start_fourth_lvl(self):
        self.end()
        bomb = Bomb(self.gm.stages["game"])
        level = Level4()
        bomb.load_level(level)
        self.gm.stages["game"].set_bomb(bomb)
        self.gm.change_stage("game")

    def start_fifth_lvl(self):
        '''переключение стейджа и запуск уровня'''
        self.end()
        bomb = Bomb(self.gm.stages["game"])
        level = Level5()
        bomb.load_level(level)
        self.gm.stages["game"].set_bomb(bomb)
        self.gm.change_stage("game")

    # ------------------------------------------------------------------------------------------------------------------
    # первичная инициализация gui по уровням
    def first_lvl_gui(self):
        self.btn_first_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (SECOND_BLOCK_POS[0] + START_BUTTONS_POS[0], SECOND_BLOCK_POS[1] + START_BUTTONS_POS[1]),
            START_BUTTONS_SIZE),
            text='1 уровень',
            manager=self.ui_manager)

        self.lbl_first_lvl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SECOND_BLOCK_POS[0] + TITLE_POS[0], SECOND_BLOCK_POS[1] + TITLE_POS[1]),
                                      (337, 55)),
            text=f'Первые шаги',
            manager=self.ui_manager,
            object_id="#game_title")

        self.txt_first_lvl = pygame_gui.elements.UITextBox(
            FIRES_LVL_DESCRIPT,
            relative_rect=pygame.Rect((SECOND_BLOCK_POS[0] + TEXT_BOX_POS[0], SECOND_BLOCK_POS[1] + TEXT_BOX_POS[1]),
                                      TEXT_BOX_SIZE),
            manager=self.ui_manager,
            object_id="#text_box")
        self.page1_ui_group.extend([self.btn_first_lvl, self.lbl_first_lvl, self.txt_first_lvl])

    def second_lvl_gui(self):
        self.btn_second_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (THIRD_BLOCK_POS[0] + START_BUTTONS_POS[0], THIRD_BLOCK_POS[1] + START_BUTTONS_POS[1]), START_BUTTONS_SIZE),
            text='2 уровень',
            manager=self.ui_manager)

        self.lbl_second_lvl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((THIRD_BLOCK_POS[0] + TITLE_POS[0], THIRD_BLOCK_POS[1] + TITLE_POS[1]),
                                      (337, 55)),
            text=f'Вторые шаги',
            manager=self.ui_manager,
            object_id="#game_title")

        self.txt_second_lvl = pygame_gui.elements.UITextBox(
            SECOND_LVL_DESCRIPT,
            relative_rect=pygame.Rect((THIRD_BLOCK_POS[0] + TEXT_BOX_POS[0], THIRD_BLOCK_POS[1] + TEXT_BOX_POS[1]),
                                      TEXT_BOX_SIZE),
            manager=self.ui_manager,
            object_id="#text_box")
        self.page1_ui_group.extend([self.btn_second_lvl, self.lbl_second_lvl, self.txt_second_lvl])

    def third_lvl_gui(self):
        self.btn_third_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (FIRST_BLOCK_POS[0] + START_BUTTONS_POS[0], FIRST_BLOCK_POS[1] + START_BUTTONS_POS[1]), START_BUTTONS_SIZE),
            text='3 уровень',
            manager=self.ui_manager)

        self.lbl_third_lvl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((FIRST_BLOCK_POS[0] + TITLE_POS[0], FIRST_BLOCK_POS[1] + TITLE_POS[1]),
                                      (337, 55)),
            text=f'Третие шаги',
            manager=self.ui_manager,
            object_id="#game_title")

        self.txt_third_lvl = pygame_gui.elements.UITextBox(
            THIRD_LVL_DESCRIPT,
            relative_rect=pygame.Rect((FIRST_BLOCK_POS[0] + TEXT_BOX_POS[0], FIRST_BLOCK_POS[1] + TEXT_BOX_POS[1]),
                                      TEXT_BOX_SIZE),
            manager=self.ui_manager,
            object_id="#text_box")
        self.page2_ui_group.extend([self.btn_third_lvl, self.lbl_third_lvl, self.txt_third_lvl])

    def fourth_lvl_gui(self):
        self.btn_fourth_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (SECOND_BLOCK_POS[0] + START_BUTTONS_POS[0], SECOND_BLOCK_POS[1] + START_BUTTONS_POS[1]),
            START_BUTTONS_SIZE),
            text='4 уровень',
            manager=self.ui_manager)

        self.lbl_fourth_lvl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SECOND_BLOCK_POS[0] + TITLE_POS[0], SECOND_BLOCK_POS[1] + TITLE_POS[1]),
                                      (337, 55)),
            text=f'Четвертые шаги',
            manager=self.ui_manager,
            object_id="#game_title")

        self.txt_fourth_lvl = pygame_gui.elements.UITextBox(
            FOURTH_LVL_DESCRIPT,
            relative_rect=pygame.Rect((SECOND_BLOCK_POS[0] + TEXT_BOX_POS[0], SECOND_BLOCK_POS[1] + TEXT_BOX_POS[1]),
                                      TEXT_BOX_SIZE),
            manager=self.ui_manager,
            object_id="#text_box")
        self.page2_ui_group.extend([self.btn_fourth_lvl, self.lbl_fourth_lvl, self.txt_fourth_lvl])

    def fifth_lvl_gui(self):
        self.btn_fifth_lvl = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (THIRD_BLOCK_POS[0] + START_BUTTONS_POS[0], THIRD_BLOCK_POS[1] + START_BUTTONS_POS[1]), START_BUTTONS_SIZE),
            text='5 уровень',
            manager=self.ui_manager)

        self.lbl_fifth_lvl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((THIRD_BLOCK_POS[0] + TITLE_POS[0], THIRD_BLOCK_POS[1] + TITLE_POS[1]),
                                      (337, 55)),
            text=f'Пятые шаги',
            manager=self.ui_manager,
            object_id="#game_title")

        self.txt_fifth_lvl = pygame_gui.elements.UITextBox(
            FIFTH_LVL_DESCRIPT,
            relative_rect=pygame.Rect((THIRD_BLOCK_POS[0] + TEXT_BOX_POS[0], THIRD_BLOCK_POS[1] + TEXT_BOX_POS[1]),
                                      TEXT_BOX_SIZE),
            manager=self.ui_manager,
            object_id="#text_box")
        self.page2_ui_group.extend([self.btn_fifth_lvl, self.lbl_fifth_lvl, self.txt_fifth_lvl])

    # ------------------------------------------------------------------------------------------------------------------
    # Отрисовка уровня
    def draw_first_lvl(self, screen):
        lvl = "first"
        self.rect_first = screen.blit(self.sprite_first, SECOND_BLOCK_POS)

        res = self.font_best_time_txt.render("Лучшая попытка", True, (183, 47, 42))
        screen.blit(res, (SECOND_BLOCK_POS[0] + BEST_TIME_TXT_POS[0], SECOND_BLOCK_POS[1] + BEST_TIME_TXT_POS[1]))

        if lvl in self.lvl_results:
            txt = f"{self.lvl_results[lvl][0]}:{self.lvl_results[lvl][1]}"
        else:
            txt = "NET"
        res = self.font_best_time.render(txt, True, (255, 0, 0))
        screen.blit(res, (SECOND_BLOCK_POS[0] + BEST_TIME_POS[0], SECOND_BLOCK_POS[1] + BEST_TIME_POS[1]))

    def draw_second_lvl(self, screen):
        lvl = "second"
        self.rect_second = screen.blit(self.sprite_second, THIRD_BLOCK_POS)

        res = self.font_best_time_txt.render("Лучшая попытка", True, (183, 47, 42))
        screen.blit(res, (THIRD_BLOCK_POS[0] + BEST_TIME_TXT_POS[0], THIRD_BLOCK_POS[1] + BEST_TIME_TXT_POS[1]))

        if lvl in self.lvl_results:
            txt = f"{self.lvl_results[lvl][0]}:{self.lvl_results[lvl][1]}"
        else:
            txt = "NET"
        res = self.font_best_time.render(txt, True, (255, 0, 0))
        screen.blit(res, (THIRD_BLOCK_POS[0] + BEST_TIME_POS[0], THIRD_BLOCK_POS[1] + BEST_TIME_POS[1]))

    def draw_third_lvl(self, screen):
        lvl = "third"
        self.rect_third = screen.blit(self.sprite_third, FIRST_BLOCK_POS)

        res = self.font_best_time_txt.render("Лучшая попытка", True, (183, 47, 42))
        screen.blit(res, (FIRST_BLOCK_POS[0] + BEST_TIME_TXT_POS[0], FIRST_BLOCK_POS[1] + BEST_TIME_TXT_POS[1]))

        if lvl in self.lvl_results:
            txt = f"{self.lvl_results[lvl][0]}:{self.lvl_results[lvl][1]}"
        else:
            txt = "NET"
        res = self.font_best_time.render(txt, True, (255, 0, 0))
        screen.blit(res, (FIRST_BLOCK_POS[0] + BEST_TIME_POS[0], FIRST_BLOCK_POS[1] + BEST_TIME_POS[1]))

    def draw_fourth_lvl(self, screen):
        lvl = "fourth"
        self.rect_fourth = screen.blit(self.sprite_fourth, SECOND_BLOCK_POS)

        res = self.font_best_time_txt.render("Лучшая попытка", True, (183, 47, 42))
        screen.blit(res, (SECOND_BLOCK_POS[0] + BEST_TIME_TXT_POS[0], SECOND_BLOCK_POS[1] + BEST_TIME_TXT_POS[1]))

        if lvl in self.lvl_results:
            txt = f"{self.lvl_results[lvl][0]}:{self.lvl_results[lvl][1]}"
        else:
            txt = "NET"
        res = self.font_best_time.render(txt, True, (255, 0, 0))
        screen.blit(res, (SECOND_BLOCK_POS[0] + BEST_TIME_POS[0], SECOND_BLOCK_POS[1] + BEST_TIME_POS[1]))

    def draw_fifth_lvl(self, screen):
        lvl = "fifth"
        self.rect_fifth = screen.blit(self.sprite_fifth, THIRD_BLOCK_POS)

        res = self.font_best_time_txt.render("Лучшая попытка", True, (183, 47, 42))
        screen.blit(res, (THIRD_BLOCK_POS[0] + BEST_TIME_TXT_POS[0], THIRD_BLOCK_POS[1] + BEST_TIME_TXT_POS[1]))

        if lvl in self.lvl_results:
            txt = f"{self.lvl_results[lvl][0]}:{self.lvl_results[lvl][1]}"
        else:
            txt = "NET"
        res = self.font_best_time.render(txt, True, (255, 0, 0))
        screen.blit(res, (THIRD_BLOCK_POS[0] + BEST_TIME_POS[0], THIRD_BLOCK_POS[1] + BEST_TIME_POS[1]))

    # ------------------------------------------------------------------------------------------------------------------

    def start(self):
        # Активация всего gui
        self.menu_button.visible = True
        self.back_button.visible = True
        self.next_button.visible = True
        for ui in self.page2_ui_group:
            ui.visible = True
        for ui in self.page1_ui_group:
            ui.visible = True

    def end(self):
        # Деактивация всего gui
        self.back_button.visible = False
        self.next_button.visible = False
        self.menu_button.visible = False
        for ui in self.page2_ui_group:
            ui.visible = False
        for ui in self.page1_ui_group:
            ui.visible = False
