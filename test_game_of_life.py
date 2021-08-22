from copy import deepcopy
from pathlib import Path
from unittest import TestCase

from game_of_life import GameOfLife, Grid, Cell


class TestGameOfLife(TestCase):
    def setUp(self) -> None:
        self.file_path: str = 'glider.txt'

    def test_create_grid(self):
        life: GameOfLife = GameOfLife((5, 5), randomize=False)
        grid: Grid = life.curr_generation

        expected_grid: Grid = Grid([[0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0]])

        self.assertEqual(grid, expected_grid)

    def test_count_neighbours(self):
        grid: Grid = Grid([[0, 1, 0, 0, 0],
                           [1, 1, 0, 0, 0],
                           [1, 1, 1, 0, 0],
                           [1, 0, 1, 0, 0],
                           [1, 1, 1, 0, 0]])

        life: GameOfLife = GameOfLife((5, 5), randomize=False)
        life.curr_generation = grid

        self.assertEqual(life.count_neighbours(Cell(0, 0)), 3)
        self.assertEqual(life.count_neighbours(Cell(3, 1)), 8)
        self.assertEqual(life.count_neighbours(Cell(0, 4)), 0)
        self.assertEqual(life.count_neighbours(Cell(1, 2)), 4)

    def test_get_next_generation(self):
        life: GameOfLife = GameOfLife.from_file(Path(self.file_path))
        grid: Grid = life.get_next_generation()

        expected_grid: Grid = Grid([[0, 0, 0, 0, 0],
                                    [1, 0, 1, 0, 0],
                                    [0, 1, 1, 0, 0],
                                    [0, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0]])

        self.assertEqual(grid, expected_grid)

    def test_step(self):
        life: GameOfLife = GameOfLife.from_file(Path(self.file_path))
        generations_counter: int = life.generations
        expected_prev_grid: Grid = deepcopy(life.curr_generation)

        life.step()

        prev_grid: Grid = life.prev_generation
        curr_grid: Grid = life.curr_generation
        expected_curr_grid: Grid = Grid([[0, 0, 0, 0, 0],
                                         [1, 0, 1, 0, 0],
                                         [0, 1, 1, 0, 0],
                                         [0, 1, 0, 0, 0],
                                         [0, 0, 0, 0, 0]])

        self.assertEqual(life.generations, generations_counter + 1)
        self.assertEqual(prev_grid, expected_prev_grid)
        self.assertEqual(curr_grid, expected_curr_grid)

    def test_is_max_generations_exceeded(self):
        life: GameOfLife = GameOfLife.from_file(Path(self.file_path))
        life.max_generations = 4

        for _ in range(10):
            if life.is_max_generations_exceeded:
                break
            life.step()

        expected_grid: Grid = Grid([[0, 0, 0, 0, 0],
                                    [0, 0, 1, 0, 0],
                                    [0, 0, 0, 1, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0]])

        self.assertTrue(life.is_max_generations_exceeded)
        self.assertEqual(life.curr_generation, expected_grid)

    def test_is_changing(self):
        life: GameOfLife = GameOfLife.from_file(Path(self.file_path))

        from_file_grid: Grid = deepcopy(life.curr_generation)
        life.step()

        self.assertNotEqual(from_file_grid, life.curr_generation)

    def test_from_file(self):
        life: GameOfLife = GameOfLife.from_file(Path(self.file_path))

        from_file_grid: Grid = life.curr_generation
        expected_grid: Grid = Grid([[0, 1, 0, 0, 0],
                                    [0, 0, 1, 0, 0],
                                    [1, 1, 1, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0]])

        self.assertEqual(from_file_grid, expected_grid)

    def test_save(self):
        save_path: str = 'saved.txt'

        life: GameOfLife = GameOfLife((5, 5))
        life.save(Path(save_path))
        self.assertEqual(Path(save_path).is_file(), True)

        expected_grid: Grid = deepcopy(life.curr_generation)
        self.assertEqual(life.from_file(Path(save_path)).curr_generation, expected_grid)

        Path(save_path).unlink()
