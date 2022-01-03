import pygame


class MusicManager:
    '''Осуществляет управление музыкой'''

    def __init__(self):
        self.music_list = {
            "menu": "Resources/Music/MenuMusic.mp3",
            "game": "Resources/Music/GameStart.mp3",
        }
        self.volume = 1.0

    def start_music(self, music):
        if music in self.music_list:
            pygame.mixer.music.load(self.music_list[music])
            if music == "menu":
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play()

    def change_volume(self, vol):
        # Изменить текущее значение громкости на кол пунктов (от -100, до 100)
        self.volume += vol / 100
        if self.volume > 1:
            self.volume = 1
        if self.volume < 0:
            self.volume = 0
        pygame.mixer.music.set_volume(self.volume)
