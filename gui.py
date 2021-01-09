import pygame
from sys import exit
from MainChar import MainChar
from Mob import Mob
from random import randint


pygame.init()
pygame.font.init()

background = pygame.image.load('room.png')

SCREEN_WIDTH = background.get_width()
SCREEN_HEIGHT = background.get_height()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

mobs = []
bullets = set()
main_char = MainChar(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

movementSpeed = 5
intensity = 1


def options():
    BG_COLOUR = (168, 74, 50)
    running = True
    while running:
        screen.fill(BG_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)
        pygame.display.update()


def newLevel():
    up, down, right, left = False, False, False, False

    mob = Mob(50, SCREEN_HEIGHT//2 - 32, 2 * intensity, 5 * intensity, 20)
    mob.flip()
    mobs.append(mob)
    mobs.append(Mob(SCREEN_WIDTH - 64 - 50, SCREEN_HEIGHT //
                    2 - 32, 2 * intensity, 5 * intensity, 20))

    running = True
    currentTime = pygame.time.get_ticks()
    while running:
        screen.blit(background, (0, 0))
        screen.blit(main_char.image, (main_char.x, main_char.y))
        main_char.displayHealth(screen)
        for mob in mobs:
            screen.blit(mob.image, (mob.x, mob.y))
            mob.displayHealth(screen)

            if pygame.time.get_ticks()-currentTime > randint(200,800) :
                bullets.add(mob.shoot(main_char.x+32,main_char.y+32))
                currentTime = pygame.time.get_ticks()

        toDel = []
        mobsToDel = []
        for bullet in bullets:
            if(bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                toDel.append(bullet)
            elif(bullet.character.charType == 'villain' and bullet.collide(main_char)):
                if main_char.alive:
                    main_char.health -= 1
                toDel.append(bullet)
            else:
                bullet.draw()
            for mob in mobs:
                if(bullet.character.charType == 'hero' and bullet.collide(mob)):
                    toDel.append(bullet)
                    mob.lowerHealth(main_char.bulletDmg)
                    if(mob.alive == False):
                        mobsToDel.append(mob)

        for bullet in toDel:
            bullets.remove(bullet)
        for mob in mobsToDel:
            mobs.remove(mob)

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
                if event.key == pygame.K_ESCAPE:
                    up, down, right, left = False, False, False, False
                    options()
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

            if event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = pygame.mouse.get_pos()
                bullets.add(main_char.shoot(mouseX, mouseY))

        clock.tick(60)
        pygame.display.update()

        if len(mobs) == 0:
            running = False

def entryScreen():
    BG_COLOUR = (168, 74, 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


    play_button = pygame.Rect(250, 106, 500, 150)
    controls_button = pygame.Rect(250, 306, 500, 150)
    running = True
    while running:
        screen.fill(BG_COLOUR)

        screen.fill(BLACK, play_button)
        text = myfont.render("PLAY", True, WHITE)
        disp_coords = (play_button.center[0] - myfont.size("PLAY")[0]//2, play_button.center[1] - myfont.size("PLAY")[1]//2)
        screen.blit(text, disp_coords)

        screen.fill(BLACK, controls_button)
        text = myfont.render("CONTROLS", True, WHITE)
        disp_coords = (controls_button.center[0] - myfont.size("CONTROLS")[0]//2, controls_button.center[1] - myfont.size("CONTROLS")[1]//2)
        screen.blit(text, disp_coords)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                

        clock.tick(60)
        pygame.display.update()

def main():
    entryScreen()


if __name__ == '__main__':
    main()
