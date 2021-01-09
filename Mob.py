import pygame
import math
from Bullet import Bullet


class Mob():
    def __init__(self, x, y, bulletSpd, bulletDmg, health):
        self.image = pygame.image.load('mob.png')
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = health
        self.bulletSpeed = bulletSpd
        self.bulletDamage = bulletDmg
        self.alive = True
        self.charType = "villain"
    
    def flip(self):
        self.image = pygame.image.load('flipped_mob.png')

    def lowerHealth(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def shoot(self, x, y):
        xChange = x-self.x-32
        yChange = y-self.y-32
        size = xChange*xChange + yChange*yChange
        xChange /= math.sqrt(size)
        yChange /= math.sqrt(size)
        return Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed, self.bulletDamage, self)
