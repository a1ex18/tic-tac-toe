#import mysql.connector
import pygame as pg
import sys
import time
from pygame.locals import *

#mydb=mysql.connector.connect()
#if mydb.is_connected():
#  print("true")

XO = 'x'
# storing the winner's value
winner = None
# var to check if the game is a draw
draw = None

#width of window
width = 400

#height of window
height = 400

#background color of window
white = (255, 255, 255)
line_color = (0, 0, 0)
board = [[None] * 3, [None] * 3, [None] * 3]
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("My Tic Tac Toe")

# loading the images
initiating_window = pg.image.load("cover.png")
x_img = pg.image.load("x.jpg")
y_img = pg.image.load("o.jpg")

# resizing
initiating_window = pg.transform.scale(initiating_window, (width, height))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))


def game_initiating_window():

    #displaying over the screen
    screen.blit(initiating_window, (0, 0))

    # updating the display
    pg.display.update()
    time.sleep(3)
    screen.fill(white)

    # drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

    # drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_status()


def draw_status():

    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won !"
    if draw:
        message = "Game Draw !"

    font = pg.font.Font(None, 30)

    text = font.render(message, 1, (255, 255, 255))

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global board, winner, draw

    # checking for winning rows
    for row in range(0, 3):
        if ((board[row][0] == board[row][1] == board[row][2])
                and (board[row][0] is not None)):
            winner = board[row][0]
            pg.draw.line(screen,(220, 20, 60),(0, (row + 1) * height / 3 - height / 6), (width, (row + 1) * height / 3 - height / 6), 7)
            break

    # checking winning columns
    for col in range(0, 3):
        if ((board[0][col] == board[1][col] == board[2][col])
                and (board[0][col] is not None)):
            winner = board[0][col]
            pg.draw.line(screen, (220, 20, 60),((col + 1) * width / 3 - width / 6, 0),((col + 1) * width / 3 - width / 6, height), 7)
            break

    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 7)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 7)

    if (all([all(row) for row in board]) and winner is None):
        draw = True
    draw_status()


def drawXO(row, col):
    global board, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30
    if col == 1:
        posy = 30
    if col == 2:
        posy = height / 3 + 30
    if col == 3:
        posy = height / 3 * 2 + 30
    board[row - 1][col - 1] = XO

    if (XO == 'x'):
        screen.blit(x_img, (posy, posx))
        XO = 'o'

    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()


def user_click():
    x, y = pg.mouse.get_pos()

    if (x < width / 3):
        col = 1
    elif (x < width / 3 * 2):
        col = 2
    elif (x < width):
        col = 3
    else:
        col = None

    if (y < height / 3):
        row = 1

    elif (y < height / 3 * 2):
        row = 2

    elif (y < height):
        row = 3

    else:
        row = None

    if (row and col and board[row - 1][col - 1] is None):
        global XO
        drawXO(row, col)
        check_win()


def reset_game():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_initiating_window()
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]


game_initiating_window()

while (True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_click()
            if (winner or draw):
                reset_game()
    pg.display.update()
    CLOCK.tick(fps)
