import pygame, time, sys, pygame.mixer
import os, random
from pygame.constants import QUIT

os.environ["SDL_VIDEO_WINDOW_POS"] = '500,100'
pygame.mixer.init()

# global variables
playerType = " "
player1Type = " "
player2Type = " "  # player type between human and computer
player1 = "HUMAN"  # player1 will be human
player2 = ""
player1choice = ""
playerChoice = ""  # choice between X/O
player2choice = ""
currentPlayer = ""
playerName = " "
player1Name = ""
player2Name = ""
grid = [[None, None, None],
        [None, None, None],
        [None, None, None]]
winner = None
# sound on click
Beep1 = pygame.mixer.Sound('playerturn.wav')
Beep2 = pygame.mixer.Sound('computermove.wav')
Beep4 = pygame.mixer.Sound('crackers.wav')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 222)
GREEN = (0, 245, 0)
RED = (255, 0, 0)


# START
# the header for tic-ta-toe
def print_header():
    print(""" 
    TIC TAC TOE
    1 | 2 | 3  
    4 | 5 | 6 
    7 | 8 | 9

     TO PLAY AND WIN TIC TAC TOE YOU NEED TO GET 3 IN A ROW FROM 1 TO 9

    """)


print_header()


# intialize the game board
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


def showBoard(ttt, board):
    # redraw the game board on the display

    drawStatus(board)
    ttt.blit(board, (0, 0))
    pygame.display.flip()


def boardPos(mouseX, mouseY):
    # determine the row the user clicked
    if (mouseY < 100):
        row = 0
    elif (mouseY < 200):
        row = 1
    else:
        row = 2

    # determine the column the user clicked
    if (mouseX < 100):
        col = 0
    elif (mouseX < 200):
        col = 1
    else:
        col = 2

    # return the tuple containing the row & column
    return (row, col)


# to check player type
def checkPlayerType(type):
    global player2Type
    if (type == "HUMAN"):
        player2Type = "HUMAN"
        return True
    elif (type == "COMPUTER"):
        player2Type = "COMPUTER"
        return True
    else:
        print(" Type only human or computer")
        exit()
        return False

    # return player2Type


def assignMark(mark):
    global player2choice, player1choice
    if (mark == "X"):
        player2choice = "O"

    elif (mark == "O"):
        player2choice = "X"

    else:
        print(" Type only X or O")
        exit()
        return False
    print(" PLAYER1 goes first your mark - ", player1choice)
    print(" PLAYER2 your mark - ", player2choice)
    return player2choice


# current player
def current_player(player):
    global currentPlayer, player1, player2
    player
    currentPlayer = player
    if (currentPlayer == player1):
        currentPlayer = player2
    else:
        currentPlayer = player1
    return currentPlayer


# Player Details
def playerDetails():
    global player1, player2, player1choice, player2Type, player1Name, player2Name
    print(" PLAYER1 IS HUMAN , CHOOSE THE OPPONENT - ")
    player2 = input("ENTER COMPUTER OR HUMAN - ").upper()
    player1Name = input("ENTER PLAYER1 NAME - ").upper()
    player2Name = input("ENTER PLAYER2 NAME - ").upper()
    # check type of player2
    checkPlayerType(player2)
    player2Type = player2
    print(player2Type)

    print(player1Name, " VS ", player2Name)
    # get the player1 choice
    player1choice = input(" PLAYER1 CHOOSE BETWEEN X AND O - ").upper()
    # put the choice
    player1Type = "HUMAN"
    assignMark(player1choice)
    current_player(player1)
    return player1Type, player2Type


