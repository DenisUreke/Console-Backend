import pygame
from pathlib import Path

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sound(self, name, relative_path):
        abs_path = Path.cwd() / relative_path
        self.sounds[name] = pygame.mixer.Sound(str(abs_path))

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Sound '{name}' not found!")

    def play_music(self, relative_path, loop=-1):
        abs_path = Path.cwd() / relative_path
        pygame.mixer.music.load(str(abs_path))
        pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()
        
    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)  # 0.0 to 1.0
        
    def stop_all(self):
        self.stop_music()
        for sound in self.sounds.values():
            sound.stop()
