import pygame, time, random
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

    def handle_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.current_block.move_left()
        elif key[pygame.K_RIGHT]:
            self.current_block.move_right()
        elif key[pygame.K_UP]:
            self.current_block.rotate_cw()
        elif key[pygame.K_DOWN]:
            self.current_block.move_down()

    def run(self):
        running = True
    
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False 
            
            window.fill((0, 0, 0)) 
            self.draw_board()
            self.current_block.draw_shape(
            self.tetris_coords("x", self.current_block.x),  # 340
            self.tetris_coords("y", self.current_block.y),  # 30
            self.current_block.color, window
            )
            self.current_block.update()
            self.handle_input()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(60)

        pygame.quit()

tetrisBoard = Tetris()
tetrisBoard.run()
