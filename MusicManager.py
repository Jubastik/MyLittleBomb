import pygame


class MusicManager:
    '''Осуществляет управление музыкой'''

    def __init__(self, GM):
        self.GM = GM
        self.music_list = {
            "menu": "Resources/Music/MenuMusic.mp3",
            "result": "Resources/Music/MenuMusic.mp3",
            "game": "Resources/Music/GameStart.mp3",
            "win": "Resources/Music/win.mp3",
            "explosion": "Resources/Music/explosion.mp3",
        }
        self.volume = self.GM.DATABASE.get_music_volume()[0] / 100
        pygame.mixer.music.set_volume(self.volume)

    def start_music(self, music):
        if music in self.music_list:
            if (music == "menu" or music == "choose_lvl") and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.music_list[music])
                pygame.mixer.music.play(-1)
            elif music == "game":
                pygame.mixer.music.load(self.music_list[music])
                pygame.mixer.music.play()
            elif music == "result":
                try:
                    if self.GM.stages["result"].is_win:
                        pygame.mixer.music.load(self.music_list["win"])
                    else:
                        pygame.mixer.music.load(self.music_list["explosion"])
                    pygame.mixer.music.play()
                except Exception:
                    print("err music manager")
                pygame.mixer.music.queue(self.music_list[music], loops=-1)

    def change_volume(self, vol):
        # Изменить текущее значение громкости на кол пунктов (от -100, до 100)
        self.volume += vol / 100
        if self.volume > 1:
            self.volume = 1
        if self.volume < 0:
            self.volume = 0
        self.volume = round(self.volume, 2)
        pygame.mixer.music.set_volume(self.volume)
        self.GM.DATABASE.update_music_volume(self.volume * 100)
