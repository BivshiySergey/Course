import pygame
import os


class Sounds:
    def __init__(self):
        self.volume = 0.5
        self.shot_sound_path= os.path.join("sounds","shot.mp3")
        self.move_sound_path=os.path.join("sounds","move.mp3")
        self.move_sound=pygame.mixer.Sound(self.move_sound_path)
        self.shot_sound=pygame.mixer.Sound(self.shot_sound_path)

    def set_shot(self,path):
        self.shot_sound_path =path

    def set_move(self,path):
        self.move_sound_path =path

    def minus_volume(self):
        self.volume-=0.1
        self.move_sound.set_volume(self.volume)
        self.shot_sound.set_volume(self.volume)

    def plus_volume(self):
        self.volume+=0.1
        self.move_sound.set_volume(self.volume)
        self.shot_sound.set_volume(self.volume)


    def play_shot(self):
        pygame.mixer.Sound.stop(self.shot_sound)
        pygame.mixer.Sound.play(self.shot_sound)

    def play_move(self):
        pygame.mixer.Sound.stop(self.move_sound)
        pygame.mixer.Sound.play(self.move_sound)