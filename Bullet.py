import pygame



class Bullet():
    def __init__(self, xChange, yChange, dmg, character):
        from gui import screen

        if character.type == 'hero':
            self.colour = (0, 0, 255)
        else:
            self.colour = (255, 0, 0)

        self.x = character.x + 32
        self.y = character.y + 32
        self.radius = 5
        self.circle = pygame.draw.circle(
            screen, self.colour, (self.x, self.y), self.radius)
        self.xChange = xChange
        self.yChange = yChange
        self.dmg = dmg
        self.character = character

    def draw(self):
        from gui import screen
        
        screen.blit(self.circle, (self.x, self.y))
        self.x += self.xChange
        self.y += self.yChange

    def collide(self, char):
        rect = char.image.get_rect()
        rect.x = char.x
        rect.y = char.y

        if self.circle.colliderect(rect):
            return True
        else:
            return False
