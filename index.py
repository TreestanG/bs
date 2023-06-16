import pygame, pygame.freetype
import time
import random
from pygame.locals import *
from definitions import *
from tetris_classes import *

pygame.init()
window_width = 900
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris - lol")
clock = pygame.time.Clock()
game_over_font = pygame.freetype.Font("Tetris.ttf", 96)
game_font = pygame.freetype.Font("Tetris.ttf", 36)


class Tetris:
    def __init__(self):
        self.bag = self.create_bag()
        self.current_block = TetrisBlock(5, 1, self.shape())
        self.move_start_time = 0
        self.held_block = False

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
                    
    def create_bag(self):
        bag = random.sample(list(shapes.keys()), 7)
        for a in random.sample(list(shapes.keys()), 7):
            bag.append(a)
        return bag
    
    def shape(self):
        if len(self.bag) > 0:
            return self.bag.pop(0)
        else:
            self.bag = self.create_bag()
            return self.bag.pop(0)
    
    def draw_next_blocks(self):
        for i in self.bag[0:3]:
            ind = self.bag.index(i)
            self.current_block.draw_shape(
                self.tetris_coords("x", 13), 
                self.tetris_coords("y", 3+ind*4), 
                shape_colors[self.bag[ind]], 
                window,
                shapes[i][0]
            )

    def block_fits(self):
        available_spaces = self.current_block.create_available()

        for coord in self.current_block.block_coords:
            if not (coord[0], coord[1]+1) in available_spaces:
                return False
        return True

    def handle_input(self, event):

        keys = pygame.key.get_pressed()
        self.move_start_time = pygame.time.get_ticks()

        while not pygame.time.get_ticks() - self.move_start_time < 300:
            if keys[K_LEFT]:
                self.current_block.move_left()
            if keys[K_RIGHT]:
                self.current_block.move_right()
            if keys[K_DOWN]:
                self.current_block.move_down()
            if keys[K_UP]:
                self.current_block.rotate()
            if keys[K_SPACE]:
                self.current_block.hard_drop()
        else:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.current_block.move_left()
                if event.key == K_RIGHT:
                    self.current_block.move_right()
                if event.key == K_DOWN:
                    self.current_block.move_down()
                if event.key == K_UP:
                    self.current_block.rotate_cw()
                if event.key == K_SPACE:
                    self.current_block.hard_drop()
                if event.key == K_c:
                    if not self.held_block:
                        self.held_block = TetrisBlock(5, 1, self.current_block.shape)
                        self.current_block = TetrisBlock(5,1, self.shape())
                    else:
                        held = self.current_block
                        self.current_block = self.held_block
                        self.held_block = held
            if event.type == MOUSEBUTTONDOWN and self.current_block.game_over:
                self.__init__()
                tetris_matrix = [[0 for i in range(10)] for j in range(20)]
                self.draw_past_blocks()


    
    def draw_held(self):
        if self.held_block:
            self.current_block.draw_shape(
                self.tetris_coords("x", -3),
                self.tetris_coords("y", 6),
                shape_colors[self.held_block.shape],
                window,
                shapes[self.held_block.shape][0]
            )
    
    def check_full_rows(self):
        for row in tetris_matrix:
            if not (0 in row):
                tetris_matrix.pop(tetris_matrix.index(row))
                tetris_matrix.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def draw_text(self):
        game_font.render_to(window, (100, 90), "Hold", (255, 255, 255))
        game_font.render_to(window, (575, 20), "Next", (255, 255, 255))


    def check_game_over(self):
        if self.current_block.game_over:
            game_over_font.render_to(window, (100, 200), "GAME OVER", (255, 255, 255))
            pygame.display.flip()

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
            self.draw_next_blocks()
            self.draw_held()
            self.check_full_rows()
            self.draw_text()
            self.current_block.draw_shape(
                self.tetris_coords("x", self.current_block.x),  # 340
                self.tetris_coords("y", self.current_block.y),  # 30
                self.current_block.color, window,
            )
            self.check_game_over()
            self.current_block.update(1250)
            if self.current_block.new_block:
                self.current_block = TetrisBlock(5, 1, self.shape())
            pygame.display.flip()
            pygame.display.update()
            clock.tick(60)

        pygame.quit()


tetrisBoard = Tetris()
tetrisBoard.run()
