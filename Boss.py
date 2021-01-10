import pygame
import math
from random import random
from Bullet import Bullet


class Boss():
    def __init__(self, x, y):
        self.image = pygame.image.load('boss.png')
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = 100
        self.maxHealth = 100
        self.healthBarLength = 64
        self.bulletSpeed = 3
        self.bulletDamage = 3
        self.alive = True
        self.charType = "boss"
        self.dir = "Left"

    def flip(self):
        if self.dir == "Right":
            self.image = pygame.image.load('flipped_boss.png')

        if self.dir == "Left":
            self.image = pygame.image.load('boss.png')

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

        size = xChange*xChange + yChange*yChange
        xChange /= math.sqrt(size)
        yChange /= math.sqrt(size)
        return [Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed, self.bulletDamage, self), 
                Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed + 1, self.bulletDamage, self),
                Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed - 1, self.bulletDamage, self),
                Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed + 2, self.bulletDamage, self),
                Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed - 2, self.bulletDamage, self),]


    def move(self, x, y):
        from gui import SCREEN_WIDTH

        if self.x == SCREEN_WIDTH//4 - 32:
            self.x = SCREEN_WIDTH - SCREEN_WIDTH//4 - 32
        else:
            self.x = SCREEN_WIDTH//4 - 32
    
    def changeDir(self, x, y):
        if self.x < x:
            self.dir = "Right"
        else:
            self.dir = "Left"
        self.flip()
