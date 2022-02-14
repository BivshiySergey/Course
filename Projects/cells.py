import os
import pygame


class Cell:
    def __init__(self, type, surface=(40, 40)):
        self.rect = pygame.Rect(0, 0, surface[0], surface[1])
        self.type = type
        self.image = pygame.Surface(surface)

        if type == 0:
            self.hp = 0
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "grass.jpg")), surface)
        elif type == 1:
            self.hp = 3
            self.buff = {'HP': 1, 'Damage': 1}
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "dirt.jpg")), surface)
        elif type == 2:
            self.hp = 10
            self.buff = {'HP': 1, 'Damage': 2}
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "stone.jpg")), surface)
        elif type == 3:
            self.hp = 8
            self.buff = {'HP': 0, 'Damage': 2}
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "coal.jpg")), surface)
        elif type == 4:
            self.hp = 15
            self.buff = {'HP': 3, 'Damage': 3}
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "metal.jpg")), surface)
        elif type == 5:
            self.hp = 15
            self.buff = {'HP': 5, 'Damage': 0}
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "star.jpg")), surface)
        elif type == 6:
            self.hp = 40
            self.buff = {'HP': 0, 'Damage': 20}
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "heart.jpg")), surface)

    def damaged(self, damage):
        if self.type > 0:
            self.hp = self.hp - damage
            if self.hp > 0:
                return False
            else:
                self.type = 0
                self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "grass.jpg")),
                                                    self.image.get_size())
                return True

    def get_buff(self):
        return self.buff

    def get_type(self):
        return self.type

    def get_image(self):
        return self.image

    def set_rect(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect

    def get_hp(self):
        return self.hp
