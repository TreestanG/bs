import pygame, math
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
        self.block_coords = []

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

    def check_collision(self, direction):
        check_left = dimensions[self.shape][0][self.rotation]+2
        check_right = 10 - dimensions[self.shape][1][self.rotation]
        print(self.x, self.y)
        if direction == "v":
            if self.y >= 19:
                self.y = 19
                self.reached_bottom = True

                return True
        elif direction == "r":
            if self.x >= check_right:
                return True
        elif direction == "l":
            if self.x <= check_left:
                return True
        return False
    
    def block_collision(self):
        blk_dimensions = shape_dimensions[self.shape]
        if self.rotation == 1 or self.rotation == 3:
            blk_dimensions = blk_dimensions.reverse()

        available_spaces = []
        
        for row in range(len(tetris_matrix)):
            for col in range(len(tetris_matrix[row])):
                if tetris_matrix[row][col] == 0:
                    available_spaces.append((row, col))
        for coords in self.block_coords:
            if coords not in available_spaces:
                if self.y <= 0:
                    return True   
        return False
    
    def move_down(self):
        if not self.check_collision("v") or not self.reached_bottom:
            if self.block_collision():
                self.reached_bottom = True
            self.y += 1
        elif self.reached_bottom: 
            self.new_block = True

    def move_left(self):
        if not self.check_collision("l"):
            self.x -= 1

    def move_right(self):
        if not self.check_collision("r"):
            self.x += 1

    def draw_block(self, x, y, color, window):
        return pygame.draw.rect(window, color, tetris_piece(x,y))

    def draw_shape(self, x, y, color, window):
        self.block_coords = []
        for row in range(len(tetris_grid)):
            for e in range(len(tetris_grid[row])):
                if tetris_grid[row][e] in self.code:
                    coord = (math.floor((x+(e)*block_size)/block_size)-6, math.floor((y+(row-1)*block_size)/block_size)+1)
                    if coord not in self.block_coords:
                        self.block_coords.append(coord)
                    (self.draw_block(x+(e)*block_size, y+(row-1)*block_size, color, window))
    
    def update(self):
        if pygame.time.get_ticks() - self.start_time > 1250:
            self.move_down()
            self.start_time = pygame.time.get_ticks()
    
    
