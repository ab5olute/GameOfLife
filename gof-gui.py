import argparse
import textwrap
from itertools import product
from math import floor

import pygame
from pygame.locals import *
from pygame.surface import Surface
from pygame.time import Clock

from game_of_life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.life: GameOfLife = life
        self.cell_size: int = cell_size
        self.speed: int = speed

        super().__init__(life)

        self.width: int = self.cell_size * life.cols
        self.height: int = self.cell_size * life.rows

        # Setting the window size
        self.screen_size: tuple[int, int] = self.width, self.height
        # Creating a new window
        self.screen: Surface = pygame.display.set_mode(self.screen_size)

        # Game states
        self.running: bool = True
        self.pause: bool = False

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, Color('black'), start_pos=(x, 0), end_pos=(x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, Color('black'), start_pos=(0, y), end_pos=(self.width, y))

    def draw_grid(self) -> None:
        for c, r in product(range(self.life.curr_generation.columns), range(self.life.curr_generation.rows)):
            color: Color = pygame.Color('green') if self.life.curr_generation[r][c] == 1 else pygame.Color('white')
            rect: Rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color, rect)

    def draw_elements(self) -> None:
        self.draw_grid()
        self.draw_lines()

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.pause = True

                    x: int
                    y: int
                    x, y = pygame.mouse.get_pos()

                    x = floor(x / self.cell_size)
                    y = floor(y / self.cell_size)

                    self.life.curr_generation[y][x] = 1 if self.life.curr_generation[y][x] == 0 else 0
                    self.draw_elements()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause = not self.pause

    def run(self) -> None:
        pygame.init()

        clock: Clock = Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        while self.running:
            self.check_events()

            if not self.pause:
                if self.life.is_changing and not self.life.is_max_generations_exceeded:
                    self.life.step()
                else:
                    self.running = False

                self.draw_elements()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Game of Life',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
             To pause the game: press SPACE key.
             To draw or remove cell: click LEFT MOUSE button.
             '''))

    parser.add_argument('--height', required=False, type=int, default=300)
    parser.add_argument('--width', required=False, type=int, default=500)
    parser.add_argument('--cell-size', required=False, type=int, default=20)

    args = parser.parse_args()

    height_: int = args.height
    width_: int = args.width
    cell_size_: int = args.cell_size

    game: GameOfLife = GameOfLife((height_ // cell_size_, width_ // cell_size_))
    gui: GUI = GUI(game, cell_size_)

    gui.run()
