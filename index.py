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

    def handle_input(self, event, k_down_active):

        if event.type == KEYDOWN:
            if event.key == K_DOWN and not k_down_active >= 300:
                self.current_block.move_down()
                k_down_active = True
            if event.key == K_LEFT:
                self.current_block.move_left()
            if event.key == K_RIGHT:
                self.current_block.move_right()
            if event.key == K_UP:
                self.current_block.rotate_cw()
        elif event.type == KEYUP:
            if event.key == K_DOWN and k_down_active >= 300:
                k_down_active = 0

    def run(self):
        running = True
        k_down_tracker = 0

        while running:
            k_down_tracker += 30
           # print(k_down_tracker)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                self.handle_input(event, k_down_tracker)

            window.fill((0, 0, 0))
            self.draw_board()
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
