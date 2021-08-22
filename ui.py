from abc import ABC, abstractmethod
from game_of_life import GameOfLife


class UI(ABC):
    def __init__(self, life: GameOfLife) -> None:
        self.life: GameOfLife = life

    @abstractmethod
    def run(self) -> None:
        ...
