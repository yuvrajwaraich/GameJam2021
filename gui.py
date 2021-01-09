import pygame
from sys import exit
from MainChar import MainChar
from Mob import Mob

pygame.init()
pygame.font.init()

background = pygame.image.load('room.png')

SCREEN_WIDTH = background.get_width()
SCREEN_HEIGHT = background.get_height()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

mobs = []
main_char = MainChar(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

movementSpeed = 5
intensity = 1



def newLevel():
    up, down, right, left = False, False, False, False
    
    mobs.append(Mob(50, SCREEN_HEIGHT//2 - 32, 2 * intensity, 5 * intensity, 20))
    mobs.append(Mob(SCREEN_WIDTH - 64 - 50, SCREEN_HEIGHT//2 - 32, 2 * intensity, 5 * intensity, 20))

    while True:
        screen.blit(background, (0, 0))
        screen.blit(main_char.image, (main_char.x, main_char.y))
        
        for mob in mobs:
            screen.blit(mob.image, (mob.x, mob.y))
        
        if right:
            main_char.move(movementSpeed, 0)
        if left:
            main_char.move(-1 * movementSpeed, 0)
        if up:
            main_char.move(0, -1 * movementSpeed)
        if down:
            main_char.move(0, movementSpeed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    right = True
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    left = True
                if event.key in [pygame.K_UP, pygame.K_w]:
                    up = True
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    down = True

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    right = False
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    left = False
                if event.key in [pygame.K_UP, pygame.K_w]:
                    up = False
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    down = False

        pygame.display.update()

def main():
    newLevel()


if __name__ == '__main__':
    main()
