# Общие настройки
FPS = 30
WIDTH = 1920
HEIGHT = 1080

# Характеристики модуля бомбы
MODULE_BORDER = 15
MODULE_W = MODULE_H = 300  # обязательно чётное число
COUNT_MODULES_X = 3
COUNT_MODULES_Y = 2

# Характеристики бомбы
BOMB_W = (COUNT_MODULES_X * MODULE_W) + (((COUNT_MODULES_X * 2) - 2) * MODULE_BORDER)
BOMB_H = (COUNT_MODULES_Y * MODULE_W) + (((COUNT_MODULES_Y * 2) - 2) * MODULE_BORDER)
BOMB_X = (WIDTH // 2) - (BOMB_W // 2)  # Центрирование бомбы по X
BOMB_Y = (HEIGHT // 2) - (BOMB_H // 2)  # Центрирование бомбы по Y
BOMB_X2 = BOMB_X + BOMB_W
BOMB_Y2 = BOMB_Y + BOMB_H

# Характеристики картинки бомбы
BOMB_IMG_W = 990
BOMB_IMG_H = 795
BOMB_IMG_X = BOMB_X - 15
BOMB_IMG_Y = BOMB_Y - 150
BOMB_IMG_X2 = BOMB_IMG_X + BOMB_IMG_H
BOMB_IMG_Y2 = BOMB_IMG_Y + BOMB_IMG_H

# Характеристики надписи с серийником.
SERIAL_NUM_IMG_FONT = r"Resources/impact.ttf"
SERIAL_NUM_IMG_FONT_SIZE = 48
SERIAL_NUM_IMG_X = BOMB_IMG_X + 315 + 5
SERIAL_NUM_IMG_Y = BOMB_IMG_Y + 45
SERIAL_NUM_IMG_X2 = BOMB_IMG_X2 + 945 - 5
SERIAL_NUM_IMG_Y2 = BOMB_IMG_Y2 + 105 - 5
SERIAL_NUM_IMG_W = SERIAL_NUM_IMG_X2 - SERIAL_NUM_IMG_X
SERIAL_NUM_IMG_H = SERIAL_NUM_IMG_Y2 - SERIAL_NUM_IMG_Y


# Расчёт координат модулей
# Порядок модулей:
# 0 1 2
# 3 4 5
# Формат словаря: {номер модуля: [x, y, x2, y2]}
MODULES_COORDS = {
    0: [BOMB_X, BOMB_Y, BOMB_X + MODULE_W, BOMB_Y + MODULE_H],
    1: [
        BOMB_X + MODULE_W * 1 + MODULE_BORDER * 2,
        BOMB_Y,
        BOMB_X + MODULE_W * 2 + MODULE_BORDER * 2,
        BOMB_Y + MODULE_H,
    ],
    2: [
        BOMB_X + MODULE_W * 2 + MODULE_BORDER * 4,
        BOMB_Y,
        BOMB_X + MODULE_W * 3 + MODULE_BORDER * 4,
        BOMB_Y + MODULE_H,
    ],
    3: [
        BOMB_X,
        BOMB_Y + MODULE_H * 1 + MODULE_BORDER * 2,
        BOMB_X + MODULE_W,
        BOMB_Y + MODULE_H * 2 + MODULE_BORDER * 2,
    ],
    4: [
        BOMB_X + MODULE_W * 1 + MODULE_BORDER * 2,
        BOMB_Y + MODULE_H * 1 + MODULE_BORDER * 2,
        BOMB_X + MODULE_W * 2 + MODULE_BORDER * 2,
        BOMB_Y + MODULE_H * 2 + MODULE_BORDER * 2,
    ],
    5: [
        BOMB_X + MODULE_W * 2 + MODULE_BORDER * 4,
        BOMB_Y + MODULE_H * 1 + MODULE_BORDER * 2,
        BOMB_X + MODULE_W * 3 + MODULE_BORDER * 4,
        BOMB_Y + MODULE_H * 2 + MODULE_BORDER * 2,
    ],
}
