import pygame
from definitions import *

class tetris_piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect((self.x, self.y, block_size, block_size))

class TetrisBlock:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shape]
        self.rotation = 0
        self.code = shapes[shape][self.rotation]
        self.group_bricks = []
        self.start_time = pygame.time.get_ticks()
        self.new_block = False
        self.reached_bottom = False

    def rotate_cw(self):
        self.rotation += 1
        if self.rotation > 3:
            self.rotation = 0
        self.code = shapes[self.shape][self.rotation]

    def rotate_ccw(self):
        self.rotation -= 1
        if self.rotation < 0:
            self.rotation = 3
        self.code = shapes[self.shape][self.rotation]

    def move_down(self):
        print(self.check_collision(), self.reached_bottom)
        if not self.check_collision() or not self.reached_bottom:
            print('isnt')
            self.y += 1
        elif self.reached_bottom: 
            print('elif')
            self.new_block = True

    def check_collision(self):
        check_left = dimensions[self.shape][0][self.rotation]+2
        check_right = 10 - dimensions[self.shape][1][self.rotation]
        if self.y >= 19:
            self.y = 19
            self.reached_bottm = True
            return True
        elif self.x <= check_left:
            return True
        elif self.x >= check_right:
            return True
        return False

    def move_left(self):
        if (self.check_collision() and not self.reached_bottom) or not self.check_collision():
            self.x -= 1

    def move_right(self):
        if (self.check_collision() and not self.reached_bottom) or not self.check_collision:
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
    
    
