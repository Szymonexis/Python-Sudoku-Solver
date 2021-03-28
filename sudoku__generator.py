# Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
from random import randint, shuffle
from time import sleep


class SudokuGenerator:
    def __init__(self):
        # initialise empty 9 by 9 grid
        self.grid = []
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.counter = 1

    # A function to check if the grid is full
    def check_grid(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if self.grid[row][col] == 0:
                    return False

        # We have a complete grid!
        return True

    def check_grid_copy(self, copy_crid):
        for row in range(0, 9):
            for col in range(0, 9):
                if copy_crid[row][col] == 0:
                    return False

        # We have a complete grid!
        return True

    # A backtracking/recursive function to check all possible combinations of numbers until a solution is found
    def solve_grid(self):
        # global counter
        # Find next empty cell
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if self.grid[row][col] == 0:
                for value in range(1, 10):
                    # Check that this value has not already be used on this row
                    if not (value in self.grid[row]):
                        # Check that this value has not already be used on this column
                        if not value in (
                        self.grid[0][col], self.grid[1][col], self.grid[2][col], self.grid[3][col], self.grid[4][col], 
                        self.grid[5][col], self.grid[6][col], self.grid[7][col], self.grid[8][col]):
                            # Identify which of the 9 squares we are working on
                            square = []
                            if row < 3:
                                if col < 3:
                                    square = [self.grid[i][0:3] for i in range(0, 3)]
                                elif col < 6:
                                    square = [self.grid[i][3:6] for i in range(0, 3)]
                                else:
                                    square = [self.grid[i][6:9] for i in range(0, 3)]
                            elif row < 6:
                                if col < 3:
                                    square = [self.grid[i][0:3] for i in range(3, 6)]
                                elif col < 6:
                                    square = [self.grid[i][3:6] for i in range(3, 6)]
                                else:
                                    square = [self.grid[i][6:9] for i in range(3, 6)]
                            else:
                                if col < 3:
                                    square = [self.grid[i][0:3] for i in range(6, 9)]
                                elif col < 6:
                                    square = [self.grid[i][3:6] for i in range(6, 9)]
                                else:
                                    square = [self.grid[i][6:9] for i in range(6, 9)]
                            # Check that this value has not already be used on this 3x3 square
                            if not value in (square[0] + square[1] + square[2]):
                                self.grid[row][col] = value
                                if self.check_grid():
                                    self.counter += 1
                                    break
                                else:
                                    if self.solve_grid():
                                        return True
                break
        self.grid[row][col] = 0

    def solve_grid_copy(self, copy_grid):
        # global counter
        # Find next empty cell
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if copy_grid[row][col] == 0:
                for value in range(1, 10):
                    # Check that this value has not already be used on this row
                    if not (value in copy_grid[row]):
                        # Check that this value has not already be used on this column
                        if not value in (
                                copy_grid[0][col], copy_grid[1][col], copy_grid[2][col], copy_grid[3][col], copy_grid[4][col],
                                copy_grid[5][col], copy_grid[6][col], copy_grid[7][col], copy_grid[8][col]):
                            # Identify which of the 9 squares we are working on
                            square = []
                            if row < 3:
                                if col < 3:
                                    square = [copy_grid[i][0:3] for i in range(0, 3)]
                                elif col < 6:
                                    square = [copy_grid[i][3:6] for i in range(0, 3)]
                                else:
                                    square = [copy_grid[i][6:9] for i in range(0, 3)]
                            elif row < 6:
                                if col < 3:
                                    square = [copy_grid[i][0:3] for i in range(3, 6)]
                                elif col < 6:
                                    square = [copy_grid[i][3:6] for i in range(3, 6)]
                                else:
                                    square = [copy_grid[i][6:9] for i in range(3, 6)]
                            else:
                                if col < 3:
                                    square = [copy_grid[i][0:3] for i in range(6, 9)]
                                elif col < 6:
                                    square = [copy_grid[i][3:6] for i in range(6, 9)]
                                else:
                                    square = [copy_grid[i][6:9] for i in range(6, 9)]
                            # Check that this value has not already be used on this 3x3 square
                            if not value in (square[0] + square[1] + square[2]):
                                copy_grid[row][col] = value
                                if self.check_grid_copy(copy_grid):
                                    self.counter += 1
                                    break
                                else:
                                    if self.solve_grid_copy(copy_grid):
                                        return True
                break
        self.grid[row][col] = 0

    # A backtracking/recursive function to check all possible combinations of numbers until a solution is found
    def fill_grid(self):
        # global counter
        # Find next empty cell
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if self.grid[row][col] == 0:
                shuffle(self.numberList)
                for value in self.numberList:
                    # Check that this value has not already be used on this row
                    if not (value in self.grid[row]):
                        # Check that this value has not already be used on this column
                        if not value in (
                        self.grid[0][col], self.grid[1][col], self.grid[2][col], self.grid[3][col], self.grid[4][col], 
                        self.grid[5][col], self.grid[6][col], self.grid[7][col], self.grid[8][col]):
                            # Identify which of the 9 squares we are working on
                            square = []
                            if row < 3:
                                if col < 3:
                                    square = [self.grid[i][0:3] for i in range(0, 3)]
                                elif col < 6:
                                    square = [self.grid[i][3:6] for i in range(0, 3)]
                                else:
                                    square = [self.grid[i][6:9] for i in range(0, 3)]
                            elif row < 6:
                                if col < 3:
                                    square = [self.grid[i][0:3] for i in range(3, 6)]
                                elif col < 6:
                                    square = [self.grid[i][3:6] for i in range(3, 6)]
                                else:
                                    square = [self.grid[i][6:9] for i in range(3, 6)]
                            else:
                                if col < 3:
                                    square = [self.grid[i][0:3] for i in range(6, 9)]
                                elif col < 6:
                                    square = [self.grid[i][3:6] for i in range(6, 9)]
                                else:
                                    square = [self.grid[i][6:9] for i in range(6, 9)]
                            # Check that this value has not already be used on this 3x3 square
                            if not value in (square[0] + square[1] + square[2]):
                                self.grid[row][col] = value
                                if self.check_grid():
                                    return True
                                else:
                                    if self.fill_grid():
                                        return True
                break
        self.grid[row][col] = 0

    def create_solvable_sudoku(self):
        self.fill_grid()

        # Start Removing Numbers one by one

        # A higher number of attempts will end up removing more numbers from the grid
        # Potentially resulting in more difficiult grids to solve!
        attempts = 5
        self.counter = 1
        while attempts > 0:
            # Select a random cell that is not already empty
            row = randint(0, 8)
            col = randint(0, 8)
            while self.grid[row][col] == 0:
                row = randint(0, 8)
                col = randint(0, 8)
            # Remember its cell value in case we need to put it back
            backup = self.grid[row][col]
            self.grid[row][col] = 0

            # Take a full copy of the grid
            copy_grid = []
            for r in range(0, 9):
                copy_grid.append([])
                for c in range(0, 9):
                    copy_grid[r].append(self.grid[r][c])

            # Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
            self.counter = 0
            self.solve_grid_copy(copy_grid)
            # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
            if self.counter != 1:
                self.grid[row][col] = backup
                # We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
                attempts -= 1


def get_sudoku():
    sudoku_grid = SudokuGenerator()
    sudoku_grid.create_solvable_sudoku()
    return sudoku_grid.grid
