import pygame
import math
from Bullet import Bullet


class MainChar():
    def __init__(self, x, y):
        self.image = pygame.image.load('main_char.png')
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.maxHealth = 20
        self.health = 20
        self.healthBarLength = 400
        self.bulletSpeed = 5
        self.bulletDmg = 10
        self.alive = True
        self.charType = "hero"

    def displayHealth(self, screen):
        if self.health <= 0:
            self.health = 0
        pygame.draw.rect(screen, (255, 0, 0), (10, 10,
                                               self.health/(self.maxHealth/self.healthBarLength), 25))
        pygame.draw.rect(screen, (255, 255, 255),
                         (10, 10, self.healthBarLength, 25), 4)

    def lowerHealth(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def move(self, x, y):
        from gui import SCREEN_WIDTH, SCREEN_HEIGHT
        self.x += x
        self.y += y
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH-self.width:
            self.x = SCREEN_WIDTH-self.width
        if self.y < 0:
            self.y = 0
        if self.y > SCREEN_HEIGHT-self.height:
            self.y = SCREEN_HEIGHT-self.height

    def shoot(self, x, y):
        xChange = x-self.x-32
        yChange = y-self.y-32
        size = xChange*xChange + yChange*yChange
        xChange /= math.sqrt(size)
        yChange /= math.sqrt(size)
        return Bullet(xChange*self.bulletSpeed, yChange*self.bulletSpeed, self.bulletDmg, self)
