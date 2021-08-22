from __future__ import annotations

from copy import deepcopy
from itertools import product
from pathlib import Path
from random import choice
from typing import NamedTuple, Optional


class Grid:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid: list[list[int]] = grid
        self.rows: int = len(grid)
        self.columns: int = len(grid[0])

    def __getitem__(self, key: int):
        return self.grid[key]

    def __eq__(self, other: Grid) -> bool:
        return self.grid.__eq__(other.grid)

    def __repr__(self) -> str:
        return repr(self.grid)


class Cell(NamedTuple):
    row: int
    column: int


class GameOfLife:
    def __init__(self, size: tuple[int, int], randomize: bool = True, max_generations: Optional[int] = None) -> None:
        self.rows: int
        self.cols: int

        self.rows, self.cols = size

        # Previous generation of cells
        self.prev_generation: Grid = self.create_grid()
        # Current cell generation
        self.curr_generation: Grid = self.create_grid(randomize=randomize)

        # Maximum number of generations
        self.max_generations: Optional[int] = max_generations
        # Current number of generations
        self.generations: int = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid: list[list[int]] = [[choice([0, 1]) if randomize else 0 for _ in range(self.cols)]
                                 for _ in range(self.rows)]
        return Grid(grid)

    def count_neighbours(self, cell: Cell) -> int:
        neighbours: int = 0

        for r, c in product(range(-1, 2), range(-1, 2)):
            row_: int = r + cell.row
            column_: int = c + cell.column

            if 0 <= row_ < self.curr_generation.rows and 0 <= column_ < self.curr_generation.columns:
                neighbours += self.curr_generation[row_][column_]

        return neighbours - self.curr_generation[cell.row][cell.column]

    def get_next_generation(self) -> Grid:
        new_generation: Grid = deepcopy(self.curr_generation)

        for row, column in product(range(self.curr_generation.rows), range(self.curr_generation.columns)):
            neighbours: int = self.count_neighbours(Cell(row, column))

            if self.curr_generation[row][column] == 1 and (neighbours < 2 or neighbours > 3):
                new_generation[row][column] = 0
            elif self.curr_generation[row][column] == 0 and neighbours == 3:
                new_generation[row][column] = 1

        return new_generation

    def step(self) -> None:
        new_generation: Grid = self.get_next_generation()
        self.prev_generation, self.curr_generation = self.curr_generation, new_generation

        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.max_generations is not None and self.generations == self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: Path) -> GameOfLife:
        with filename.open() as file:
            new_grid: list[list[int]] = [list(map(int, filter(str.isdigit, line))) for line in file]

        new_grid: Grid = Grid(new_grid)
        game_of_life: GameOfLife = GameOfLife((new_grid.rows, new_grid.columns), randomize=False)
        game_of_life.curr_generation = new_grid

        return game_of_life

    def save(self, filename: Path) -> None:
        with filename.open(mode='w') as file:
            for row in self.curr_generation:
                data: str = ''.join(map(str, row)) + '\n'
                file.write(data)
