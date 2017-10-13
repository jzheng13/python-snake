import pygame
import random
import sys
import time

# global constants
unit = 10
game_x = 72
game_y = 48

# menu locations
title_y = 100
final_score_y = 160
menu_x = 210
start_y = 200
end_y = 280
menu_width = 300
menu_height = 50

# general helper functions
def opp(direction):
    opp_dir = {'LEFT': 'RIGHT',
               'RIGHT': 'LEFT',
               'UP': 'DOWN',
               'DOWN': 'UP'}
    return opp_dir[direction]

def randPos(x, y):
    return [random.randrange(x) * unit, random.randrange(y) * unit]

def inside(pos, x, y, width, height):
    return x <= pos[0] <= x + width and y <= pos[1] <= y + height

# initialisation
success, errors = pygame.init()
if errors:
    print("(!) Had {0} initialising errors, exiting...".format(errors))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialised.")

# game display
screen = pygame.display.set_mode((game_x * unit, game_y * unit))
pygame.display.set_caption("Snake Game")

# colours
red = pygame.Color(153, 0, 0)         # game over
green = pygame.Color(34, 139, 34)    # snake
black = pygame.Color(0, 0, 0)        # score
white = pygame.Color(255, 255, 255)  # background
brown = pygame.Color(140, 70, 20)    # food
lbrown = pygame.Color(160,90,40)     # menu highlight

# framerate controller
fps_controller = pygame.time.Clock()

# game menu
def gameMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit()
        screen.fill(white)

        # draw title
        drawTitle("Python Snake", green)

        # draw menu buttons
        drawButton("Start", menu_x, start_y, menu_width, menu_height, "play")
        drawButton("Quit", menu_x, end_y, menu_width, menu_height, "quit")

        # update
        pygame.display.update()

# score
def showScore(gameover=False, score = 0):
    font = pygame.font.SysFont("Calibri", 20)
    sc_surf = font.render("Score: {0}".format(score), True, black)
    sc_rect = sc_surf.get_rect()
    if (gameover):
        sc_rect.center = ((game_x / 2) * unit, final_score_y)
    else:
        sc_rect.midtop = (80, 10)
    screen.blit(sc_surf, sc_rect)

# game over
def gameOver(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit()
        screen.fill(white)

        # draw game over
        drawTitle("Game over!", red)
        
        # draw menu buttons
        drawButton("Restart", menu_x, start_y, menu_width, menu_height, "play")
        drawButton("Quit", menu_x, end_y, menu_width, menu_height, "quit")

        # draw score
        showScore(True, score)

        pygame.display.update()

def drawTitle(txt, col):
    title_font = pygame.font.SysFont("Calibri", 60)
    title_surf = title_font.render(txt, True, col)
    title_rect = title_surf.get_rect()
    title_rect.center = ((game_x / 2) * unit, title_y)
    screen.blit(title_surf, title_rect)

def drawButton(txt, x, y, width, height, action):

    # mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()
        
    # handle hover
    if inside(mouse_pos, x, y, width, height):
        pygame.draw.rect(screen, lbrown, (x, y, width, height))
        if mouse_clicked[0] and action != None:
            if action == "play":
                gameLoop()
            if action == "quit":
                gameExit()
    else:
        pygame.draw.rect(screen, brown, (x, y, width, height))

    # draw menu
    menu_font = pygame.font.SysFont("Calibri", 32)
    menu_surf = menu_font.render(txt, True, black)
    menu_rect = menu_surf.get_rect()
    menu_rect.center = ((game_x / 2) * unit, y + height / 2)
    screen.blit(menu_surf, menu_rect)

def gameExit():
    pygame.quit() # pygame window
    sys.exit()    # console


def gameLoop():

    # game objects and variables
    snake_pos = [360, 400]
    snake_body = [[360, 400], [360, 410], [360, 420]]
    snake_dir = 'UP'
    change_to = snake_dir

    food_pos = randPos(game_x, game_y)
    food_spawn = True

    game_score = 0

    while True:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):  
                    change_to = 'RIGHT'
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                elif event.key == pygame.K_ESCAPE:
                    gameOver(game_score)

        # direction validation
        if not (change_to == snake_dir or change_to == opp(snake_dir)):
            snake_dir = change_to

        # movement
        if snake_dir == 'LEFT':
            snake_pos[0] -= unit
        if snake_dir == 'RIGHT':
            snake_pos[0] += unit
        if snake_dir == 'UP':
            snake_pos[1] -= unit
        if snake_dir == 'DOWN':
            snake_pos[1] += unit

        # body mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            food_spawn = False
            game_score = game_score + 1
        else:
            snake_body.pop()

        # spawn food if eaten
        if not food_spawn:
            food_pos = randPos(game_x, game_y)
            food_spawn = True

        # draw
        screen.fill(white)
        for seg in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(seg[0], seg[1], unit, unit))
        pygame.draw.rect(screen, brown, pygame.Rect(food_pos[0], food_pos[1], unit, unit))

        # game over condition
        if snake_pos[0] > 710 or snake_pos[0] < 0 or snake_pos[1] > 470 or snake_pos[1] < 0:
            gameOver(game_score)

        for seg in snake_body[1:]:
            if snake_pos == seg:
                gameOver(game_score)

        # show score as normal if game looping
        showScore(False, game_score)

        # update game screen
        pygame.display.update()

        # set tick per second (determines snake speed)
        fps_controller.tick(25)

gameMenu()







