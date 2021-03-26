import pygame
import os
import sys
from algorithm import backtracking_algorithm_sudoku_solve

# init pygame
pygame.init()

# game specific variables
fps = 120
tile_width, tile_height = 100, 100
sudoku_file_name = os.path.join("Assets", "test_sudoku.csv")
mouse_x, mouse_y = 0, 0
number_buttons = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                  pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
keyboard_digit = 0
PLAYER_WON = pygame.USEREVENT + 1
COMPUTER_WON = pygame.USEREVENT + 2


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


class Tile:
    def __init__(self, border_color, position_x, position_y, digit, index):
        self.position_x_begin = position_x
        self.position_x_end = position_x + int(resize_w * 100)

        self.position_y_begin = position_y
        self.position_y_end = position_y + int(resize_h * 100)

        self.index = index

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
        self.active = False

    def change_state(self):
        self.active = True


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
        line.append(int(sudoku_numbers[index]))
        if len(line) == 9:
            sudoku_board.append(line)
            index_sudoku_board += 1
            line = []

    return sudoku_board


def draw_screen(sudoku_grid, mouse_x, mouse_y, given_digit, changeable_indexes):
    screen.blit(background, (0, 0))

    pos_x = 0
    pos_y = 0
    for row in range(len(sudoku_grid)):
        for column in range(len(sudoku_grid[0])):
            sudoku_digit = sudoku_grid[row][column]
            if sudoku_grid[row][column] == 0:
                sudoku_digit = " "

            if column == 8:
                Tile(black, pos_x, pos_y, str(sudoku_digit), (row, column))
                # TODO figure out how to change this behaviour
                if (pos_x + int(resize_w * 30)) <= mouse_x <= (pos_x + int(resize_w * 130)) and \
                        (pos_y + int(resize_h * 30)) <= mouse_y <= (pos_y + int(resize_h * 130)):
                    Tile(green, pos_x, pos_y, str(sudoku_digit), (row, column)).change_state()
                    if (row, column) in changeable_indexes:
                        sudoku_grid[row][column] = given_digit

                pos_y += int(resize_h * 130)
                pos_x = 0
            else:
                Tile(black, pos_x, pos_y, str(sudoku_digit), (row, column))
                if (pos_x + int(resize_w * 30)) <= mouse_x <= (pos_x + int(resize_w * 130)) and \
                        (pos_y + int(resize_h * 30)) <= mouse_y <= (pos_y + int(resize_h * 130)):
                    Tile(green, pos_x, pos_y, str(sudoku_digit), (row, column)).change_state()
                    if (row, column) in changeable_indexes:
                        sudoku_grid[row][column] = given_digit

                pos_x += int(resize_w * 130)

    for line in range(0, 10):
        LinesVertical(line)
        LinesHorizontal(line)

    pygame.display.update()


def check_if_grid_correct(given_solved_sudoku_grid, given_sudoku_grid):
    for row in range(len(given_solved_sudoku_grid)):
        for column in range(len(given_solved_sudoku_grid[0])):
            if given_solved_sudoku_grid[row][column] != given_sudoku_grid[row][column]:
                given_sudoku_grid[row][column] = 0


def game_end(given_message):
    screen.blit(background, (0, 0))

    font = pygame.font.SysFont('comicsans', int(resize_w * 75))
    screen.blit(font.render(str(given_message), True, black), (int(resize_w * 425),
                                                               int(resize_h * 575),
                                                               resize_w * 350, resize_h * 50))


# creation of the sudoku board from file and changeable indexes marking
sudoku_board = read_from_file(sudoku_file_name)
changeable_indexes = []
for i in range(len(sudoku_board)):
    for j in range(len(sudoku_board[0])):
        if sudoku_board[i][j] == 0:
            changeable_indexes.append((i, j))

solved_sudoku_board = read_from_file(sudoku_file_name)
backtracking_algorithm_sudoku_solve(solved_sudoku_board)


def main():
    global resize_w, resize_h, width, height, background, mouse_x, mouse_y, number_buttons, keyboard_digit
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
                    keyboard_digit = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mouse_x, mouse_y = 0, 0
                    backtracking_algorithm_sudoku_solve(sudoku_board)
                    # game_end("Computer won :c")
                    # pygame.quit()
                    # return

                if event.key in number_buttons:
                    keyboard_digit = event.key - 48

                if event.key == pygame.K_RETURN:
                    mouse_x, mouse_y = 0, 0
                    check_if_grid_correct(solved_sudoku_board, sudoku_board)

        draw_screen(sudoku_board, mouse_x, mouse_y, keyboard_digit, changeable_indexes)
    main()


if __name__ == "__main__":
    main()
