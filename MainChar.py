import pygame
import math
from Bullet import Bullet


class MainChar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('main_char.png')
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = 20
        self.bullets = []
        self.bulletSpeed = 5
        self.bulletDmg = 10
        self.alive = True

    def lowerHealth(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def move(self, x, y):
        from gui import SCREEN_WIDTH, SCREEN_HEIGHT
        self.x += x
        self.y += y
        if x < 0:
            x = 0
        if x > SCREEN_WIDTH:
            x = SCREEN_WIDTH
        if y < 0:
            y = 0
        if y > SCREEN_HEIGHT:
            y = SCREEN_HEIGHT

    def shoot(self, x, y):
        angle = math.radians(math.tan((x-self.x)/(y-self.y)))
        xChange = self.bulletSpeed*math.cos(angle)
        yChange = self.bulletSpeed*math.sin(angle)
        self.bullets.append(Bullet(xChange, yChange, self.bulletDmg, self))
