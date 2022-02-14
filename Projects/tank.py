import os
import pygame


class Tank:
    def __init__(self, stats, pos, player=True, surface=(40, 40)):
        self.hp = stats['HP']
        self.damage = stats['Damage']
        self.pos = pos
        self.AP = 2
        if player:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "player_tank.png")), surface)
        else:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "enemy_tank.png")), surface)

    def damaged(self, damage):
        self.hp = self.hp - damage
        if self.hp > 0:
            return False
        else:
            return True

    def get_type(self):
        return "tank"

    def get_image(self):
        return self.image

    def get_hp(self):
        return self.hp

    def get_damage(self):
        return self.damage

    def upgrade(self, buff):
        self.hp += buff['HP']
        self.damage += buff['Damage']

    def is_Dead(self):
        if self.hp > 0:
            return False
        else:
            return True
