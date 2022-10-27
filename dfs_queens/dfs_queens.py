# -*- coding: utf-8 -*-

# columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
# hint -- you will need this for the following code: column=random.randrange(0,size)

import random
import sys

size = 0
queen_array = []
queen_array_mirror = [[]]


def place_n_queens():
    queen_array.clear()
    row = 0
    while row < size:
        column = random.randrange(0, size)
        queen_array.append(column)
        row += 1


def museum_solution():
    queen_array.clear()
    number_iterations = 0
    number_moves = 0
    solution_found = False

    while not solution_found:
        number_iterations += 1

        number_moves += size
        place_n_queens()

        solution_found = verify_solution()

    return solution_found, number_iterations, number_moves


def backtracking_solution():
    queen_array.clear()
    number_of_moves = 0  # where do I change this so that it counts the number of Queen moves?
    number_of_iterations = 0  # going through the process of searching through the board and making a move
    row = 0
    column = 0

    # iterate over rows of board
    while True:

        # place queen in next row
        while column < size:

            number_of_iterations += 1
            number_of_moves += 1

            if spot_is_safe(row, column):
                place_in_next_col(column)
                row += 1
                column = 0
                break
            else:
                column += 1

        # if I could not find an open column or if board is full
        if column == size or row == size:
            number_of_iterations += 1
            number_of_moves += 1

            # if board is full, we have a solution
            if row == size:
                return True, number_of_iterations, number_of_moves

            # I couldn't find a solution so I now backtrack
            prev_queen_position = remove_in_current_row()
            if prev_queen_position == -1:  # I backtracked past column 1
                return False, number_of_iterations, number_of_moves

            # try previous row again
            row -= 1

            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_queen_position


def heuristic_solution():
    queen_array.clear()
    number_iterations = 0
    number_moves = 0
    solution_found = False

    while not solution_found:

        number_iterations += 1
        # print("iteration: " + str(number_iterations))

        place_n_queens()
        number_moves += size

        if verify_solution():
            solution_found = True
            continue

        for x in range(10):

            # print("assessment: " + str(counter))
            rated_queens_map = rate_queens()
            rated_queens_rows = list(rated_queens_map)


            for y in range(1):
                worst_queen_row = rated_queens_rows[y]
                queen_array[worst_queen_row] = rated_queens_map.get(worst_queen_row)[1]
                number_moves += 1

                if verify_solution():
                    solution_found = True
                    break

    return True, number_iterations, number_moves



    # for next_queen in enumerate(rate_queens()):

    # 1. Genearte a random board
    # 2.
    #   a. Find most problematic queen
    #   b. Find lest problematic square
    # 3. Move until both: false solution AND at local max OR TRUE OR Ran a couple times
    # try randomly restarting only some, like the two biggest problems
    # 10 for 8, 100 for 100


# creates new board after a given number of iterations, or a local max
def heuristic_local_solution():
    queen_array.clear()
    number_iterations = 0
    number_moves = 0
    solution_found = False

    while not solution_found:

        number_iterations += 1
        # print("iteration: " + str(number_iterations))

        place_n_queens()
        number_moves += size

        if verify_solution():
            solution_found = True
            continue

        for counter in range(10):

            # print("assessment: " + str(counter))

            rated_queens_map = rate_queens()
            if at_local_max(rated_queens_map):
                break
            rated_queens_rows = list(rated_queens_map)

            for y in range(1):
                worst_queen_row = rated_queens_rows[y]
                queen_array[worst_queen_row] = rated_queens_map.get(worst_queen_row)[1]
                number_moves += 1

                if verify_solution():
                    solution_found = True
                    break


    return True, number_iterations, number_moves


def heuristic_only_local_solution():
    queen_array.clear()
    number_iterations = 0
    number_moves = 0
    solution_found = False

    while not solution_found:

        number_iterations += 1
        # print("iteration: " + str(number_iterations))

        place_n_queens()
        number_moves += size

        if verify_solution():
            solution_found = True
            continue

        while True:

            # print("assessment: " + str(counter))

            rated_queens_map = rate_queens()

            display()
            print()
            if at_local_max(rated_queens_map):
                break

            worst_queen_row = find_worst_queen(rated_queens_map)
            queen_array[worst_queen_row] = rated_queens_map.get(worst_queen_row)[1]
            number_moves += 1

            if verify_solution():
                solution_found = True
                break

    return True, number_iterations, number_moves


def forward_solution():
    # make a mirror image of the board, with only the correct possibilities within it
    # you still do dfs
    # what you could do is, think of them as pawns for conflicts, but when deciiding where to put down the queens, think of them as queens

    global queen_array_mirror

    queen_array.clear()
    queen_array_mirror.clear()
    number_of_moves = 0  # where do I change this so that it counts the number of Queen moves?
    number_of_iterations = 0  # going through the process of searching through the board and making a move
    row = 0
    column = 0

    queen_array_mirror = [[0 for i in range(size)] for j in range(size)]

    # iterate over rows of board
    while True:

        # place queen in next row
        while column < size:

            number_of_iterations += 1

            if spot_is_safe_forward(row, column):
                place_in_spot_forward(row, column)
                number_of_moves += 1
                row += 1
                column = 0
                break
            else:
                column += 1

        # if I could not find an open column or if board is full
        if column == size or row == size:
            number_of_iterations += 1
            number_of_moves += 1

            # if board is full, we have a solution
            if row == size:
                return True, number_of_iterations, number_of_moves

            # I couldn't find a solution so I now backtrack
            prev_queen_position = remove_in_current_row_forward()
            if prev_queen_position == -1:  # I backtracked past column 1

                return False, number_of_iterations, number_of_moves

            # try previous row again
            row -= 1

            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_queen_position


# def forward_heuristic_solution():