def drawStatus(board):
    # draw the status at the bottom of the board
    # gain access to global variables
    global playerChoice, winner, player1choice, grid, playerName

    # determine the status message
    sumX = 0
    sumO = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[i][j] == "X":
                sumX += 1
            if grid[i][j] == "O":
                sumO += 1

    # playerChoice
    # status message
    if (sumX + sumO != 9):
        if (winner is None):
            message = playerChoice + "'s turn "

        else:
            message = winner + " congratulations you won!"

        font = pygame.font.Font(None, 30)
        text = font.render(message, 1, (10, 10, 10))

        board.fill((250, 250, 250), (0, 300, 300, 25))
        board.blit(text, (10, 300))


    elif (sumX + sumO == 9):
        if (winner is None):
            msg = "TIE"
            font = pygame.font.Font(None, 30)
            text = font.render(msg, 1, (10, 10, 10))

            # copy the  message on board
            board.fill((250, 250, 250), (0, 300, 300, 25))
            board.blit(text, (10, 300))

    #font = pygame.font.Font(None, 30)
    #text = font.render(message, 1, (10, 10, 10))

    # copy the  message on board
    #board.fill((250, 250, 250), (0, 300, 300, 25))
    #board.blit(text, (10, 300))


def Mark():
    global playerChoice, player1choice, player2choice

    if (playerChoice == player1choice):
        playerChoice = player2choice
        Beep1.play()

    else:
        playerChoice = player1choice
        Beep2.play()

    return playerChoice


def clickBoard(board):
    global grid, playerChoice, player1choice, player2choice

    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos(mouseX, mouseY)

    # make sure no one's used this space
    if ((grid[row][col] == "X") or (grid[row][col] == "O")):
        # this space is in use
        return

    # draw an X or O
    drawMove(board, row, col, playerChoice)

    # toggle XO to the other player's move
    # Mark()


def getPlayerMove():
    global player2Type, player1Type, currentPlayer
    player1Type = "HUMAN"
    if player1Type == "HUMAN" or player2Type == "HUMAN":
        clickBoard(board)
        Mark()

    if player2Type == "COMPUTER":
        compClick(board)
        Mark()


def compClick(board):
    global grid, player2choice, playerChoice, player1choice
    corner=[(0,0),(0,2),(2,0),(2,2)]
    side=[(0,1),(1,0),(1,2),(2,1)]
    middle=[(1,1)]

# computer's smart move
         # FOR PUTTING O

    def Enquiry(list):
        if not list:
            return 1
        else:
            return 0

    val = None
    list = [(index, row.index(val)) for index, row in enumerate(grid) if val in row]
   # list1 = [(0,1),(1,2),(2,1),(2,2)]
    print(list)

    if Enquiry(list):
        print("The list is Empty")


    else:

        for e in range(1):
            print("The list is not empty")
            number = random.choice(corner)
            row = number[0]
            col = number[1]
            num = random.choice(side)
            row1= num[0]
            col1= num[1]

            # print(number)
            #                print(row, col)

            if grid[row][col] == None:
                drawMove(board, row, col, playerChoice)

            elif grid[row1][col1] == None:
                drawMove(board,row1,col1,playerChoice)



            else:
                for itm in range(0, 3):
                    if (grid[itm][0] == grid[itm][1] == player2choice):
                        if (grid[itm][2] == None):
                            col = 2
                            row = itm
                            drawMove(board, row, col, playerChoice)
                            # grid[row][2] = 'O'
                            return row, col

                    elif (grid[itm][0] == grid[itm][2] == player2choice):
                        if (grid[itm][1] == None):
                            col = 1
                            row = itm
                            drawMove(board, row, col, playerChoice)
                            # grid[row][1] = 'O'
                            return row, col

                    elif (grid[itm][1] == grid[itm][2] == player2choice):
                        if (grid[itm][0] == None):
                            col = 0
                            row = itm
                            drawMove(board, row, col, playerChoice)
                            # grid[row][0] = 'O'
                            return row, col

                    # --------------------------------------------------------------------------------------------------
                    elif (grid[itm][0] == grid[itm][1] == player1choice):
                        if (grid[itm][2] == None):
                            col = 2
                            row = itm
                            drawMove(board, row, col, playerChoice)
                            return row, col

                            # grid[row][2] = 'O'
                    elif (grid[itm][0] == grid[itm][2] == player1choice):
                        if (grid[itm][1] == None):
                            col = 1
                            row = itm
                            drawMove(board, row, col, playerChoice)
                            # grid[row][1] = 'O'
                            return row, col

                    elif (grid[itm][1] == grid[itm][2] == player1choice):
                        if (grid[itm][0] == None):
                            col = 0
                            row = itm
                            drawMove(board, row, col, playerChoice)
                            # grid[row][0] = 'O'
                            return row, col


                    elif (grid[0][itm] == grid[1][itm] == player2choice):
                        if (grid[2][itm] == None):
                            row = 2
                            col = itm
                            drawMove(board, row, col, playerChoice)
                    elif (grid[0][itm] == grid[2][itm] == player2choice):
                        if (grid[1][itm] == None):
                            row = 1
                            col = itm
                            drawMove(board, row, col, playerChoice)

                    elif (grid[2][itm] == grid[1][itm] == player2choice):
                        if (grid[0][itm] == None):
                            row = 0
                            col = itm
                            drawMove(board, row, col, playerChoice)
                    elif (grid[0][itm] == grid[1][itm] == player1choice):
                        if (grid[2][itm] == None):
                            row = 2
                            col = itm
                            drawMove(board, row, col, playerChoice)
                    elif (grid[0][itm] == grid[2][itm] == player1choice):
                        if (grid[1][itm] == None):
                            row = 1
                            col = itm
                            drawMove(board, row, col, playerChoice)

                    elif (grid[2][itm] == grid[1][itm] == player1choice):
                        if (grid[0][itm] == None):
                            row = 0
                            col = itm
                            drawMove(board, row, col, playerChoice)

