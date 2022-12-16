import copy
import numpy as np
import random
from termcolor import colored  # can be taken out if you don't like it...

# # # # # # # # # # # # # # global values  # # # # # # # # # # # # # #
ROW_COUNT = 6
COLUMN_COUNT = 7

RED_CHAR = colored('X', 'red')  # RED_CHAR = 'X'
BLUE_CHAR = colored('O', 'blue')  # BLUE_CHAR = 'O'

EMPTY = 0
RED_INT = 1
BLUE_INT = 2


# # # # # # # # # # # # # # functions definitions # # # # # # # # # # # # # #

def create_board():
    """creat empty board for new game"""
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


def drop_chip(board, row, col, chip):
    """place a chip (red or BLUE) in a certain position in board"""
    board[row][col] = chip


def is_valid_location(board, col):
    """check if a given column in the board has a room for extra dropped chip"""
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    """assuming column is available to drop the chip,
    the function returns the lowest empty row  """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    """print current board with all chips put in so far"""
    # print(np.flip(board, 0))
    print(" 1 2 3 4 5 6 7 \n" "|" + np.array2string(np.flip(np.flip(board, 1)))
          .replace("[", "").replace("]", "").replace(" ", "|").replace("0", "_")
          .replace("1", RED_CHAR).replace("2", BLUE_CHAR).replace("\n", "|\n") + "|")


def game_is_won(board, chip):
    """check if current board contain a sequence of 4-in-a-row of in the board
     for the player that play with "chip"  """

    winning_Sequence = np.array([chip, chip, chip, chip])
    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[r, :]))):
            return True
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[:, c]))):
            return True
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board.diagonal(offset)))):
            return True
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            return True


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def inputHeuristic(board, color):
    # See if the agent can win or must block one move ahead
    valid_pos = get_valid_locations(board)
    bestCol = random.choice(valid_pos)
    if (color==BLUE_INT):
        for col in valid_pos:
            tmp = copy.deepcopy(board)
            row = get_next_open_row(tmp,col)
            drop_chip(tmp,row,col,BLUE_INT)
            if (game_is_won(tmp, BLUE_INT)):
                bestCol = col
                break
        for col in valid_pos:
            tmp = copy.deepcopy(board)
            row = get_next_open_row(tmp,col)
            drop_chip(tmp,row,col,RED_INT)
            if (game_is_won(tmp, RED_INT)):
                bestCol = col
                break
    if (color==RED_INT):
        for col in valid_pos:
            tmp = copy.deepcopy(board)
            row = get_next_open_row(tmp,col)
            drop_chip(tmp,row,col,RED_INT)
            if (game_is_won(tmp, RED_INT)):
                bestCol = col
                break
        for col in valid_pos:
            tmp = copy.deepcopy(board)
            row = get_next_open_row(tmp,col)
            drop_chip(tmp,row,col,BLUE_INT)
            if (game_is_won(tmp, BLUE_INT)):
                bestCol = col
                break
    drop_chip(board,get_next_open_row(board,bestCol),bestCol,color)

def MoveRandom(board, color):
    valid_locations = get_valid_locations(board)
    column = random.choice(
        valid_locations)  # you can replace with input if you like... -- line updated with Gilad's code-- thanks!
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)


def MoveMC(board, color):
    # assumes that the computer color is blue, and player color is red. This method only makes moves for the computer

    bestWinCount = -101
    bestCol = -1

    for nextCol in range(7):

        curWinCount = 0

        if not is_valid_location(board, nextCol):
            continue

        for nextTry in range(100):

            newBoard = board.copy()
            drop_chip(newBoard, get_next_open_row(newBoard, nextCol), nextCol, color)

            curColor = RED_INT

            while (not ((game_is_won(newBoard, RED_INT)) or (game_is_won(newBoard, BLUE_INT)))) and len(get_valid_locations(newBoard)) > 0:

                MoveRandom(newBoard, curColor)

                if curColor == RED_INT:
                    curColor = BLUE_INT
                else:
                    curColor = RED_INT

            if game_is_won(newBoard, BLUE_INT):
                curWinCount += 1

            if game_is_won(newBoard, RED_INT):
                curWinCount -= 1

        # print(str(curWinCount) + " >= " + str(bestWinCount) + ": " + str(curWinCount >= bestWinCount))
        if curWinCount >= bestWinCount:
            bestCol = nextCol
            bestWinCount = curWinCount

        # print("col: " + str(nextCol) + " | score: " + str(curWinCount))
        # print("bestWinCount: " + str(bestWinCount))


    drop_chip(board, get_next_open_row(board, bestCol), bestCol, BLUE_INT)


# # # # # # # # # # # # # # main execution of the game # # # # # # # # # # # # # #
turn = 0

board = create_board()
print_board(board)
game_over = False

while not game_over:

    if turn % 2 == 0:
        # to get input from the commandline
        # col = int(input("RED please choose a column(1-7): "))
        # while col > 7 or col < 1:
        #     col = int(input("Invalid column, pick a valid one: "))
        # while not is_valid_location(board, col - 1):
        #     col = int(input("Column is full. pick another one..."))
        # col -= 1
        # row = get_next_open_row(board, col)
        # drop_chip(board, row, col, RED_INT)

        #Professor's code to test
        inputHeuristic(board, RED_INT)

    if turn % 2 == 1 and not game_over:
        #MoveRandom(board, BLUE_INT)
        MoveMC(board, BLUE_INT)

    print_board(board)

    if game_is_won(board, RED_INT):
        game_over = True
        print(colored("Red wins!", 'red'))
    if game_is_won(board, BLUE_INT):
        game_over = True
        print(colored("Blue wins!", 'blue'))
    if len(get_valid_locations(board)) == 0:
        game_over = True
        print(colored("Draw!", 'blue'))
    turn += 1

# tmp = copy.deepcopy(board)
