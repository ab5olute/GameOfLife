## GameOfLife

A Python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life) with PyGame module.

### Rules

1. Any live cell with two or three live neighbours survives.
2. Any dead cell with three live neighbours becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

### Example of GameOfLife usage

```
>>> life = GameOfLife.from_file(pathlib.Path('glider.txt'))
```
```
>>> life.curr_generation
[[0, 1, 0, 0, 0],
 [0, 0, 1, 0, 0],
 [1, 1, 1, 0, 0],
 [0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0]]
```
```
>>> for _ in range(4):
...    life.step()
```
```
>>> life.curr_generation
[[0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0],
 [0, 0, 0, 1, 0],
 [0, 1, 1, 1, 0],
 [0, 0, 0, 0, 0]]
```
```
>>> life.save(pathlib.Path('glider-4-steps.txt'))
```

### Pygame Controle Settings

* To pause the game: press SPACE key.
* To draw or remove cell click: LEFT MOUSE button.