# -----------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------

def drawMove(board, boardRow, boardCol, Mark):
    # draw an X or O (Mark) on the board in boardRow, boardCol
    # determine the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    # draw the appropriate mark

    if (Mark == 'O'):
        pygame.draw.circle(board, GREEN, (centerX, centerY), 44, 4)
    else:
        pygame.draw.line(board, RED, (centerX - 22, centerY - 22), \
                         (centerX + 22, centerY + 22), 4)
        pygame.draw.line(board, RED, (centerX + 22, centerY - 22), \
                         (centerX - 22, centerY + 22), 4)

    grid[boardRow][boardCol] = Mark


def gameWon(board):
    # determine if anyone has won the game
    # board : the game board surface

    global grid, winner

    # check for winning rows
    for row in range(0, 3):
        if ((grid[row][0] == grid[row][1] == grid[row][2]) and
                (grid[row][0] is not None)):
            # this row won
            winner = grid[row][0]
            pygame.draw.line(board, (250, 0, 0), (0, (row + 1) * 100 - 50),
                             (300, (row + 1) * 100 - 50), 5)
            break

    # check for winning columns
    for col in range(0, 3):
        if (grid[0][col] == grid[1][col] == grid[2][col]) and \
                (grid[0][col] is not None):
            # this column won
            winner = grid[0][col]
            pygame.draw.line(board, (250, 0, 0), ((col + 1) * 100 - 50, 0), \
                             ((col + 1) * 100 - 50, 300), 5)
            break

    # check for diagonal winners
    if (grid[0][0] == grid[1][1] == grid[2][2]) and \
            (grid[0][0] is not None):
        # game won diagonally left to right
        winner = grid[0][0]
        pygame.draw.line(board, (250, 0, 0), (50, 50), (250, 250), 5)

    if (grid[0][2] == grid[1][1] == grid[2][0]) and \
            (grid[0][2] is not None):
        # game won diagonally right to left
        winner = grid[0][2]
        pygame.draw.line(board, (250, 0, 0), (250, 50), (50, 250), 5)

    return True


# game over function
def game_over(winner):
    if (winner != None):
        Beep4.play()
        time.sleep(5)
        sys.exit(0)


# player full details
playerDetails()
playerChoice = player1choice

# initialize pygame and window
pygame.init()
ttt = pygame.display.set_mode((300, 325))
pygame.display.set_caption('Tic-Tac-Toe')

# image icon on window
cross = pygame.image.load('/home/eshita/PycharmProjects/ttt//cross.png')
pygame.display.set_icon(cross)

# create the game board
board = initBoard(ttt)

showBoard(ttt, board)

# main event loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                player1 = "HUMAN"
                player2 = ""
                getPlayerMove()
                gameWon(board)

        # update the display

        showBoard(ttt, board, )
        game_over(winner)

pygame.quit()
