import copy
from dataclasses import dataclass


@dataclass
class GameGridRepository:
    _game_grid: list[list]

    def __init__(self):
        self._game_grid = [[0]*10 for _ in range(10)]

    @property
    def game_grid(self):
        '''
        Gets the game grid
        :return:
        '''
        return self._game_grid

    def update(self, i, j, value):
        '''
        Update the game grid at position (i,j) with the given [value]
        :param i:
        :param j:
        :param value:
        :return:
        '''
        self._game_grid[i][j] = value

