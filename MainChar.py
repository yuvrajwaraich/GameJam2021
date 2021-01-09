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
        self.health = 20
        self.bullets = []
        self.bulletSpeed = 5
        self.bulletDmg = 10
        self.alive = True
        self.charType = "hero"

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
        angle = math.radians(math.tan((x-self.x)/(y-self.y)))
        xChange = self.bulletSpeed*math.cos(angle)
        yChange = self.bulletSpeed*math.sin(angle)
        self.bullets.append(Bullet(xChange, yChange, self.bulletDmg, self))
