# Import the pygame module
import pygame as pg
import tileclass
import filehelper
import sudoku_methods

# Import py'game.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

# Initialize pygame
pg.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pg.Surface(screen.get_size())
background = background.convert()

background.fill((255,255,255))
screen.blit(background, (0,0))

t = tileclass.SudokuBoard(950)
values = filehelper.get_table("new file.txt")

if values != None:
    t.setup_board(values)

screen.blit(t, (0,0))

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pg.event.get():
        change = False
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
            elif event.key == pg.K_RETURN:
                t.save_board()
            elif event.key == pg.K_SPACE:
                print(sudoku_methods.check_solution(t))
            else:
                t.keypress(event.key, event.type)
                change = True
        elif event.type == pg.KEYUP:
            t.keypress(event.key, event.type)
            change = True
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = pg.mouse.get_pos()
            t.check_click(pos)
            change = True
        if change:
            screen.blit(t, (0,0))


    # Update the display
    pg.display.flip()
