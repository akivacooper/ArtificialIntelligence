##########################################
# INSTRUCTION SECTION
##########################################
"""There are five sections to my code
   1. Instruction Section
   2. Global Variable Section
   3. General Use Function Section
   4. Solution Section
   5. Run Section

See the Solution Section for the different solutions I've implemented.
Descriptions of each solution are above the function.
To test a solution, copy the solution name, and paste it into the run function in the Run Section
Note that solutions have variable number of handles which can be customized (like how many tries before a new iteration, and how many queens to place down each iteration).
See the description above each solution for the handles avaliable, and where to find them.
The General Use Function Section are for general use functions. Although 'general use' some solutions required specialized 'general' functions.
See the description above each solution in the Solution Section to see which general use functions a method uses

"""

##########################################
# GLOBAL VARIABLE SECTION
##########################################

# columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
# hint -- you will need this for the following code: column=random.randrange(0,size)

import random
import sys

size = 0
queen_array = []
queen_array_mirror = [[]]


##########################################
# GENERAL USE FUNCTIONS SECTION
##########################################

'''
Assess:
    1. The conflicts of each queen. 
    2. The best coloumn to move each queen to. Meaning, the column in which each queen will conflict the least
    3. The conflicts incurred for moving each queen to it's respective column in #2
Returns a map of {queen: -> [#1, #2, #3] 
'''
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

            # best_col_score must be the best column aside the current column
            if next_col_score < best_col_score:
                best_col = next_col
                best_col_score = next_col_score

        rated_queens[next_queen_row_x] = [current_score, best_col, best_col_score]

    rated_queens_sorted = {k: v for k, v in sorted(rated_queens.items(), key=lambda item: item[1])}
    rated_queens_sorted_reversed = dict(reversed(list(rated_queens_sorted.items())))

    return rated_queens_sorted_reversed


'''
Given a map, and the API of the 'rate_queens' method, return the queen which conflicts the most
'''
def find_worst_queen(rated_queens_map):
    for next_row in rated_queens_map:

        next_queen_values = rated_queens_map.get(next_row)

        # by definition, the best column [2] must be a column other than the current
        if next_queen_values[0] >= next_queen_values[2]:
            return next_row


'''
Given a map defined by the API in 'rate_queens' determines if the map indicates a local max.
Local max is determined if for each queen, #3--as determined by the 'rate_queens' API is worse than #1
This is a local max because this indicates that each queen can only worsen the board by moving
'''
def at_local_max(rated_queens):
    for next_row in rated_queens:

        next_queen_values = rated_queens.get(next_row)

        # by definition, the best column [2] must be a column other than the current
        if next_queen_values[0] >= next_queen_values[2]:
            return False

    return True

'''
Appends a row to the board, and places the queen into the row with the inputed coloumn
'''
def place_in_next_col(column):
    queen_array.append(column)

'''
The equivilant method of 'place_in_next_col' for the 'forward_solution'
The 'forward solution requires its own method because for each addition and removal of queens, the mirror board needs updating 
'''
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



'''
Removes the last row of the board, or returns -1 if there are no rows
'''
def remove_in_current_row():
    if len(queen_array) > 0:
        return queen_array.pop()
    return -1

'''
The equivilant method of 'remove_in_current_row' for the 'forward_solution'
The 'forward solution requires its own method because for each addition and removal of queens, the mirror board needs updating 
'''
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


'''
takes in two 'row' parameters, and two 'col' parameters, does appropriate math, and determines if the two boxes conflict with one another
true if a conflict, false if not
'''
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

'''
Similar to does_conflict, this function does not take in the coordinates of two boxes, but only one
With the coordinates of one box, it runs through the board, and checks whether ther are other queens that conflict with the inputed box
Returns false if there is a conflict, true otherwise
'''
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

'''
The equivilant method of 'spot_is_safe' for the 'forward_solution'
The 'forward' solution requires its own method because it checks the mirror board, and not the actual board
'''
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


'''
The equivilant method of 'display' for the 'forward_solution'
The 'forward' solution requires its own method because it prints the mirror board instead of the actual board (the mirror board shows the number of conficts for each box)
'''
def display_forward():
    for row in range(size):
        for col in range(size):
            print(" " + str(queen_array_mirror[row][col]), end=" ")
        print()
    print()

