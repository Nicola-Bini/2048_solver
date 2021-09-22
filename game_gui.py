import numpy as np
import pygame
from pygame.locals import *

class Game2048Gui():


    # Blocks colors
    grid_colors =  {0       : [230, 230, 230],
                    2       : [179, 255, 153],
                    4       : [120, 255, 153],
                    8       : [70, 255, 179],
                    16	    : [40, 255, 204],
                    32	    : [25, 255, 230],
                    64	    : [10, 255, 255],
                    128	    : [153, 230, 255],
                    256	    : [153, 204, 255],
                    512	    : [153, 179, 255],
                    1024	: [153, 153, 255],
                    2048    : [179, 153, 255],
                    4096    : [204, 153, 255],
                    8192    : [230, 153, 255],
                    16384   : [255, 153, 255],
                    32768   : [255, 153, 230],
                    65536	: [255, 153, 204],
                    131072  : [255, 153, 179],
                    262144	: [255, 153, 153]}


    # Wait for key (Human input)
    def wait_for_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 4
                    elif event.key == K_RIGHT:
                        return 3
                    elif event.key == K_LEFT:
                        return 1
                    elif event.key == K_DOWN:
                        return 2
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'
                    else:
                        return "nothing"

    def __init__(self, window_size):
        '''
                Initialize GUI

                :param window_size:
                :return:
        '''

        pygame.init()

        self.SPACING = int(10 / window_size)
        self.RECT_W = int(200 / window_size)
        self.RECT_H = int(200 / window_size)

        self.W = int(self.SPACING * 3 + self.RECT_W * 4)
        self.H = int(self.SPACING * 3 + self.RECT_H * 4)

        # Display game
        self._display_surf = pygame.display.set_mode((self.W, self.H))


    # Update game GUI
    def draw_game(self,game, game_over=False):
        sans25 = pygame.font.SysFont('Arial', 52)
        sans15 = pygame.font.SysFont('Arial', 35)

        self._display_surf.fill([0, 0, 0])
        for i in range(4):
            for j in range(4):

                if i == 0:
                    x = i * self.RECT_W
                else:
                    x = i * self.RECT_W + i * self.SPACING

                if j == 0:
                    y = j * self.RECT_H
                else:
                    y = j * self.RECT_H + j * self.SPACING

                rect = pygame.Rect(x, y, self.RECT_W, self.RECT_H)
                pygame.draw.rect(self._display_surf, self.grid_colors[game.game_grid[i, j]], rect)

                text_render = sans25.render(str(game.game_grid[i, j]), True, [0, 0, 0])
                text_rect = text_render.get_rect(center=(x + self.RECT_W / 2, y + self.RECT_H / 2))

                self._display_surf.blit(text_render, text_rect)

        if game_over:
            rect_game_over_W = 200
            rect_game_over_H = 50
            x = ((self.RECT_W * 4 + self.SPACING * 3) - rect_game_over_W) / 2
            y = ((self.RECT_H * 4 + self.SPACING * 3) - rect_game_over_H) / 2
            rect = pygame.Rect(x, y, rect_game_over_W, rect_game_over_H)

            pygame.draw.rect(self._display_surf, [45,45,45], rect)

            text_render = sans15.render("Game Over", True, [255, 255, 255])
            text_rect = text_render.get_rect(center=(x + rect_game_over_W / 2, y + rect_game_over_H / 2))
            self._display_surf.blit(text_render, text_rect)


        pygame.display.flip()





        return "Game updated"
