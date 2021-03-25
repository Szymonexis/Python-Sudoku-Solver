import pygame
import os
import sys

# init pygame
pygame.init()

# game specific variables
fps = 30
tile_width, tile_height = 100, 100
sudoku_file_name = os.path.join("Assets", "test_sudoku.csv")

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
resize_w, resize_h = width / 12, height / 12
flags = pygame.RESIZABLE   # TODO add later - find out how to get current window size
screen = pygame.display.set_mode((width, height), flags)
background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.jpg")), (width, height))

pygame.display.set_caption("Sudoku")
icon = pygame.image.load(os.path.join("Assets", "icon_sudoku.png"))     # TODO find a working .png for icon
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


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
            line.append(" ")
        if len(line) == 9:
            sudoku_board.append(line)
            index_sudoku_board += 1
            line = []

    return sudoku_board


def draw_screen(sudoku_grid):
    screen.blit(background, (0, 0))

    pos_x = 0
    pos_y = 0
    for i in range(len(sudoku_grid)):
        for j in range(len(sudoku_grid[0])):
            if j == 8:
                Tile(black, pos_x, pos_y, str(sudoku_grid[i][j]))
                pos_y += int(resize_h * 130)
                pos_x = 0
            else:
                Tile(black, pos_x, pos_y, str(sudoku_grid[i][j]))
                pos_x += int(resize_w * 130)

    for line in range(0, 10):
        LinesVertical(line)
        LinesHorizontal(line)

    pygame.display.update()


def main():
    global resize_w, resize_h, width, height, background
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

        draw_screen(read_from_file(sudoku_file_name))
    main()


if __name__ == "__main__":
    main()
