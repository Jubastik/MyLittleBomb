from image_loader import load_image

RANDOM_BTN_POS = (385, 252)


class OwnLevel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.init_img()
        self.rects = False
        self.sprite_time = 0

    def init_img(self):
        self.main_images = load_image("LevelChooseImg/own_lvl_main.png").convert()
        self.random_btn = load_image("LevelChooseImg/random_btn.png").convert()

    def init_rect(self, screen):
        self.random_btn_rect = screen.blit(self.random_btn, (self.x + RANDOM_BTN_POS[0], self.y + RANDOM_BTN_POS[1]))

    def draw(self, screen):
        if not self.rects:
            self.init_rect(screen)
            self.rects = True
        screen.blit(self.main_images, self.pos)

    def update(self):
        pass

    def LKM_down(self, x, y):
        if self.random_btn_rect.collidepoint((x, y)):
            self.start_random_mode()

    def start_random_mode(self):
        pass

    def on_sprite(self):
        self.sprite_time += 1
        if self.sprite_time == 20:
            self.lamp_flashing()
            self.sprite_time = 0

    def lamp_flashing(self):
        pass