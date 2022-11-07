import copy

import numpy
import numpy as np
import random
from termcolor import colored  # can be taken out if you don't like it...

# # # # # # # # # # # # # # 1. global values  # # # # # # # # # # # # # #
ROW_COUNT = 6
COLUMN_COUNT = 7

RED_CHAR = colored('X', 'red')  # RED_CHAR = 'X'
BLUE_CHAR = colored('O', 'blue')  # BLUE_CHAR = 'O'

EMPTY = 0
RED_INT = 1
BLUE_INT = 2


# # # # # # # # # # # # # # 2. helper functions # # # # # # # # # # # # # #

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


def get_valid_cols(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def get_viable_formations(board, chip):
    """
    @param board:
    @param chip:
    @return: the number of viable formations a given state has
    a 'viable formation' is a formation that can be used to win; therefore, all viable formations are four in length, and have either no chips in a given slot, or chips of the correct color
    the formations are scored by the number of chips it contains
    """

    total_chips_in_sets = 0

    four_one = np.array([chip, chip, chip, chip])

    three_one = np.array([chip, chip, chip, 0])
    three_two = np.array([chip, 0, chip, chip])
    three_three = np.array([chip, chip, 0, chip])
    three_four = np.array([0, chip, chip, chip])

    two_one = np.array([0, 0, chip, chip])
    two_two = np.array([0, chip, 0, chip])
    two_three = np.array([0, chip, chip, 0])
    two_four = np.array([chip, 0, 0, chip])
    two_five = np.array([chip, 0, chip, 0])
    two_six = np.array([chip, chip, 0, 0])

    one_one = np.array([0, 0, 0, chip])
    one_two = np.array([0, 0, chip, 0])
    one_three = np.array([0, chip, 0, 0])
    one_four = np.array([chip, 0, 0, 0])

    ##########################
    # 4
    ##########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, four_one))) in "".join(list(map(str, board[r, :]))):
            # return 4
            total_chips_in_sets += 4
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, four_one))) in "".join(list(map(str, board[:, c]))):
            # return 4
            total_chips_in_sets += 4
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, four_one))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 4
            total_chips_in_sets += 4

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, four_one))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 4
            total_chips_in_sets += 4

    ##########################
    # 3
    ##########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, three_one))) in "".join(list(map(str, board[r, :]))):
            # return 3
            total_chips_in_sets += 3

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, three_one))) in "".join(list(map(str, board[:, c]))):
            # return 3
            total_chips_in_sets += 3

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_one))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_one))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, three_two))) in "".join(list(map(str, board[r, :]))):
            # return 3
            total_chips_in_sets += 3

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, three_two))) in "".join(list(map(str, board[:, c]))):
            # return 3
            total_chips_in_sets += 3

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_two))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_two))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, three_three))) in "".join(list(map(str, board[r, :]))):
            # return 3
            total_chips_in_sets += 3

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, three_three))) in "".join(list(map(str, board[:, c]))):
            # return 3
            total_chips_in_sets += 3

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_three))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_three))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, three_four))) in "".join(list(map(str, board[r, :]))):
            # return 3
            total_chips_in_sets += 3

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, three_four))) in "".join(list(map(str, board[:, c]))):
            # return 3
            total_chips_in_sets += 3

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_four))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, three_four))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 3
            total_chips_in_sets += 3

    ##########################
    # 2
    ##########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, two_one))) in "".join(list(map(str, board[r, :]))):
            # return 2
            total_chips_in_sets += 2

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, two_one))) in "".join(list(map(str, board[:, c]))):
            # return 2
            total_chips_in_sets += 2

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_one))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_one))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, two_two))) in "".join(list(map(str, board[r, :]))):
            # return 2
            total_chips_in_sets += 2

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, two_two))) in "".join(list(map(str, board[:, c]))):
            # return 2
            total_chips_in_sets += 2

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_two))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_two))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, two_three))) in "".join(list(map(str, board[r, :]))):
            # return 2
            total_chips_in_sets += 2

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, two_three))) in "".join(list(map(str, board[:, c]))):
            # return 2
            total_chips_in_sets += 2

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_three))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_three))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, two_four))) in "".join(list(map(str, board[r, :]))):
            # return 2
            total_chips_in_sets += 2

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, two_four))) in "".join(list(map(str, board[:, c]))):
            # return 2
            total_chips_in_sets += 2

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_four))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_four))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, two_five))) in "".join(list(map(str, board[r, :]))):
            # return 2
            total_chips_in_sets += 2

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, two_five))) in "".join(list(map(str, board[:, c]))):
            # return 2
            total_chips_in_sets += 2

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_five))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_five))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    #########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, two_six))) in "".join(list(map(str, board[r, :]))):
            # return 2
            total_chips_in_sets += 2

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, two_six))) in "".join(list(map(str, board[:, c]))):
            # return 2
            total_chips_in_sets += 2

    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_six))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, two_six))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 2
            total_chips_in_sets += 2

    ##########################
    # 1
    ##########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, one_one))) in "".join(list(map(str, board[r, :]))):
            # return 1
            total_chips_in_sets += 1

    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, one_one))) in "".join(list(map(str, board[:, c]))):
            # return 1
            total_chips_in_sets += 1
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_one))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 1
            total_chips_in_sets += 1
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_one))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 1
            total_chips_in_sets += 1

    ##########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, one_two))) in "".join(list(map(str, board[r, :]))):
            # return 1
            total_chips_in_sets += 1
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, one_two))) in "".join(list(map(str, board[:, c]))):
            # return 1
            total_chips_in_sets += 1
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_two))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 1
            total_chips_in_sets += 1
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_two))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 1
            total_chips_in_sets += 1

    ##########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, one_three))) in "".join(list(map(str, board[r, :]))):
            # return 1
            total_chips_in_sets += 1
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, one_three))) in "".join(list(map(str, board[:, c]))):
            # return 1
            total_chips_in_sets += 1
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_three))) in "".join(list(map(str, board.diagonal(offset)))):
            return 1
            total_chips_in_sets += 1
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_three))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 1
            total_chips_in_sets += 1

    ##########################

    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, one_four))) in "".join(list(map(str, board[r, :]))):
            # return 1
            total_chips_in_sets += 1
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, one_four))) in "".join(list(map(str, board[:, c]))):
            # return 1
            total_chips_in_sets += 1
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_four))) in "".join(list(map(str, board.diagonal(offset)))):
            # return 1
            total_chips_in_sets += 1
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, one_four))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            # return 1
            total_chips_in_sets += 1

    return total_chips_in_sets

