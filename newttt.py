import pygame,time, pygame.mixer,sys, random
from pygame.locals import *
import os
os.environ["SDL_VIDEO_WINDOW_POS"] = '500,100'
pygame.mixer.init()
XO = "X"
sumx=0
sumy=0
grid = [[None , None , None],
        [None , None , None],
        [None , None , None]]

winner = None
Beep1=pygame.mixer.Sound('playerturn.wav')
Beep2=pygame.mixer.Sound('computermove.wav')
#Beep3=pygame.mixer.Sound('1.wav')
Beep4=pygame.mixer.Sound('crackers.wav')
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 222)
GREEN = (0, 245, 0)
RED = (255, 0, 0)

def print_header():
    print(""" 
    TIC TAC TOE
    1 | 2 | 3  
    4 | 5 | 6 
    7 | 8 | 9

     TO PLAY TIC TAC TOE YOU NEED TO GET 3 IN A ROW FROM 1 TO 9

    """)


print_header()

def initBoard(ttt):
    # background surface
    background = pygame.Surface(ttt.get_size())
    background = background.convert()
    background.fill((0, 255, 254))

    # vertical lines
    pygame.draw.line(background, (0, 0, 255), (100, 0), (100, 300), 3)
    pygame.draw.line(background, (0, 0, 255), (200, 0), (200, 300), 3)

    # horizontal lines...
    pygame.draw.line(background, (0, 0, 255), (0, 100), (300, 100), 3)
    pygame.draw.line(background, (0, 0, 255), (0, 200), (300, 200), 3)

    # return the board
    return background

def drawStatus(board):
    global XO, winner

    # status message
    if (winner is None):
        message = XO + "'s turn "


    else:
        message = winner + " cogratulations you won!"

    font = pygame.font.Font(None, 30)
    text = font.render(message, 1, (10, 10, 10))

    # copy the  message on board
    board.fill((250, 250, 250), (0, 300, 300, 25))
    board.blit(text, (10, 300))


def showBoard(ttt, board):
    # once again draw the game board
    drawStatus(board)
    ttt.blit(board, (0, 0))
    pygame.display.flip()


def boardPosition(mX, mY):
    # determine the row the user clicked
    if (mY < 100):
        row = 0
    elif (mY < 200):
        row = 1
    else:
        row = 2

    # determine the column the  clicked
    if (mX < 100):
        col = 0
    elif (mX < 200):
        col = 1
    else:
        col = 2

    return (row, col)


def drawMove(board, boardRow, boardCol, Mark):
    # draw an X or O  on the board in boardRow, boardCol and the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    if (Mark == 'O'):
        pygame.draw.circle(board, GREEN, (centerX, centerY), 44, 4)
    else:
        pygame.draw.line(board, RED, (centerX - 22, centerY - 22), \
                         (centerX + 22, centerY + 22), 4)
        pygame.draw.line(board, RED, (centerX + 22, centerY - 22), \
                         (centerX - 22, centerY + 22), 4)

    # mark the space as used
    grid[boardRow][boardCol] = Mark



def gameWon(board):
    # check if anyone has won the game

    global grid, winner

    # check rows
    for row in range(0, 3):
        if ((grid[row][0] == grid[row][1] == grid[row][2]) and
                (grid[row][0] is not None)):
            # this row won
            winner = grid[row][0]

            pygame.draw.line(board, (250, 0, 0), (0, (row + 1) * 100 - 50), (300, (row + 1) * 100 - 50), 5)

            break

    # check for cols
    for col in range(0, 3):
        if (grid[0][col] == grid[1][col] == grid[2][col]) and \
                (grid[0][col] is not None):
            # this column won
            winner = grid[0][col]
            pygame.draw.line
            pygame.draw.line(board, RED, ((col + 1) * 100 - 50, 0), \
                             ((col + 1) * 100 - 50, 300), 5)
            break

    # check for diagonal
    if (grid[0][0] == grid[1][1] == grid[2][2]) and \
            (grid[0][0] is not None):
        #  diagonally left to right
        winner = grid[0][0]
        pygame.draw.line(board, (250, 0, 0), (50, 50), (250, 250), 5)

    if (grid[0][2] == grid[1][1] == grid[2][0]) and \
            (grid[0][2] is not None):
        #  diagonally right to left
        winner = grid[0][2]
        pygame.draw.line(board, (250, 0, 0), (250, 50), (50, 250), 5)


def game_over(winner):
    if (winner != None):
        Beep4.play()
        time.sleep(5)
        sys.exit(0)


def compClick(board):

    global grid,XO

    def Enquiry(list):
        if not list:
            return 1
        else:
            return 0

    val = None
    list = [(index, row.index(val)) for index, row in enumerate(grid) if val in row]
    print(list)

    if Enquiry(list):
        print("The list is Empty")
    else:
        print("The list is not empty")
        number = random.choice(list)
        print(number)
        row = number[0]
        col = number[1]
        print(row, col)

        drawMove(board,row,col,XO)


    # toggle XO between the  player's move
    if (XO == "X"):
        XO = "O"
        Beep1.play()

    else:
        XO = "X"
        Beep2.play()

def clickBoard(board):
    global grid, XO

    (mX, mY) = pygame.mouse.get_pos()
    (row, col) = boardPosition(mX, mY)

    # make sure it is empty space
    if ((grid[row][col] == "X") or (grid[row][col] == "O")):
        # this space is in use
        return

    # draw an X or O
    drawMove(board, row, col, XO)

    # toggle XO between the  player's move
    if (XO == "X"):
        XO = "O"
        Beep1.play()

    else:
        XO = "X"
        Beep2.play()


print("Choose the opponent- ")
player_1 = input("ENTER 0 FOR COMPUTER and 1 FOR HUMAN  ")
player_1 = int(player_1)
print(player_1)

if (player_1 == 0):
    print("Player 1 is computer ")
    print("player 2 is YOU")
    print("You v\s Computer")

    cross = pygame.image.load('/home/eshita/PycharmProjects/ttt//cross.png')
    pygame.display.set_icon(cross)

    # initialize pygame  window
    pygame.init()

    ttt = pygame.display.set_mode((300, 325))
    pygame.display.set_caption('Tic-Tac-Toe')

    # create the game board
    board = initBoard(ttt)

    # main event loop
    running = 1

    while (running == 1):
        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0


            elif event.type is MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    print(pos)

                # the user clicked,put X or O
                clickBoard(board)
                compClick(board)

            # check for a winner
            gameWon(board)

            # update the display
            showBoard(ttt, board)
            game_over(winner)

    pygame.quit()

if (player_1==1):
    print("Player 1 is YOUR FRIEND ")
    print("player 2 is YOU")
    print("Your Friend v\s you")

    cross = pygame.image.load('/home/eshita/PycharmProjects/ttt//cross.png')
    pygame.display.set_icon(cross)

    # initialize pygame  window
    pygame.init()

    ttt = pygame.display.set_mode((300, 325))
    pygame.display.set_caption('Tic-Tac-Toe')

    # create the game board
    board = initBoard(ttt)

    # main event loop
    running = 1

    while (running == 1):
        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0


            elif event.type is MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    print(pos)

                # the user clicked,put X or O
                clickBoard(board)

            # check for a winner
            gameWon(board)

            # update the display
            showBoard(ttt, board)
            game_over(winner)

    pygame.quit()

