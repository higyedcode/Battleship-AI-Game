import copy
from dataclasses import dataclass

from domain.battleShip import BattleShip
from exceptions.exceptions import *


@dataclass
class BattleShipRepository:
    __repo = list

    def __init__(self):
        self.__repo = [BattleShip(1, 5, 0), BattleShip(2, 4, 0), BattleShip(3, 3, 0), BattleShip(4, 3, 0),
                       BattleShip(5, 2, 0)]

    @property
    def repository(self):
        '''
        Returns the list of battleShips
        :return:
        '''
        return self.__repo

    @property
    def ships_not_yet_placed(self):
        return [ship for ship in self.__repo if ship.start_position is None]

    def _find_by_id(self, id):
        '''
        Finds the battleship with the given id, if id is not found returns None
        :param id:
        :return:
        '''
        for battle_ship in self.__repo:
            if battle_ship.id == id:
                return battle_ship

    def find_by_length(self, length):
        '''
        Finds the battleship with the given length, else returns None
        :param length:
        :return:
        '''
        for battle_ship in self.__repo:
            if battle_ship.length == length:
                return battle_ship

    def save_position(self, battleShip, pos_x, pos_y):
        '''
        Saves the position of the battleShip in the game board as a property of the battleship
        :param battleShip:
        :param pos_x:
        :param pos_y:
        :return:
        '''
        battleShip.start_position = pos_x
        battleShip.end_position = pos_y

    def remove(self, battle_ship_id):
        '''
        Removes the battleship with the given id from the battleShipRepository
        :param battle_ship_id:
        :return:
        '''
        battle_ship = self._find_by_id(battle_ship_id)
        if battle_ship is None:
            raise IdNotFoundError

        self.__repo.remove(battle_ship)
