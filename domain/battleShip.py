from dataclasses import dataclass

from exceptions.exceptions import WrongDataTypeError


@dataclass
class BattleShip:
    __id: int
    __length: int
    __nr_of_blocks_hit: int
    __start_position = None
    __end_position = None


    @property
    def id(self):
        return self.__id
    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        if type(value) == int:
            self.__length = value
        else:
            raise WrongDataTypeError("The value attributed to the battleship length is not integer!")

    @property
    def nr_of_blocks_hit(self):
        return self.__nr_of_blocks_hit

    @nr_of_blocks_hit.setter
    def nr_of_blocks_hit(self, value):
        if type(value) == int:
            self.__nr_of_blocks_hit = value
        else:
            raise WrongDataTypeError


    @property
    def start_position(self):
        return self.__start_position

    @start_position.setter
    def start_position(self, value):
        self.__start_position = value

    @property
    def end_position(self):
        return self.__end_position

    @end_position.setter
    def end_position(self, value):
        self.__end_position = value
