import pygame


class Bullet():
    def __init__(self, xChange, yChange, dmg, character):
        from gui import screen

        if character.charType == 'hero':
            self.colour = (0, 0, 255)
        else:
            self.colour = (255, 0, 0)

        self.x = character.x + 32
        self.y = character.y + 32
        self.radius = 5
        self.circle = pygame.draw.circle(
            screen, self.colour, (int(self.x), int(self.y)), self.radius)
        self.xChange = xChange
        self.yChange = yChange
        self.dmg = dmg
        self.character = character

    def draw(self):
        from gui import screen

        circle = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(screen, self.colour,
                           (int(self.x), int(self.y)), self.radius)
        screen.blit(circle, (self.x, self.y))
        self.x += self.xChange*2
        self.y += self.yChange*2

    def collide(self, char):
        return (self.x > char.x and self.x < char.x + char.width) and (self.y > char.y and self.y < char.y + char.height)
