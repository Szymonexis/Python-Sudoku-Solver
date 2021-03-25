import pygame
import os
import sys

# init pygame
pygame.init()

# game specific variables
fps = 30
tile_width, tile_height = 100, 100
sudoku_file_name = os.path.join("Assets", "test_sudoku.csv")
mouse_x, mouse_y = 0, 0

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)

# screen creation
width, height = 1200, 1200
resize_w, resize_h = 1, 1
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((width, height), flags)
background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.jpg")), (width, height))

pygame.display.set_caption("Sudoku")
icon = pygame.image.load(os.path.join("Assets", "icon_sudoku.png"))  # TODO find a working .png for icon
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


def find_empty(given_board):
    for i in range(len(given_board)):
        for j in range(len(given_board[0])):
            if given_board[i][j] == 0:
                return (i, j)   # row, column
    return None


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


class Tile:
    def __init__(self, border_color, position_x, position_y, digit):
        self.font = pygame.font.SysFont('comicsans', int(resize_w * 75))
        self.tile_border = pygame.draw.rect(screen, border_color, (int(position_x + resize_w * 30),
                                                                   int(position_y + resize_h * 30),
                                                                   int(resize_w * 100),
                                                                   int(resize_h * 100)),
                                            int(resize_w * 2))

        self.tile_fill = pygame.draw.rect(screen, white, (int(position_x + resize_w * 32),
                                                          int(position_y + resize_h * 32),
                                                          int(resize_w * 96),
                                                          int(resize_h * 96)))
        screen.blit(self.font.render(str(digit), True, black), (int(position_x + resize_w * 65),
                                                                int(position_y + resize_h * 60),
                                                                resize_w * 50, resize_h * 50))


class LinesVertical:
    def __init__(self, line_num):
        if line_num in (0, 3, 6, 9):
            self.vertical = pygame.draw.rect(screen, black, (int(resize_w * 130 * line_num + resize_w * 12),
                                                             int(resize_h * 12),
                                                             int(resize_w * 6),
                                                             int(resize_h * 1176)))
        else:
            self.vertical = pygame.draw.rect(screen, black, (int(resize_w * 130 * line_num + resize_w * 12),
                                                             int(resize_h * 12),
                                                             int(resize_w * 2),
                                                             int(resize_h * 1176)))


class LinesHorizontal:
    def __init__(self, line_num):
        if line_num in (0, 3, 6, 9):
            self.horizontal = pygame.draw.rect(screen, black, (int(resize_w * 12),
                                                               int(resize_h * 130 * line_num + resize_h * 12),
                                                               int(resize_w * 1176),
                                                               int(resize_h * 6)))
        else:
            self.horizontal = pygame.draw.rect(screen, black, (int(resize_w * 12),
                                                               int(resize_h * 130 * line_num + resize_h * 12),
                                                               int(resize_w * 1176),
                                                               int(resize_h * 2)))


def read_from_file(file_name):
    f = open(file_name, "r")
    sudoku_numbers = f.read()
    sudoku_numbers = ''.join(c for c in sudoku_numbers if c.isdigit())
    sudoku_board = []
    line = []

    index_sudoku_board = 0

    for index in range(0, 81):
        if int(sudoku_numbers[index]) != 0:
            line.append(sudoku_numbers[index])
        else:
            line.append(0)
        if len(line) == 9:
            sudoku_board.append(line)
            index_sudoku_board += 1
            line = []

    return sudoku_board


def draw_screen(sudoku_grid, mouse_x, mouse_y):
    screen.blit(background, (0, 0))

    pos_x = 0
    pos_y = 0
    for i in range(len(sudoku_grid)):
        for j in range(len(sudoku_grid[0])):
            digit = sudoku_grid[i][j]
            # if sudoku_grid[i][j] == 0:
            #     digit = " "

            if j == 8:
                Tile(black, pos_x, pos_y, str(digit))
                # TODO figure out how to change this behaviour
                if (pos_x + int(resize_w * 30)) <= mouse_x <= (pos_x + int(resize_w * 130)) and \
                        (pos_y + int(resize_h * 30)) <= mouse_y <= (pos_y + int(resize_h * 130)):
                    Tile(green, pos_x, pos_y, str(digit))

                pos_y += int(resize_h * 130)
                pos_x = 0
            else:
                Tile(black, pos_x, pos_y, str(digit))
                if (pos_x + int(resize_w * 30)) <= mouse_x <= (pos_x + int(resize_w * 130)) and \
                        (pos_y + int(resize_h * 30)) <= mouse_y <= (pos_y + int(resize_h * 130)):
                    Tile(green, pos_x, pos_y, str(digit))

                pos_x += int(resize_w * 130)

    for line in range(0, 10):
        LinesVertical(line)
        LinesHorizontal(line)

    pygame.display.update()


# creation of the sudoku board from file
sudoku_board = read_from_file(sudoku_file_name)


def main():
    global resize_w, resize_h, width, height, background, mouse_x, mouse_y
    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.WINDOWRESIZED:
                surface_info = pygame.display.get_surface()
                width, height = surface_info.get_width(), surface_info.get_height()
                resize_w, resize_h = width / 1200, height / 1200
                background = pygame.transform.scale(background, (width, height))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #  TODO does only one pass through - fix
                    backtracking_algorithm_sudoku_solve(sudoku_board)

        draw_screen(sudoku_board, mouse_x, mouse_y)
    main()


if __name__ == "__main__":
    main()
