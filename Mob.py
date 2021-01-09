import pygame
import math
from Bullet import Bullet


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('profile.jpg')
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = health
        self.bullets = []
        self.bulletDamage = 5

    def lowerHealth(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.health = 0

    def shoot(self, x, y):
        angle = math.radians(math.tan((x-self.x)/(y-self.y)))
        xChange = self.bulletSpeed*math.cos(angle)
        yChange = self.bulletSpeed*math.sin(angle)
        self.bullets.append(Bullet(xChange, yChange, self.bulletDamage, self))
