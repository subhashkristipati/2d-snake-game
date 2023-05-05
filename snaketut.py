from pygame.locals import *
from pygame import mixer
import pygame
import random

# Initialize..
pygame.init()
Win_Size = [800, 500]
iconPath = 'images/icon.png'
icon = pygame.image.load(iconPath)
Display = pygame.display.set_mode(Win_Size)
pygame.display.set_caption("snake xenzia")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)


# Images...
startScreenPath = 'images/start.png'
ApplePath = 'images/apple.png'
pausedPath = 'images/pause.png'

startScreen = pygame.image.load(startScreenPath)
Apple = pygame.image.load(ApplePath)
paused = pygame.image.load(pausedPath)
paused = pygame.transform.scale(paused, (100, 100))


# Colors..
red = [254, 5, 0]
green = [192, 255, 24]
blue = [17, 29, 94]
black = [0, 0, 0]
white = [255, 255, 255]
orange = [243, 113, 33]


# Sounds...
# (freq, bit depth, no. of audio channels, buffer size)
mixer.pre_init(44100, -16, 2, 512)

gameMusicPath = 'sounds/GameMusic.mp3'
gameOverPath = 'sounds/GameOver.mp3'
EatApplePath = 'sounds/EatSound.wav'

mixer.music.load(gameMusicPath)
gameover_sound = mixer.Sound(gameOverPath)
eat_sound = mixer.Sound(EatApplePath)


# Highest Score...

HS = 0

# Font Object...

font = pygame.font.SysFont("comicsansms", 30)

# pygame.draw.rect(): This function is used to draw a rectangle.
# It takes the surface, color, and pygame Rect object as an input parameter and draws a rectangle on the surface.


def snake(block_width, block_height, SnakeList):
    for XnY in SnakeList:
        Block = pygame.draw.rect(
            Display, green, (XnY[0], XnY[1], block_width, block_height))


def text_object(text, color):
    text_area = font.render(text, True, color)
    return text_area, text_area.get_rect()


def text(msg, color):
    surface, textRect = text_object(msg, color)
    textRect.center = (Win_Size[0]/2), (Win_Size[1]/2)
    Display.blit(surface, textRect)


def Show_Instructions():
    font = pygame.font.SysFont(None, 30)
    text1 = font.render("->Press P to pause", True, black)
    text2 = font.render("->Use arrow keys to move the snake", True, black)
    text3 = font.render("->Press Q to quit", True, black)
    text4 = font.render("->Press Space to play", True, black)
    text5 = font.render("->Press M to mute/unmute", True, black)
    Display.blit(text1, (10, 10))
    Display.blit(text2, (10, 40))
    Display.blit(text3, (10, 70))
    Display.blit(text4, (10, 100))
    Display.blit(text5, (10, 130))


# Pause function...
def Pause_Screen():
    Pause = True
    mixer.music.fadeout(1000)
    while Pause:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    mixer.music.play(-1)
                    Pause = False

                if event.key == K_q:
                    pygame.quit()
                    quit()

        Display.blit(paused, [350, 170])
        pygame.display.update()
        clock.tick(5)


