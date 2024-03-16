import pygame
import math
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
        self.game_over = False
        self.held_block = False

    
    def create_available(self):
        available_spaces = [(x, 0) for x in range(10)]

        for row in range(len(tetris_matrix)):
            for col in range(len(tetris_matrix[row])):
                if tetris_matrix[row][col] == 0:
                    available_spaces.append((col+1, row+1))
        return available_spaces

    def check_rotate(self):
        spaces = self.create_available()   
        rotated_coords = []  
        test_rotation = self.rotation + 1
        if test_rotation > 3:
            test_rotation = 0  

        for row in range(len(tetris_grid)):
            for e in range(len(tetris_grid[row])):
                if tetris_grid[row][e] in shapes[self.shape][test_rotation]:
                    coord = ((self.x+e-1),
                                 (self.y+row-1))
                    rotated_coords.append(coord)

        for a in rotated_coords:
            if not a in spaces:
                return False
        return True

    def rotate_cw(self):
        if self.check_rotate():
            self.rotation += 1
            if self.rotation > 3:
                self.rotation = 0
            self.code = shapes[self.shape][self.rotation]

    def rotate_ccw(self):
        if self.check_rotate():
            self.rotation -= 1
            if self.rotation < 0:
                self.rotation = 3
            self.code = shapes[self.shape][self.rotation]

    def check_collision(self, direction):
        check_left = dimensions[self.shape][0][self.rotation]+2
        check_right = 10 - dimensions[self.shape][1][self.rotation]
        if direction == "v":
            if self.y >= 19:
                if self.shape != "I":
                    self.y = 19
                    self.reached_bottom = True
                else:
                    self.y = 20
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
        spaces = self.create_available()

        for coords in self.block_coords:
            future_coords = (coords[0], coords[1])
            if not future_coords in spaces:
                if self.y <= 20:
                    return True
        return False

    def hard_drop(self):
        while not self.check_collision("v") and not self.block_collision():
            self.move_down()

        self.write_block()
        self.reached_bottom = True
        self.new_block = True

    def write_block(self):
        for coords in self.block_coords:
            tetris_matrix[coords[1]-2][coords[0] - 1] = list(shapes.keys()).index(self.shape)+1

    def move_down(self):
        if not self.check_collision("v") or not self.reached_bottom:
            if self.block_collision():
                self.write_block()
                self.new_block = True
            else:
                for a in range(len(self.block_coords)):
                    self.block_coords[a] = (
                        self.block_coords[a][0], self.block_coords[a][1]+1)

                self.y += 1
        elif self.reached_bottom:
            self.write_block()
            self.new_block = True

    def move_left(self):
        if not self.check_collision("l"):
            if self.block_collision():
                self.write_block()
                self.new_block = True
            else:
                for a in range(len(self.block_coords)):
                    self.block_coords[a] = (
                        self.block_coords[a][0]-1, self.block_coords[a][1])

                self.x -= 1

    def move_right(self):
        if not self.check_collision("r"):
            if self.block_collision():
                self.write_block()
                self.new_block = True
            else:
                for a in range(len(self.block_coords)):
                    self.block_coords[a] = (
                        self.block_coords[a][0]+1, self.block_coords[a][1])

                self.x += 1

    def draw_block(self, x, y, color, window):
        return pygame.draw.rect(window, color, tetris_piece(x, y))

    def spawn_shape(self, x, y):
        change = 1
        if self.shape == "L" or self.shape == "J":
            change = 2
        if self.shape == "I":
            change = 0
        self.draw_shape(
            x, 0+(-change-shape_dimensions[self.shape][1])*block_size)

    def draw_shape(self, x, y, color, window, code = False):
        code = code or self.code
        self.block_coords = []
        if not self.game_over:
            for row in range(len(tetris_grid)):
                for e in range(len(tetris_grid[row])):
                    if tetris_grid[row][e] in code:
                        coord = (math.floor((x+(e)*block_size)/block_size)-7,
                                 math.floor((y+(row-1)*block_size)/block_size)+2)
                        self.draw_block(x+(e)*block_size, y+(row-1)
                                        * block_size, color, window)
                        if coord not in self.block_coords:
                            self.block_coords.append(coord)

    def update(self, time, direction="d"):
        if pygame.time.get_ticks() - self.start_time > time and not self.game_over:
            if direction == "d":
                self.move_down()
            elif direction == "r":
                self.move_right()
            elif direction == "l":
                self.move_left()
            self.start_time = pygame.time.get_ticks()
