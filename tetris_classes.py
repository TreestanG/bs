import pygame
from definitions import *
import time

class tetris_piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect((self.x, self.y, block_size, block_size))

class TetrisBlock:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.color = shape_colors[shape]
        self.rotation = 0
        self.code = shapes[shape][self.rotation]
        self.group_bricks = []
        self.start_time = pygame.time.get_ticks()

    def rotate_cw(self):
        rotation += 1
        if rotation > 3:
            rotation = 0

    def rotate_ccw(self):
        rotation -= 1
        if rotation < 0:
            rotation = 3

    def move_down(self, multiplier=1):
        if not self.check_collision():
            self.y += 1*multiplier

    def check_collision(self):
        if self.y >= 19:
            return True
        elif self.x < 0 or self.x > 9:
            return True
        return False

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def draw_block(self, x, y, color, window):
        return pygame.draw.rect(window, color, tetris_piece(x,y))

    def draw_shape(self, x, y, color, window):
        for row in range(len(tetris_grid)):
            for e in range(len(tetris_grid[row])):
                if tetris_grid[row][e] in self.code:
                    (self.draw_block(x+(e)*block_size, y+(row-1)*block_size, color, window))
    
    def update(self):
        if pygame.time.get_ticks() - self.start_time > 1250:
            self.move_down()
            self.start_time = pygame.time.get_ticks()
    
    
