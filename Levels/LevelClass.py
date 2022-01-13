from random import choice, randint
from Resources.BombGenerateInfo.BombSerialNum import (
    SERIAL_NUMBERS_FIRST_SECTOR,
    SERIAL_NUMBERS_THIRD_SECTOR,
)


class Level:
    """Уровень cодержит универсальную информацию о уровне."""
    def generate_serial_number(self):
        first = str(choice(SERIAL_NUMBERS_FIRST_SECTOR))
        second = str(randint(1001, 9999))
        third = str(choice(SERIAL_NUMBERS_THIRD_SECTOR))
        fourth = str(randint(1001, 9999))
        return [first, second, third, fourth]

    def generate_indicators(self):
        return [randint(0, 1) == 0, randint(0, 1) == 0]

    def generate_battery(self):
        return randint(1, 3)
