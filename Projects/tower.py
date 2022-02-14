import os
import pygame
import tank


class Tower(tank.Tank):
    def __init__(self, stats, pos, player=True, surface=(40, 40)):
        super().__init__(stats, pos, player=True, surface=(40, 40))
        self.image = (255, 255, 255)
        if player:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "player_tower.png")), surface)
        else:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "enemy_tower.png")), surface)
