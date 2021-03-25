# backtracking algorithm
# concept: make a decision and then remember when you made it
# if that decision was wrong then go back to the place where you made that decision

# sudoku ruleset:
# each row must have digits through 1 to 9
# each column must have digits through 1 to 9
# each 3x3 square must have digits through 1 to 9
# each row, column and 3x3 square can only have one specific digit from 1 to 9

verbose_counter = 0


# reads from csv file - format each csv line is a line of sudoku puzzle
def read_from_file(file_name):
    f = open(file_name, "r")
    sudoku_numbers = f.read()
    sudoku_numbers = ''.join(c for c in sudoku_numbers if c.isdigit())
    sudoku_board = []
    line = []

    index_sudoku_board = 0

    for index in range(0, 81):
        line.append(int(sudoku_numbers[index]))
        if len(line) == 9:
            sudoku_board.append(line)
            index_sudoku_board += 1
            line = []

    return sudoku_board


def is_board_valid(given_board, given_digit, position):
    # row check
    for index in range(len(given_board[0])):
        if given_board[position[0]][index] == given_digit and position[1] != index:
            return False

    # column check
    for index in range(len(given_board)):
        if given_board[index][position[1]] == given_digit and position[0] != index:
            return False

    # subgrid check
    subgrid_x = position[1] // 3
    subgrid_y = position[0] // 3

    for index1 in range(subgrid_y * 3, subgrid_y * 3 + 3):
        for index2 in range(subgrid_x * 3, subgrid_x * 3 + 3):
            if given_board[index1][index2] == given_digit and (index1, index2) != position:
                return False

    return True


def print_board(given_board):
    for i in range(len(given_board)):
        if i % 3 == 0 and i != 0:
            print("-"*23)

        for j in range(len(given_board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(str(given_board[i][j]))
            else:
                print(str(given_board[i][j]) + " ", end="")


def verbose_print_board(given_board):
    for i in range(len(given_board)):
        if i % 3 == 0 and i != 0:
            print("-"*23)

        for j in range(len(given_board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                if given_board[i][j] == 0:
                    print("#")
                else:
                    print(str(given_board[i][j]))
            else:
                if given_board[i][j] == 0:
                    print("#" + " ", end="")
                else:
                    print(str(given_board[i][j]) + " ", end="")


# noinspection PyRedundantParentheses
def find_empty(given_board):
    for i in range(len(given_board)):
        for j in range(len(given_board[0])):
            if given_board[i][j] == 0:
                return (i, j)   # row, column
    return None


# recursive
# works in the same fashion as backtracking_algorithm_sudoku_solve but provides an output on every decision taken
def verbose_backtracking_algorithm_sudoku_solve(given_board):
    global verbose_counter
    print(f"Attempt no. {verbose_counter}")
    verbose_print_board(given_board)
    print()
    verbose_counter += 1

    find = find_empty(given_board)
    if not find:
        return True
    else:
        row, column = find

    for digit in range(1, 10):
        if is_board_valid(given_board, digit, (row, column)):
            given_board[row][column] = digit

            if verbose_backtracking_algorithm_sudoku_solve(given_board):
                return True
            given_board[row][column] = 0

    return False


# recursive
# returns True if there are no empty squares left in the 9x9 sudoku grid
# returns False if the current grid state is not valid i.e. there are more than one digits from
# [1, 2, 3, 4, 5, 6, 7, 8, 9] set in the position dependant row, column or subgrid (3x3)
def backtracking_algorithm_sudoku_solve(given_board):
    empty_position = find_empty(given_board)
    if not empty_position:
        return True
    else:
        row, column = empty_position

    for digit in range(1, 10):
        if is_board_valid(given_board, digit, (row, column)):
            given_board[row][column] = digit

            if backtracking_algorithm_sudoku_solve(given_board):
                return True
            given_board[row][column] = 0

    return False


def main():
    sudoku = read_from_file("Assets/test_sudoku.csv")

    print_board(sudoku)
    backtracking_algorithm_sudoku_solve(sudoku)
    print()
    print_board(sudoku)
