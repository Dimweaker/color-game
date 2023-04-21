import pygame


class Player:
    def __init__(self, color, img_path):
        self.image_size = (60, 60)
        self.color = color
        self.x = 0
        self.y = 0
        self.alive = True
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, self.image_size)

