import pygame
import math
from random import random
from Bullet import Bullet


class Mob():
    def __init__(self, x, y, bulletSpd, bulletDmg, health):
        self.image = pygame.image.load('mob.png')
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = health
        self.maxHealth = 20
        self.healthBarLength = 64
        self.bulletSpeed = bulletSpd
        self.bulletDamage = bulletDmg
        self.alive = True
        self.charType = "villain"
        self.dir = "Left"

    def flip(self):
        if self.dir == "Right":
            self.image = pygame.image.load('flipped_mob.png')

        if self.dir == "Left":
            self.image = pygame.image.load('mob.png')

    def displayHealth(self, screen):
        if self.health <= 0:
            self.health = 0
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y-25,
                                               self.health/(self.maxHealth/self.healthBarLength), 10))
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x, self.y-25, self.healthBarLength, 10), 2)

    def lowerHealth(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def shoot(self, x, y):
        xChange = x-self.x-32
        yChange = y-self.y-32

        xChange *= (0.2+random()) / 0.2
        yChange *= (0.2+random()) / 0.2
        size = xChange*xChange + yChange*yChange
        xChange /= math.sqrt(size)
        yChange /= math.sqrt(size)
        return Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed, self.bulletDamage, self)

    def move(self, x, y):
        xChange = x-self.x-32
        yChange = y-self.y-32
        if xChange < 0:
            self.dir = "Left"
        else:
            self.dir = "Right"
        self.flip()
        xChange *= (0.2+random()) / 0.2
        yChange *= (0.2+random()) / 0.2
        size = (xChange*xChange + yChange*yChange)+0.00000001
        xChange /= math.sqrt(size)
        yChange /= math.sqrt(size)
        self.x += xChange
        self.y += yChange
