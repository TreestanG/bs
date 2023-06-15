import pygame
import time
import random
from pygame.locals import *
from definitions import *
from tetris_classes import *

pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris - lol")
clock = pygame.time.Clock()


class Tetris:
    def __init__(self):
        self.current_block = TetrisBlock(5, 1, self.shape())
        self.move_start_time = 0

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

    def draw_past_blocks(self):
        for row in range(len(tetris_matrix)):
            for col in range(len(tetris_matrix[row])):
                if tetris_matrix[row][col] != 0:
                    pygame.draw.rect(window, bricks[tetris_matrix[row][col]], (self.tetris_coords("x", col+2),
                                     self.tetris_coords("y", row), block_size, block_size))

    def shape(self):
        bag = []
        for shape in range(len(shapes.keys())):
            bag.append(random.choice(list(shapes.keys())))
            bag.append(random.choice(list(shapes.keys())))

        if len(bag) > 0:
            return bag.pop(random.choice(range(len(bag))))
        else:
            for shape in range(len(shapes.keys())):
                bag.append(random.choice(list(shapes.keys())))
                bag.append(random.choice(list(shapes.keys())))
            return bag.pop(random.choice(range(len(bag))))

    def block_fits(self):
        available_spaces = []

        for row in range(len(tetris_matrix)):
            for col in range(len(tetris_matrix[row])):
                if tetris_matrix[row][col] == 0:
                    available_spaces.append((col+1, row+1))

        for coord in self.current_block.block_coords:
            if not (coord[0], coord[1]+1) in available_spaces:
                return False
        return True

    def handle_input(self, event):

        if event.type == KEYDOWN:
            self.move_start_time = pygame.time.get_ticks()
            if event.key == K_SPACE:
                while not self.current_block.check_collision("v") and not self.current_block.block_collision():
                    self.current_block.move_down()

                self.current_block.write_block()
                self.current_block.reached_bottom = True
                self.current_block.new_block = True
                self.move_start_time = pygame.time.get_ticks()
        elif event.type == KEYUP:
            if self.move_start_time != 0 and pygame.time.get_ticks() - self.move_start_time >= 300:
                if event.key == K_DOWN:
                    if not self.current_block.check_collision("v"):
                        self.current_block.move_down()
                    self.move_start_time = pygame.time.get_ticks()
                if event.key == K_LEFT:
                    if not self.current_block.check_collision("l"):
                        self.current_block.move_left()
                    self.move_start_time = pygame.time.get_ticks()
                if event.key == K_RIGHT:
                    if not self.current_block.check_collision("r"):
                        self.current_block.move_right()
                    self.move_start_time = pygame.time.get_ticks()

            else:
                if event.key == K_DOWN:
                    self.current_block.move_down()
                if event.key == K_LEFT:
                    self.current_block.move_left()
                if event.key == K_RIGHT:
                    self.current_block.move_right()
            if event.key == K_UP:
                self.current_block.rotate_cw()
    
    def check_full_rows(self):
        for row in tetris_matrix:
            if not (0 in row):
                tetris_matrix.pop(tetris_matrix.index(row))
                tetris_matrix.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def run(self):
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                self.handle_input(event)

            window.fill((0, 0, 0))
            self.draw_board()
            self.draw_past_blocks()
            self.check_full_rows()
            self.check_game_over()
            self.current_block.draw_shape(
                self.tetris_coords("x", self.current_block.x),  # 340
                self.tetris_coords("y", self.current_block.y),  # 30
                self.current_block.color, window
            )
            self.current_block.update()
            if self.current_block.new_block:
                self.current_block = TetrisBlock(5, 1, self.shape())
            pygame.display.flip()
            pygame.display.update()
            clock.tick(60)

        pygame.quit()


tetrisBoard = Tetris()
tetrisBoard.run()
