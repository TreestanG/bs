import pygame, time, random
from pygame.locals import *

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

tetris_grid = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,16],
]

shapes = {
    "I":[[5,6,7,8], [3,7,11,15], [9,10,11,12], [2,6,10,14]],
    "O":[[2,3,6,7], [2,3,6,7], [2,3,6,7], [2,3,6,7]],
    "T":[[2,5,6,7], [2,6,7,10], [5,6,7,10], [2,5,6,10]],
    "L":[[2,6,10,11], [5,6,7,11], [1,2,6,10], [2,6,7,8]],
    "J":[[2,6,9,10], [1,5,6,7], [2,3,6,10], [5,6,7,11]],
    "S":[[2,3,5,6], [2,6,7,11], [2,3,5,6], [2,6,7,11]],
    "Z":[[1,2,6,7], [3,6,7,10], [1,2,6,7], [3,6,7,10]]
}



class TetrisBlock:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shape]
        self.rotation = 0
        self.code = shapes[shape][self.rotation]

    def rotate_cw(self):
        rotation += 1
        if rotation > 3:
            rotation = 0

    def rotate_ccw(self):
        rotation -= 1
        if rotation < 0:
            rotation = 3

    def move_down(self):
        #if self.check_collision():
            self.y += 1

    def check_collision(self):
        if self.y >= 20:
            return True
        elif self.x < 0 or self.x > 9:
            return True
        return False

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1
    
    def update(self, game_running):
        print(game_running)
        while game_running == True:
            time.sleep(1.25)
            self.move_down()



pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris - lol")


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
        pygame.draw.rect(window, (41, 44, 53), (x, y, block_size, block_size), 1)

    def draw_shape(self, x, y, shape, color):
        for row in range(len(tetris_grid)):
            for e in range(len(tetris_grid[row])):
                if tetris_grid[row][e] in self.current_block.code:
                    self.draw_block(x+(e)*block_size, y+(row-1)*block_size, color)                    

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

        tetris_block = TetrisBlock(x, y, shape)
        self.current_block = tetris_block

        return tetris_block

    def handle_input(self, event):
        if event.type == QUIT:
            return True
        elif event.type == KEYDOWN:
            print("key down")
            if event.key == K_LEFT:
                self.current_block.move_left()
            elif event.key == K_RIGHT:
                self.current_block.move_right()
            elif event.key == K_UP:
                self.current_block.rotate_cw()
            elif event.key == K_DOWN:
                print("down key pressed")
                self.current_block.rotate_ccw()

    def run(self):
        running = True
        self.draw_board()

        self.current_block.block = self.draw_shape(
            self.tetris_coords("x", self.current_block.x),  # 340
            self.tetris_coords("y", self.current_block.y),  # 30
            self.current_block.shape,
            self.current_block.color
        )

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                self.handle_input(event)

            pygame.display.update()

        pygame.quit()


tetrisBoard = Tetris()
tetrisBoard.run()