'''
randomly places queens
'''
def place_n_queens():
    queen_array.clear()
    row = 0
    while row < size:
        column = random.randrange(0, size)
        queen_array.append(column)
        row += 1

'''
Yair Caplan's idea.
Thought to improve results by refusing to place queens in a column already taken. 
Did not show better results, and was not used
'''
def place_n_queens_better():
    queen_array.clear()
    row_left = []

    i = 0
    for i in range(size):
        row_left.append(i)
        i += 1

    row = 0
    while row < size:
        index = random.randrange(0, len(row_left))
        column = row_left[index]
        queen_array.append(column)
        row_left.remove(column)
        row += 1


##########################################
# SOLUTION SECTION
##########################################

'''
Description: Throws down 'size' number of queens until a solution is found
Handles: - 
General Use Functions Used: 
    1. place_n_queens
    2. verify_solution
'''

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


'''
Description: Does DFS on the search space to find the correct solution.
Handles: - 
General Use Functions Used: 
    1. splot_is_safe
    2. place_in_next_col
    3. remove_in_cur_row
'''

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


'''
Description: 
    1. Throws down 'size' number of queens. 
    2. Assesses each queen, ordering them by how problematic they are.
    3. Moves a given number of queens, starting from most problematic, to locations that are least problematic
    4. Continiously does 2-3 for a given number of times
    5. Starts again from 1 until a solution is found
Handles:
    1. iterations before restart
    2. queens to move before new iteration
General Use Functions Used: 
    1. place_n_queens
    2. rate_queens
    3. verify_solution
'''

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

        for x in range(size):

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


'''
Description: 
    1. Same description as 'heuristic_solution'
    2. Revise line 3 in the 'heuristic solution' to the following: Continiously does 2-3 for a given number of times, OR UNTIL A LOCAL MAX IS REACHED
Handles:
    1. iterations before restart
    2. queens to move before new iteration
General Use Functions Used: 
    1. place_n_queens
    2. rate_queens
    3. verify_solution
'''
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

        for counter in range(size):

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

'''
Description: 
 1. Same description as 'heuristic_solution'
 2. Revise line 3 in the 'heuristic solution' to the following: Continiously does 2-3 UNTIL A LOCAL MAX IS REACHED
Handles: - 
General Use Functions Used: 
    1. place_n_queens
    2. rate_queens
    3. verify_solution
    4. find_worst_queen
'''

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

'''
Description: 
    1. Same description as 'heuristic_solution' 
    2. Revise line 2 in the 'heuristic solution' to the following: Assesses each queen, ordering them by their best available coloumn
Handles:
    1. iterations before restart
    2. queens to move before new iteration
General Use Functions Used: 
    1. place_n_queens
    2. rate_queens
    3. verify_solution
'''

def opposite_heuristic_solution():
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

        for x in range(size):

            # print("assessment: " + str(counter))
            rated_queens_map = rate_queens()
            rated_queens_sorted = {k: v for k, v in sorted(rated_queens_map.items(), key=lambda item: item[1][2])}
            rated_queens_rows = list(rated_queens_sorted)

            for y in range(1):
                worst_queen_row = rated_queens_rows[size - 1 - y]
                queen_array[worst_queen_row] = rated_queens_map.get(worst_queen_row)[1]
                number_moves += 1

                if verify_solution():
                    solution_found = True
                    break

    return True, number_iterations, number_moves

'''
Description: The forward solution described in class
    1. I'm not sure how much you want me to describe here, as we discussed it extensively in class
    2. All I could offer is a summary of the algorithm
    3. This is, at it's core a DFS algorithm. 
    4. Each box has a score, starting off at 0
    4. For each queen placed down, run through each  conflicting box in the mirror board, and add one to its score
    5. For each queen, only place down in a box whose score is 0. Then update all box scores on the board
    6. If there are not available boxes in the row with a score of 0 in the mirror board, continue through the search space using DFS
    7. When removing peices, make sure to remove them from the mirror board.
    8. This means, after removing the piece, run through the mirror board and decrement the score of each conflicting box
Handles: - 
General Use Functions Used: 
    1. spot_is_safe_forward
    2. place_in_spot_forward
    3. remove_in_current_row_forward
'''

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

##########################################
# RUN SECTION
##########################################

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
        solution, run_iterations, run_moves = opposite_heuristic_solution()

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