def rate_queens():
    rated_queens = {0: []}

    for next_queen_row_x, next_queen_col_x in enumerate(queen_array):

        current_score = 0
        best_col = next_queen_col_x
        best_col_score = sys.maxsize

        for next_col in range(0, size):

            next_col_score = 0

            for next_queen_row_y, next_queen_col_y in enumerate(queen_array):
                if does_conflict(next_queen_row_x, next_col, next_queen_row_y, next_queen_col_y):
                    next_col_score += 1

            if next_col == next_queen_col_x:
                current_score = next_col_score
                continue

            #best_col_score must be the best column aside the current column
            if next_col_score < best_col_score:
                best_col = next_col
                best_col_score = next_col_score

        rated_queens[next_queen_row_x] = [current_score, best_col, best_col_score]

    rated_queens_sorted = {k: v for k, v in sorted(rated_queens.items(), key=lambda item: item[1])}
    rated_queens_sorted_reversed = dict(reversed(list(rated_queens_sorted.items())))

    return rated_queens_sorted_reversed

def find_worst_queen(rated_queens_map):

    for next_row in rated_queens_map:

        next_queen_values = rated_queens_map.get(next_row)

        # by definition, the best column [2] must be a column other than the current
        if next_queen_values[0] >= next_queen_values[2]:
            return next_row


def at_local_max(rated_queens):
    for next_row in rated_queens:

        next_queen_values = rated_queens.get(next_row)

        #by definition, the best column [2] must be a column other than the current
        if next_queen_values[0] >= next_queen_values[2]:
            return False

    return True


def place_in_next_col(column):
    queen_array.append(column)


def place_in_spot_forward(row, col):
    queen_array.append(col)

    for next_row in range(size):
        for next_col in range(size):

            if (next_row == row) & (next_col == col):
                queen_array_mirror[next_row][next_col] += 1
                continue

            if next_col == col:
                queen_array_mirror[next_row][next_col] += 1

            if next_row == row:
                queen_array_mirror[next_row][next_col] += 1
                continue

            if next_col - next_row == col - row:
                queen_array_mirror[next_row][next_col] += 1

            if (size - next_col) - next_row == (size - col) - row:
                queen_array_mirror[next_row][next_col] += 1


def remove_in_current_row():
    if len(queen_array) > 0:
        return queen_array.pop()
    return -1


def remove_in_current_row_forward():
    row = len(queen_array) - 1

    if row >= 0:
        col = queen_array.pop()

        for next_row in range(size):
            for next_col in range(size):

                if (next_row == row) & (next_col == col):
                    queen_array_mirror[next_row][next_col] -= 1
                    continue

                if next_col == col:
                    queen_array_mirror[next_row][next_col] -= 1

                if next_row == row:
                    queen_array_mirror[next_row][next_col] -= 1

                if next_col - next_row == col - row:
                    queen_array_mirror[next_row][next_col] -= 1

                if (size - next_col) - next_row == (size - col) - row:
                    queen_array_mirror[next_row][next_col] -= 1

        return col

    return -1


# ture if no conflict
def does_conflict(row_x, col_x, row_y, col_y):
    if col_x == col_y:
        return True

    if row_x == row_y:
        return True

    if col_x - row_x == col_y - row_y:
        return True

    if (size - col_x) - row_x == (size - col_y) - row_y:
        return True

    return False


def spot_is_safe(row, column):
    # check column
    for next_queen_col in queen_array:
        if column == next_queen_col:
            return False

    # check diagonal
    for next_queen_row, next_queen_col in enumerate(queen_array):
        if next_queen_col - next_queen_row == column - row:
            return False

    # check other diagonal
    for next_queen_row, next_queen_col in enumerate(queen_array):
        if (size - next_queen_col) - next_queen_row == (size - column) - row:
            return False
    return True


def spot_is_safe_forward(row, col):
    if queen_array_mirror[row][col] != 0:
        return False
    return True


def verify_solution():
    for next_queen_row_x, next_queen_col_x in enumerate(queen_array):
        for next_queen_row_y, next_queen_col_y in enumerate(queen_array):
            if next_queen_row_x == next_queen_row_y:
                continue
            if does_conflict(next_queen_row_x, next_queen_col_x, next_queen_row_y, next_queen_col_y):
                return False
    return True


def display():
    for row in range(len(queen_array)):
        for column in range(size):
            if column == queen_array[row]:
                print(' ♛', end=' ')
            else:
                print(' .', end=' ')
        print()


def display_forward():
    for row in range(size):
        for col in range(size):
            print(" " + str(queen_array_mirror[row][col]), end=" ")
        print()
    print()


def run():
    global size
    size = int(input('Enter n: '))

    total_iterations = 0
    high_iterations = 0
    low_iterations = sys.maxsize

    total_moves = 0
    high_moves = 0
    low_moves = sys.maxsize

    for i in range(100):

        print("of 100: " + str(i))

        run_iterations = 0
        run_moves = 0
        solution = False
        solution, run_iterations, run_moves = forward_solution()

        total_iterations += run_iterations
        if run_iterations > high_iterations:
            high_iterations = run_iterations
        if run_iterations < low_iterations:
            low_iterations = run_iterations

        total_moves += run_moves
        if run_moves > high_moves:
            high_moves = run_moves
        if run_moves < low_moves:
            low_moves = run_moves

    print("total iterations: " + str(total_iterations))
    print("mean iterations: " + str(total_iterations / 100))
    print("high iterations: " + str(high_iterations))
    print("low iterations: " + str(low_iterations))

    print("\ntotal moves: " + str(total_moves))
    print("mean moves: " + str(total_moves / 100))
    print("high moves: " + str(high_moves))
    print("low moves: " + str(low_moves))
    print("most recent solution: ")
    display()


run()
