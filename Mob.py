import pygame
import math
from Bullet import Bullet


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, bulletSpd, bulletDmg, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('mob.png')
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = health
        self.bullets = []
        self.bulletSpeed = bulletSpd
        self.bulletDamage = bulletDmg
        self.alive = True
        self.type = "villain"
    
    def flip(self):
        self.image = pygame.image.load('flipped_mob.png')

    def lowerHealth(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def shoot(self, x, y):
        angle = math.radians(math.tan((x-self.x)/(y-self.y)))
        xChange = self.bulletSpeed*math.cos(angle)
        yChange = self.bulletSpeed*math.sin(angle)
        self.bullets.append(Bullet(xChange, yChange, self.bulletDamage, self))
