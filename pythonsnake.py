import pygame
import random
import sys
import time

# global constants
unit = 10
game_x = 72
game_y = 48

# helper functions
def opp(direction):
    opp_dir = {'LEFT': 'RIGHT',
               'RIGHT': 'LEFT',
               'UP': 'DOWN',
               'DOWN': 'UP'}
    return opp_dir[direction]

def randPos(x, y):
    return [random.randrange(x) * unit, random.randrange(y) * unit]

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
red = pygame.Color(255, 0, 0)        # game over
green = pygame.Color(0, 255, 0)      # snake
black = pygame.Color(0, 0, 0)        # score
white = pygame.Color(255, 255, 255)  # background
brown = pygame.Color(165, 42, 42)    # food

# framerate controller
fps_controller = pygame.time.Clock()

# game objects and variables
snake_pos = [360, 400]
snake_body = [[360, 400], [360, 410], [360, 420]]
snake_dir = 'UP'
change_to = snake_dir

food_pos = randPos(game_x, game_y)
food_spawn = True

game_score = 0

# score
def showScore(gameover):
    font = pygame.font.SysFont("Calibri", 20)
    sc_surf = font.render("Score: {0}".format(game_score), True, black)
    sc_rect = sc_surf.get_rect()
    if (gameover):
        sc_rect.midtop = (360, 100)
    else:
        sc_rect.midtop = (80, 10)
    screen.blit(sc_surf, sc_rect)

# game over
def gameOver():
    font = pygame.font.SysFont("Calibri", 60)
    go_surf = font.render("Game Over", True, red)
    go_rect = go_surf.get_rect()
    go_rect.midtop = (360, 25)
    screen.blit(go_surf, go_rect)
    showScore(True)
    pygame.display.flip()
    time.sleep(5)
    gameExit()

def gameExit():
    pygame.quit() # pygame window
    sys.exit()    # console

# game logic
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
                pygame.event.post(pygame.event.Event(pygame.QUIT))

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
        gameOver()

    for seg in snake_body[1:]:
        if snake_pos == seg:
            gameOver()

    showScore(False)

    # update game screen
    pygame.display.flip()

    # set tick per second (determines snake speed)
    fps_controller.tick(25)



