import pygame
from sys import exit
from MainChar import MainChar
from Mob import Mob
from Boss import Boss
from random import randint


pygame.init()
pygame.font.init()

background = pygame.image.load('room.png')
dead_screen = pygame.image.load('dead_screen.png')
control_pic = pygame.image.load('controls.png')
ladder_pic = pygame.image.load('ladder.png')

pygame.mixer.music.load('chillmusic.mp3')
pygame.mixer.music.play(-1)

SCREEN_WIDTH = background.get_width()
SCREEN_HEIGHT = background.get_height()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOUR = (168, 74, 50)

mobs = []
bullets = set()
main_char = MainChar(SCREEN_WIDTH//2 - 32, SCREEN_HEIGHT//2 - 32)
toDel = set()
mobsToDel = set()

movementSpeed = 5
currLevel = 0
highestScore = 0


def controls():
    running = True
    while running:
        screen.blit(control_pic, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.display.update()


def resetGame():
    main_char.x = SCREEN_WIDTH//2 - 32
    main_char.y = SCREEN_HEIGHT//2 - 32
    main_char.health = 20
    main_char.alive = True

    global bullets, mobs, toDel
    bullets = set()
    mobs = []
    toDel = set()
    mobsToDel = set()


def resetLevel():
    global currLevel
    currLevel = 0


def options():
    resume_button = pygame.Rect(250, 101, 500, 100)
    controls_button = pygame.Rect(250, 231, 500, 100)
    main_menu_button = pygame.Rect(250, 361, 500, 100)
    running = True
    while running:
        screen.fill(BG_COLOUR)

        screen.fill(BLACK, resume_button)
        text = myfont.render("RESUME", True, WHITE)
        fontSize = myfont.size("RESUME")
        disp_coords = (
            resume_button.center[0] - fontSize[0]//2, resume_button.center[1] - fontSize[1]//2)
        screen.blit(text, disp_coords)

        screen.fill(BLACK, controls_button)
        text = myfont.render("CONTROLS", True, WHITE)
        fontSize = myfont.size("CONTROLS")
        disp_coords = (
            controls_button.center[0] - fontSize[0]//2, controls_button.center[1] - fontSize[1]//2)
        screen.blit(text, disp_coords)

        screen.fill(BLACK, main_menu_button)
        text = myfont.render("EXIT TO MAIN MENU", True, WHITE)
        fontSize = myfont.size("EXIT TO MAIN MENU")
        disp_coords = (
            main_menu_button.center[0] - fontSize[0]//2, main_menu_button.center[1] - fontSize[1]//2)
        screen.blit(text, disp_coords)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mX, mY = pygame.mouse.get_pos()
                if resume_button.collidepoint((mX, mY)):
                    return True
                elif controls_button.collidepoint((mX, mY)):
                    controls()
                elif main_menu_button.collidepoint((mX, mY)):
                    return False

        clock.tick(60)
        pygame.display.update()


def goNextLevel():
    ladder_exit = pygame.Rect(SCREEN_WIDTH//2 - 32, SCREEN_HEIGHT //
                              2 + 100, ladder_pic.get_width(), ladder_pic.get_height())

    up, down, right, left = False, False, False, False
    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(ladder_pic, ladder_exit.topleft)

        screen.blit(main_char.image, (main_char.x, main_char.y))
        main_char.displayHealth(screen)

        main_char_rect = pygame.Rect(main_char.x, main_char.y, 64, 64)

        if main_char_rect.colliderect(ladder_exit):
            resetGame()
            return True

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
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    up, down, right, left = False, False, False, False
                    if not options():
                        return False

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

        clock.tick(60)
        pygame.display.update()


def deadScreen():
    running = True
    while running:
        screen.blit(dead_screen, (0, 0))

        text = myfont.render("Press Enter", True, WHITE)
        fontSize = myfont.size("Press Enter")
        disp_coords = (SCREEN_WIDTH//2 -
                       fontSize[0]//2, SCREEN_HEIGHT//2 + 150 - fontSize[1]//2)
        screen.blit(text, disp_coords)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    running = False

        pygame.display.update()


def normalLevel():
    global currLevel
    currLevel += 1

    up, down, right, left = False, False, False, False
    mouseDown = False

    for a in range(currLevel//3 + 2):
        if a % 2 == 0:
            mobX = randint(50, 300)
        else:
            mobX = randint(600, SCREEN_WIDTH - 64 - 50)
        mobY = randint(42, SCREEN_HEIGHT - 64 - 42)
        mobs.append(Mob(mobX, mobY, 2, 4, 20))

    level_disp = pygame.Rect(900, 0, 100, 42)
    myfont = pygame.font.SysFont('Comic Sans MS', 20)

    running = True
    currentTime = pygame.time.get_ticks()
    while running:
        screen.blit(background, (0, 0))
        screen.blit(main_char.image, (main_char.x, main_char.y))
        main_char.displayHealth(screen)

        text = myfont.render("Level: " + str(currLevel), True, WHITE)
        fontSize = myfont.size("Level: " + str(currLevel))
        disp_coords = (level_disp.center[0] - fontSize[0] //
                       2, level_disp.center[1] - fontSize[1]//2 + 20)
        screen.blit(text, disp_coords)

        global highestScore
        highestScore = max(highestScore, currLevel)
        highScore = myfont.render(
            "Highest Level: " + str(highestScore), True, WHITE)
        hs_fontSize = myfont.size("Highest Level: " + str(highestScore))
        hs_disp_coords = (level_disp.center[0] - hs_fontSize[0] //
                          2 - 42, level_disp.center[1] - hs_fontSize[1]//2 - 5)
        screen.blit(highScore, hs_disp_coords)

        for mob in mobs:
            screen.blit(mob.image, (mob.x, mob.y))
            mob.displayHealth(screen)
            if pygame.time.get_ticks()-currentTime > randint(200, 800):
                bullets.add(mob.shoot(main_char.x+32, main_char.y+32))
                currentTime = pygame.time.get_ticks()
            if pygame.time.get_ticks()-currentTime > randint(50, 200):
                mob.move(main_char.x+32, main_char.y+32)

        toDel, mobsToDel = set(), set()
        for bullet in bullets:
            if(bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                toDel.add(bullet)
            elif(bullet.character.charType == 'villain' and bullet.collide(main_char)):
                if main_char.alive:
                    main_char.lowerHealth(mobs[0].bulletDamage)
                toDel.add(bullet)
            else:
                bullet.draw()
            for mob in mobs:
                if(bullet.character.charType == 'hero' and bullet.collide(mob)):
                    toDel.add(bullet)
                    mob.lowerHealth(main_char.bulletDmg)
                    if(mob.alive == False):
                        mobsToDel.add(mob)

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
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    up, down, right, left = False, False, False, False
                    if not options():
                        return "no more play"
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

            if not mouseDown and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (True, False, False):
                mouseDown = True
                mouseX, mouseY = pygame.mouse.get_pos()
                bullets.add(main_char.shoot(mouseX, mouseY))

            if event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False

        clock.tick(60)
        pygame.display.update()

        if len(mobs) == 0:
            return 'continue'

        if not main_char.alive:
            return 'dead'


def timeLevel():
    global currLevel
    currLevel += 1

    up, down, right, left = False, False, False, False

    for a in range(currLevel//3 + 2):
        if a % 2 == 0:
            mobX = randint(50, 300)
        else:
            mobX = randint(600, SCREEN_WIDTH - 64 - 50)
        mobY = randint(42, SCREEN_HEIGHT - 64 - 42)
        mobs.append(Mob(mobX, mobY, 2, 4, 20))

    level_disp = pygame.Rect(900, 0, 100, 42)
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    timeFont = pygame.font.SysFont('Comic Sans MS', 35)
    time_disp = pygame.Rect(750, 0, 100, 42)

    running = True
    currentTime = pygame.time.get_ticks()
    startTime = pygame.time.get_ticks()
    while running:

        screen.blit(background, (0, 0))
        screen.blit(main_char.image, (main_char.x, main_char.y))
        main_char.displayHealth(screen)

        text = myfont.render("Level: " + str(currLevel), True, WHITE)
        fontSize = myfont.size("Level: " + str(currLevel))
        disp_coords = (level_disp.center[0] - fontSize[0] //
                       2, level_disp.center[1] - fontSize[1]//2 + 20)
        screen.blit(text, disp_coords)

        global highestScore
        highestScore = max(highestScore, currLevel)
        highScore = myfont.render(
            "Highest Level: " + str(highestScore), True, WHITE)
        hs_fontSize = myfont.size("Highest Level: " + str(highestScore))
        hs_disp_coords = (level_disp.center[0] - hs_fontSize[0] //
                          2 - 42, level_disp.center[1] - hs_fontSize[1]//2 - 5)
        screen.blit(highScore, hs_disp_coords)

        seconds = 15 - (pygame.time.get_ticks() - startTime)//1000

        if seconds > 9:
            textToWrite = "0:" + str(seconds)
        else:
            textToWrite = "0:0" + str(seconds)

    
        text = timeFont.render(textToWrite, True, WHITE)
        fontSize = timeFont.size(textToWrite)
        disp_coords = (
            SCREEN_WIDTH//2 - fontSize[0]//2, time_disp.center[1] - fontSize[1]//2)
        screen.blit(text, disp_coords)

        for mob in mobs:
            screen.blit(mob.image, (mob.x, mob.y))
            mob.displayHealth(screen)
            if pygame.time.get_ticks()-currentTime > randint(200, 800):
                bullets.add(mob.shoot(main_char.x+32, main_char.y+32))
                currentTime = pygame.time.get_ticks()
            if pygame.time.get_ticks()-currentTime > randint(50, 200):
                mob.move(main_char.x+32, main_char.y+32)

        toDel, mobsToDel = set(), set()
        for bullet in bullets:
            if(bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                toDel.add(bullet)
            elif(bullet.character.charType == 'villain' and bullet.collide(main_char)):
                if main_char.alive:
                    main_char.lowerHealth(mobs[0].bulletDamage)
                toDel.add(bullet)
            else:
                bullet.draw()

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
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    up, down, right, left = False, False, False, False
                    if not options():
                        return "no more play"
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

        clock.tick(60)
        pygame.display.update()

        if seconds == 0:
            return 'continue'

        if not main_char.alive:
            return 'dead'


def bossLevel():
    global currLevel
    currLevel += 1

    up, down, right, left = False, False, False, False

    if randint(0, 1):
        bossX = SCREEN_WIDTH//4 - 32
    else:
        bossX = SCREEN_WIDTH - SCREEN_WIDTH//4 - 32
    bossY = SCREEN_HEIGHT//2 - 32
    boss = Boss(bossX, bossY)

    level_disp = pygame.Rect(900, 0, 100, 42)
    myfont = pygame.font.SysFont('Comic Sans MS', 20)

    running = True
    currentTime = pygame.time.get_ticks()
    moveTime = pygame.time.get_ticks()
    while running:
        screen.blit(background, (0, 0))
        screen.blit(main_char.image, (main_char.x, main_char.y))
        main_char.displayHealth(screen)

        text = myfont.render("Level: " + str(currLevel), True, WHITE)
        fontSize = myfont.size("Level: " + str(currLevel))
        disp_coords = (level_disp.center[0] - fontSize[0] //
                       2, level_disp.center[1] - fontSize[1]//2 + 20)
        screen.blit(text, disp_coords)

        global highestScore
        highestScore = max(highestScore, currLevel)
        highScore = myfont.render(
            "Highest Level: " + str(highestScore), True, WHITE)
        hs_fontSize = myfont.size("Highest Level: " + str(highestScore))
        hs_disp_coords = (level_disp.center[0] - hs_fontSize[0] //
                          2 - 42, level_disp.center[1] - hs_fontSize[1]//2 - 5)
        screen.blit(highScore, hs_disp_coords)

        screen.blit(boss.image, (boss.x, boss.y))
        boss.displayHealth(screen)

        toDel = set()

        if pygame.time.get_ticks()-currentTime > 500:
            for bullet in boss.shoot(main_char.x+32, main_char.y+32):
                bullets.add(bullet)
            currentTime = pygame.time.get_ticks()

        if pygame.time.get_ticks()-moveTime > 3000:
            boss.move(main_char.x, main_char.y)
            moveTime = pygame.time.get_ticks()

        boss.changeDir(main_char.x, main_char.y)

        for bullet in bullets:
            if(bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                toDel.add(bullet)
            elif(bullet.character.charType == 'boss' and bullet.collide(main_char)):
                if main_char.alive:
                    main_char.lowerHealth(boss.bulletDamage)
                toDel.add(bullet)
            else:
                bullet.draw()

            if(bullet.character.charType == 'hero' and bullet.collide(boss)):
                toDel.add(bullet)
                boss.lowerHealth(main_char.bulletDmg)

        for bullet in toDel:
            bullets.remove(bullet)

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
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    up, down, right, left = False, False, False, False
                    if not options():
                        return "no more play"
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

        if not boss.alive:
            return 'continue'

        if not main_char.alive:
            return 'dead'


def nextLevel():
    if (currLevel + 1) % 10 == 0:
        return bossLevel()
    elif (currLevel + 1) % 5 == 0:
        return timeLevel()
    else:
        return normalLevel()


def entryScreen():
    play_button = pygame.Rect(250, 106, 500, 150)
    controls_button = pygame.Rect(250, 306, 500, 150)
    running = True
    while running:
        screen.fill(BG_COLOUR)

        screen.fill(BLACK, play_button)
        text = myfont.render("PLAY", True, WHITE)
        disp_coords = (play_button.center[0] - myfont.size("PLAY")
                       [0]//2, play_button.center[1] - myfont.size("PLAY")[1]//2)
        screen.blit(text, disp_coords)

        screen.fill(BLACK, controls_button)
        text = myfont.render("CONTROLS", True, WHITE)
        disp_coords = (controls_button.center[0] - myfont.size("CONTROLS")[
                       0]//2, controls_button.center[1] - myfont.size("CONTROLS")[1]//2)
        screen.blit(text, disp_coords)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mX, mY = pygame.mouse.get_pos()
                if play_button.collidepoint((mX, mY)):
                    alive = True
                    continueGame = True
                    while alive and continueGame:
                        result = nextLevel()
                        if result == 'continue':
                            if not goNextLevel():
                                continueGame = False
                        elif result == 'dead':
                            alive = False
                        elif result == 'no more play':
                            continueGame = False

                    if not alive:
                        deadScreen()
                    resetGame()
                    resetLevel()
                elif controls_button.collidepoint((mX, mY)):
                    controls()

        clock.tick(60)
        pygame.display.update()


def main():
    entryScreen()


if __name__ == '__main__':
    main()