# # # # # # # # # # # # # # 3. move functions # # # # # # # # # # # # # #


def MoveRandom(board, color):
    valid_locations = get_valid_cols(board)
    column = random.choice(
        valid_locations)  # you can replace with input if you like... -- line updated with Gilad's code-- thanks!
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)


def move_min_max(board, computer_turn, horizon_count, horizon_limit, num_to_beat):
    '''
    @param board: 
    @param computer_turn: boolean
    @param horizon_count: the given level in the tree
    @param horizon_limit: at which point the tree no longer grows and the state is assessed
    @param num_to_beat: alpha or beta, depending on the turn
    @return: the value of the state after making a move

    computer is maximizing score
    layer is minimizing score

    this is a generic alpha-beta function tailored to the game, connect4
    the heuristic used to determine state value can be swapped out in the 3rd if statement

    '''

    if game_is_won(board, BLUE_INT):
        return float('inf')

    elif game_is_won(board, RED_INT):
        return -float('inf')

    # if the horizon is reached, the state is assessed based on the following heuristic
    if horizon_count == horizon_limit:
        return in_a_row(board)

    color = BLUE_INT
    if not computer_turn:
        color = RED_INT

    valid_cols = get_valid_cols(board)

    if computer_turn:

        max_found = -float('inf')
        max_col = 0
        lowest_row = -1

        for next_col in valid_cols:

            new_board = numpy.copy(board)
            next_row = get_next_open_row(new_board, next_col)
            drop_chip(new_board, next_row, next_col, BLUE_INT)
            next_value = move_min_max(new_board, not computer_turn, horizon_count + 1, horizon_limit, max_found)

            if next_value >= max_found:
                if next_value > max_found:
                    max_found = next_value
                    max_col = next_col
                    lowest_row = next_row
                if next_value == max_found:
                    if next_row > lowest_row:
                        max_col = next_col
                        lowest_row = next_row

            if next_value >= num_to_beat:
                break

        open_row = get_next_open_row(board, max_col)
        drop_chip(board, open_row, max_col, color)
        return max_found

    if not computer_turn:

        min_found = float('inf')
        min_col = 0
        lowest_row = -1

        for next_col in valid_cols:

            new_board = numpy.copy(board)
            next_row = get_next_open_row(new_board, next_col)
            drop_chip(new_board, next_row, next_col, RED_INT)
            next_value = move_min_max(new_board, not computer_turn, horizon_count + 1, horizon_limit, min_found)

            if next_value <= min_found:
                if next_value < min_found:
                    min_found = next_value
                    min_col = next_col
                    lowest_row = next_row
                if next_value == min_found:
                    if next_row > lowest_row:
                        min_col = next_col
                        lowest_row = next_row

            if next_value <= num_to_beat:
                break

        open_row = get_next_open_row(board, min_col)
        drop_chip(board, open_row, min_col, color)
        return min_found


# # # # # # # # # # # # # # 4. heuristics # # # # # # # # # # # # # #

'''
keeping track not only of longest sequence, but how distinct many sequences, like double trap
keeping track of when there is an empty space in between
not thinking that if i move somewhere and win, and then it could follow up, that computes to 05
'''


def in_a_row(board):
    blue_total = get_viable_formations(board, BLUE_INT)
    red_total = get_viable_formations(board, RED_INT)
    return blue_total - red_total


# # # # # # # # # # # # # # 5. main execution of the game # # # # # # # # # # # # # #
turn = 0

board = create_board()
print_board(board)
game_over = False

while not game_over:
    if turn % 2 == 0:
        # col = int(input("RED please choose a column(1-7): "))
        # while col > 7 or col < 1:
        #     col = int(input("Invalid column, pick a valid one: "))
        # while not is_valid_location(board, col - 1):
        #     col = int(input("Column is full. pick another one..."))
        # col -= 1
        #
        # row = get_next_open_row(board, col)
        # drop_chip(board, row, col, RED_INT)

        # MoveRandom(board, BLUE_INT)

        move_min_max(board, False, 0, 5, -float('inf'))


    if turn % 2 == 1 and not game_over:
        # MoveRandom(board, BLUE_INT)
        move_min_max(board, True, 0, 5, float('inf'))

    print_board(board)

    if game_is_won(board, RED_INT):
        game_over = True
        print(colored("Red wins!", 'red'))
    if game_is_won(board, BLUE_INT):
        game_over = True
        print(colored("Blue wins!", 'blue'))
    if len(get_valid_cols(board)) == 0:
        game_over = True
        print(colored("Draw!", 'blue'))
    turn += 1

# tmp = copy.deepcopy(board)

'''
making smart moves when all else is equal
keeping track not only of longest sequence, but how distinct many sequences, like double trap
keeping track of when there is an empty space in between
not thinking that if i move somewhere and win, and then it could follow up, that computes to 05
'''
