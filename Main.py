import pygame
from sys import exit

pygame.init()
pygame.font.init()

background = pygame.image.load('room.png')
main_char = pygame.image.load('main_char.png')
mob = pygame.image.load('mob.png')

SCREEN_WIDTH = background.get_width()
SCREEN_HEIGHT = background.get_height()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
myfont = pygame.font.SysFont('Comic Sans MS', 30)
notefont = pygame.font.SysFont('Comic Sans MS', 20)
clock = pygame.time.Clock()




def main():
    mainX = 20
    mainY = 50
    up, down, right, left = False, False, False, False

    while True:
        screen.blit(background, (0, 0))
        screen.blit(main_char, (mainX, mainY))
        if right:
            mainX += 5
        if left:
            mainX -= 5
        if up:
            mainY -= 5
        if down:
            mainY += 5
        

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


if __name__ == '__main__':
    main()