# start screen function
def Start_Screen():
    StartLoop = True

    while StartLoop == True:
        Display.fill(white)
        Display.blit(startScreen, [220, 150])
        Show_Instructions()

        text = font.render("Press Space to Start", True, black)
        text_rect = text.get_rect(center=(Win_Size[0]/2, 400))
        Display.blit(text, text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    StartLoop = False

                if event.key == K_q:
                    pygame.quit()
                    quit()


def Game_Loop():

    # Snake_Object
    SnakeList = []
    SnakeLength = 3

    pos_x = Win_Size[0]/2
    pos_y = Win_Size[1]/2
    pos_x_change = 0
    pos_y_change = 0
    snake_width = 20
    snake_height = 20
    snake_step = 20

    # Apple_Object

    apple_width = 30
    apple_height = 30
    randApple_x = round(random.randrange(0, Win_Size[0]-apple_width))
    randApple_y = round(random.randrange(0, Win_Size[1]-apple_height))

    # Game_setting
    Game_Exit = False
    Game_Over = False
    mute = False
    # Game_Update = True
    # Snake speed control
    speed = 10

    # The music repeats indefinitely if this argument is set to -1
    mixer.music.play(-1)
    # get the music volume
    # Returns the current volume for the mixer. The value will be between 0.0 and 1.0.

    mixer.music.set_volume(0.9)

    while not Game_Exit:
        global HS
        # Giving scores bassed on snake length
        score = (SnakeLength-3)

        if score > HS:
            HS = score

        # game over
        while Game_Over == True:
            Display.fill(black)
            gameover_sound.set_volume(0.1)
            gameover_sound.play()

            font = pygame.font.Font(None, 32)
            text_surface1 = font.render(
                "GAME OVER! HIGHEST SCORE : {}".format(str(HS)), True, white)
            text_surface2 = font.render(
                "press 'space' to play again", True, white)
            text_rect1 = text_surface1.get_rect(
                center=(Win_Size[0]/2, Win_Size[1]/2 - 20))
            text_rect2 = text_surface2.get_rect(
                center=(Win_Size[0]/2, Win_Size[1]/2 + 20))
            Display.blit(text_surface1, text_rect1)
            Display.blit(text_surface2, text_rect2)
            pygame.display.update()

            # Pygame will register all events from the user into an event queue which can be received with the code pygame. event. get() .
            for event in pygame.event.get():
                if event.type == QUIT:
                    Game_Exit = True
                    Game_Over = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        mixer.music.play(-1)
                        gameover_sound.fadeout(100)
                        Game_Loop()
                    if event.key == K_q:
                        Game_Exit = True
                        Game_Over = False

        # While Playing Game
        for event in pygame.event.get():
            if event.type == QUIT:
                mixer.music.fadeout(100)
                Game_Exit = True

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    pos_x_change = -snake_step
                    pos_y_change = 0
                if event.key == K_RIGHT:
                    pos_x_change = snake_step
                    pos_y_change = 0
                if event.key == K_UP:
                    pos_y_change = -snake_step
                    pos_x_change = 0
                if event.key == K_DOWN:
                    pos_y_change = snake_step
                    pos_x_change = 0

                if event.key == K_p:
                    Pause_Screen()
                if event.key == K_q:
                    Game_Exit = True
                    Game_Over = False
                if event.key == pygame.K_m:
                    if mute:
                        mixer.music.set_volume(1.0)  # Unmute
                        mute = False
                    else:
                        mixer.music.set_volume(0.0)  # Mute
                        mute = True

        # Wall collision...
        if pos_x < 0 or pos_x > Win_Size[0] or pos_y < 0 or pos_y > Win_Size[1]:
            mixer.music.fadeout(1000)
            Game_Over = True

        # Snake Collision with Apple...
        if pos_x > randApple_x and pos_x < randApple_x + apple_width or pos_x + snake_width > randApple_x and pos_x + snake_width < randApple_x + apple_width:
            if pos_y > randApple_y and pos_y < randApple_y + apple_height or pos_y + snake_height > randApple_y and pos_y + snake_height < randApple_y + apple_height:
                randApple_x = round(random.randrange(
                    0, Win_Size[0]-apple_width))
                randApple_y = round(random.randrange(
                    0, Win_Size[1]-apple_height))
                SnakeLength += 1
                eat_sound.set_volume(1)
                eat_sound.play()

        pos_x += pos_x_change
        pos_y += pos_y_change

        # Canvas

        Display.fill(blue)

        # Apple Object...

        # surface.blit() function draws a source Surface onto this Surface
        Display.blit(Apple, [randApple_x, randApple_y])
        SnakeHead = []
        SnakeHead.append(pos_x)
        SnakeHead.append(pos_y)
        SnakeList.append(SnakeHead)

        if len(SnakeList) > SnakeLength:
            del SnakeList[0]

        # Self collision...
        for eachSegment in SnakeList[:-3]:
            if eachSegment == SnakeHead:
                mixer.music.fadeout(1000)
                Game_Over = True

        # Snake Object...
        snake(snake_width, snake_height, SnakeList)

        # Score Board...
        if (SnakeLength-3) > 0:
            text(str(SnakeLength-3), white)

        # It allows only a portion of the screen to updated, instead of the entire area.
        pygame.display.update()
        # clock.tick(speed) means that for every second at most 40 frames should pass.
        clock.tick(speed)

    pygame.quit()
    quit()


# Game call...
Start_Screen()

# Looping the game to start the next round
Game_Loop()
