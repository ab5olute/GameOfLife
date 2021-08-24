## GameOfLife

A Python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life) with PyGame module.

### Rules

1. Any live cell with two or three live neighbours survives.
2. Any dead cell with three live neighbours becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

### Example of GameOfLife usage

```python
>>> life = GameOfLife.from_file(pathlib.Path('figures/glider.txt'))
```
```python
>>> life.curr_generation
[[0, 1, 0, 0, 0],
 [0, 0, 1, 0, 0],
 [1, 1, 1, 0, 0],
 [0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0]]
```
```python
>>> for _ in range(4):
...    life.step()
```
```python
>>> life.curr_generation
[[0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0],
 [0, 0, 0, 1, 0],
 [0, 1, 1, 1, 0],
 [0, 0, 0, 0, 0]]
```
```python
>>> life.save(pathlib.Path('glider-4-steps.txt'))
```

### Pygame Controle Settings

* To pause the game: press SPACE key.
* To draw or remove cell click: LEFT MOUSE button.

### Run tests

```python
python -m unittest discover
```

### Demo
![Demo](https://github.com/ab5olute/GameOfLife/blob/master/images/demo.gif?raw=true)

