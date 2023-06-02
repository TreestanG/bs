import pygame
import sched
import time
import random
from pygame.locals import *

pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

shape_colors = {
    "I": CYAN,
    "O": YELLOW,
    "T": MAGENTA,
    "L": ORANGE,
    "J": BLUE,
    "S": GREEN,
    "Z": RED
}

block_size = 30
shape_size = 4


shapes = {
    "I": [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    "O": [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    "T": [
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    "L": [
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ],
    "J": [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ],
    "S": [
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    "Z": [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
}


class TetrisBlock:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shape]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(shapes[self.shape])

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def update_board(self, scheduler):
        scheduler.enter(1.25, 1, self.update_board, (scheduler,))
        self.move_down()

        my_scheduler = sched.scheduler(time.time, time.sleep)
        my_scheduler.enter(1.25, 1, self.update_board, (my_scheduler,))
        my_scheduler.run()


class Tetris:
    def __init__(self):
        self.board_width = 10
        self.board_height = 20
        self.block_shape = 30
        self.shape_size = 4
        self.board = [[0 for x in range(self.board_width)]
                      for y in range(self.board_height)]
        self.current_block = TetrisBlock(5, 1, self.shape())

    def draw_block(self, x, y, color):
        pygame.draw.rect(window, color, (x, y, block_size, block_size))
        pygame.draw.rect(window, (41, 44, 53),
                         (x, y, block_size, block_size), 1)
        return

    def draw_shape(self, x, y, shape, color):
        for row in range(shape_size):
            for col in range(shape_size):
                if shape[row][col]:
                    self.draw_block(x + col * block_size, y +
                                    row * block_size, color)

    def draw_board(self):
        window.fill(BLACK)
        windowDimensions = {"x": block_size*10, "y": block_size*20}
        pygame.draw.rect(window, (41, 44, 53), (250, 0,
                         windowDimensions["x"], windowDimensions["y"]))

        for i in range(250, 550, block_size):
            pygame.draw.line(window, (75, 75, 75), (i, 0),
                             (i, windowDimensions["y"]), 1)
        for y in range(0, 600, block_size):
            pygame.draw.line(window, (75, 75, 75), (250, y), (550, y), 1)

    def tetris_coords(self, label, number):
        if label == "x":
            return 250 + (number-2)*block_size
        elif label == "y":
            return (number)*block_size

    def shape(self):
        return random.choice(list(shapes.keys()))

    def generate_block(self):
        x = self.board_width // 2
        y = 0
        shape = self.shape()
        return TetrisBlock(x, y, shape)

    def run(self):
        running = True
        self.current_block = self.generate_block()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_board()
            self.draw_shape(
                self.tetris_coords("x", self.current_block.x),
                self.tetris_coords("y", self.current_block.y),
                shapes[self.current_block.shape],
                self.current_block.color
            )

            pygame.display.update()

        pygame.quit()


tetrisBoard = Tetris()
tetrisBoard.run()
