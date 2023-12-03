from dataclasses import dataclass
import random

from domain.battleShip import BattleShip
from exceptions.exceptions import *
from repository.GameGridRepository import *
from repository.battleShipRepository import *


@dataclass
class BattleShipService:
    '''
    There are ships with the following dimensions: [5,4,3,3,2]
    '''
    _battle_ship_repository: list[BattleShipRepository]
    _game_grid_repository: list[GameGridRepository]
    _target_grid_repository: list[GameGridRepository]
    __hit_positions_array = []

    def configure_game(self):
        # self._battle_ship_service.place_battle_ship(5, (0, 0), (4, 0), 0)
        # self._battle_ship_service.place_battle_ship(4, (2, 6), (5, 6), 0)
        # self._battle_ship_service.place_battle_ship(3, (4, 3), (4, 5), 0)
        # self._battle_ship_service.place_battle_ship(3, (6, 5), (6, 7), 0)
        # self._battle_ship_service.place_battle_ship(2, (0, 1), (0, 2), 0)

        ship_lengths = [5, 4, 3, 3, 2]
        index = 0
        while index < len(ship_lengths):
            position_x = random.randrange(0, 10)
            position_y = random.randrange(0, 10)
            vertical = random.randrange(0, 2)
            horizontal = (1 if vertical == 0 else 0)

            if position_x + ship_lengths[index] * vertical <= 9 and position_y + ship_lengths[index] * horizontal <= 9:
                try:
                    self.place_battle_ship(ship_lengths[index], (position_x, position_y), (
                        position_x + (ship_lengths[index] - 1) * vertical,
                        position_y + (ship_lengths[index] - 1) * horizontal), 1)
                    index += 1
                except:
                    pass

        # index = 0
        # while index < len(ship_lengths):
        #     position_x = random.randrange(0, 10)
        #     position_y = random.randrange(0, 10)
        #     vertical = random.randrange(0, 2)
        #     horizontal = (1 if vertical == 0 else 0)
        #     if position_x + ship_lengths[index] * vertical <= 9 and position_y + ship_lengths[index] * horizontal <= 9:
        #         try:
        #             self._battle_ship_service.place_battle_ship(ship_lengths[index], (position_x, position_y), (
        #                 position_x + (ship_lengths[index] - 1) * vertical,
        #                 position_y + (ship_lengths[index] - 1) * horizontal), 0)
        #             index += 1
        #         except:
        #             pass

    @property
    def player_battle_ship_repository(self):
        '''
        Returns the battleShipRepository of the first player
        :return:
        '''
        return self._battle_ship_repository[0].repository

    @property
    def ships_len_not_yet_placed_by_player(self):
        return [ship.length for ship in self._battle_ship_repository[0].ships_not_yet_placed]

    @property
    def ai_battle_ship_repository(self):
        '''
        Returns the battleShipRepository of the first player
        :return:
        '''
        return self._battle_ship_repository[1].repository

    def get_game_grid(self, player_index):
        '''
        Returns the game grid of the player with the index [player_index] - 0 is player human and 1 is player A.I.
        :param player_index:
        :return:
        '''
        return self._game_grid_repository[player_index].game_grid

    def get_target_grid(self, player_index):
        '''
        Returns the target grid of the player with the index [player_index] - 0 is player human, 1 player A.I.
        :param player_index:
        :return:
        '''
        return self._target_grid_repository[player_index].game_grid

    def remove_sunk_ship(self, battle_ship_id, player_index):
        self._battle_ship_repository[player_index].remove(battle_ship_id)
        # print("Repository:\n")
        # for el in self._battle_ship_repository[player_index].repository:
        #     print(el, end="\n")

    def check_position(self, ship_length, position_start, position_end, player_index):
        '''
        Checks if a player can put a ship of length [ship_length] in between positions [position_start, position_end], if that space is empty and doesn't overlap with other battleships and if the space reserved can fit a ship of given length
        :param ship_length:
        :param position_start:
        :param position_end:
        :param player_index:
        :return: True or False accordingly
        '''
        for i in range(position_start[0], position_end[0] + 1):
            for j in range(position_start[1], position_end[1] + 1):
                if self._game_grid_repository[player_index].game_grid[i][j] != 0:
                    return False

        if (position_start[0] - position_end[0]) * (position_start[1] - position_end[1]) == 0 and (
                abs(position_start[1] - position_end[1]) + 1 == ship_length or abs(
            position_start[0] - position_end[0]) + 1 == ship_length):
            return True

        return False

    def place_battle_ship(self, ship_length, position_start, position_end, player_index):
        '''
        Places the battleship on the grid by updating grid positions with the value of the battleship with the given length that hasn't been set yet. In this way we can navigate the game grid and get information about the battleship sitting on those positions in every one of the positions the ship occupies.
        :param ship_length:
        :param position_start:
        :param position_end:
        :param player_index:
        :return:
        '''

        battle_ship = \
            [ship for ship in self._battle_ship_repository[player_index].repository if
             ship.start_position is None and ship.length == ship_length]

        if len(battle_ship) == 0:
            raise InvalidShipProperty(
                'The length of the ship is invalid or the ship has already been placed on the board!')
        else:
            battle_ship = battle_ship[0]

        if not self.check_position(ship_length, position_start, position_end, player_index):
            raise InvalidPositionError

        battle_ship.start_position = position_start
        battle_ship.end_position = position_end

        for i in range(position_start[0], position_end[0] + 1):
            for j in range(position_start[1], position_end[1] + 1):
                self._game_grid_repository[player_index].update(i, j, battle_ship)

    def configuration_phase_finished(self, player_index):
        '''
        Checks if all the ships of player with index [player_index] have been placed on the game grid
        :param player_index:
        :return:
        '''
        for ship in self._battle_ship_repository[player_index].repository:
            if ship.start_position is None:
                return False

        return True

    def game_over(self, player_index):
        '''
        Checks if all the ships of a player are sunk, meaning that the length of the ships is equal to the nr of blocks hit from that ship.
        :param player_index:
        :return:
        '''
        # for ship in self._battle_ship_repository[player_index].repository:
        #     if ship.length != ship.nr_of_blocks_hit:
        #         return False
        # return True
        if len(self._battle_ship_repository[player_index].repository) == 0:
            return True

        return False

    @staticmethod
    def opposite_player_index(player_index):
        '''
        Returns the opposite player index, switching between human player and A.I. player
        :param player_index:
        :return:
        '''
        if player_index == 0:
            return 1

        return 0

    def place_hit(self, pos_x, pos_y, player_index):
        '''
        This function checks if on the positions [pos_x, pos_y] there is a battleship of the opposite player:
         if there is-- increments the battleship's hit counter
         regardless of the hit status -- updates the game grid of the plyer who launched the hit, either with 1 if hit, or -1 if missed

         The function returns the index of the player who does the next move and a message indicating the hit status
        :param pos_x:
        :param pos_y:
        :param player_index:
        :return:
        '''
        if pos_x < 0 or pos_x > 9 or pos_y < 0 or pos_y > 9:
            raise InvalidPositionError

        if self._target_grid_repository[player_index].game_grid[pos_x][pos_y] != 0:
            raise PositionAlreadyGuessedError
        if type(self._game_grid_repository[self.opposite_player_index(player_index)].game_grid[pos_x][
                    pos_y]) == BattleShip:
            battle_ship = self._game_grid_repository[self.opposite_player_index(player_index)].game_grid[pos_x][pos_y]
            battle_ship.nr_of_blocks_hit += 1
            self._target_grid_repository[player_index].update(pos_x, pos_y, 1)  # 1 = hit, -1 = not hit

            if battle_ship.length == battle_ship.nr_of_blocks_hit:
                return self.opposite_player_index(player_index), f'hit and sunk,{battle_ship.id}'
            elif battle_ship.length > battle_ship.nr_of_blocks_hit:
                return player_index, 'hit'
        else:
            self._target_grid_repository[player_index].update(pos_x, pos_y, -1)  # 1 = hit, -1 = not hit
            return self.opposite_player_index(player_index), 'miss'

    '''
    We will implement some statistics of where is the most likely position for a ship to be in.
    Let's take for example ship with length 5.
    Step 1 horizontal
       1 2 3 4 5 6 7 8 9 10 
     -----------------------
     1|1 2 3 4 5 5 4 3 2 1
     2|1 2 3 4 5 5 4 3 2 1
     3|1 2 3 4 5 5 4 3 2 1
     4|1 2 3 4 5 5 4 3 2 1
     5|1 2 3 4 5 5 4 3 2 1
     6|1 2 3 4 5 5 4 3 2 1
     7|1 2 3 4 5 5 4 3 2 1
     8|1 2 3 4 5 5 4 3 2 1
     9|1 2 3 4 5 5 4 3 2 1
    10|1 2 3 4 5 5 4 3 2 1
    
       1 2 3 4 5 6 7 8 9 10
     -----------------------
     1|1 2 3 4 5 5 4 3 2 1   for 5: y if y<=5, 11-y if 11-y<=5, else: 5
     2|1 2 3 4 4 4 3 3 2 1   for n length of ship: y if y<=n, 11-y if 11-y<=n, else n for both vertical and horisontal 
     3|1 2 3 3 3 3 3 3 2 1
     4|1 2 2 2 2 2 2 2 2 1
     5|1 2 3 4 5 5 4 3 2 1
     6|1 2 3 4 5 5 4 3 2 1
     7|1 2 3 4 5 5 4 3 2 1
     8|1 2 3 4 5 5 4 3 2 1
     9|1 2 3 4 5 5 4 3 2 1
    10|1 2 3 4 5 5 4 3 2 1
    
    Step 2 vertical
       1 2 3 4 5 6 7 8 9 10
     -----------------------
     1|2 3 3 4 5 5 4 3 2 1
     2|3 2 3 4 5 5 4 3 2 1
     3|4 2 3 4 5 5 4 3 2 1
     4|5 2 3 4 5 5 4 3 2 1
     5|6 2 3 4 5 5 4 3 2 1
     6|6 2 3 4 5 5 4 3 2 1
     7|5 2 3 4 5 5 4 3 2 1
     8|4 2 3 4 5 5 4 3 2 1
     9|3 2 3 4 5 5 4 3 2 1
    10|2 2 3 4 5 5 4 3 2 1
    
    Step 1 horizontal with obstacles => if he finds obstacle on the next 5, don't add anything, go from the position of the obtsacle until there are no more obstacles in front and then search again for 5 free positions. The same horisontally
       1 2 3 4 5 6 7 8 9 10
     -----------------------
     1|0 0 0 0 0 0 0 0 0 0
     2|0 0 0 0 0 0 0 0 0 0
     3|0 0 0 0 0 0 0 0 0 0
     4|0 0 0 0 0 0 0 0 0 0
     5|0 0 0 0 0 0 0 0 0 0
     6|1 1 1 1 1 - 4 3 2 1
     7|1 2 3 4 5 5 4 3 2 1
     8|0 0 0 0 0 0 0 0 0 0
     9|0 0 0 0 0 0 0 0 0 0
    10|0 0 0 0 0 0 0 0 0 0
    
    1 2 3 4 5 6 7 8 9 10
     -----------------------
     1|0 0 0 0 0 0 0 0 0 0   ### if we encounter a hit, we just substract, else we set value to 0
     2|0 0 0 0 1 0 0 0 0 0   ### after we hit and sunk a ship, clean up the road and column and the remaining should 
     3|0 0 0 0 2 0 0 0 0 0   ### be the other ship if two are placed next to one another
     4|0 0 0 0 0 0 0 0 0 0
     5|0 0 0 0 0 # 0 0 0 0
     6|0 0 0 # - - # 0 0 0
     7|0 0 0 0 - 1 0 0 0 0
     8|0 0 0 0 - 1 0 0 0 0
     9|0 0 0 0 - 1 0 0 0 0
    10|0 0 0 0 1 1 0 0 0 0
    
       1 2 3 4 5 6 7 8 9 10
     -----------------------
     1|0 0 0 0 0 0 0 0 0 0   
     2|0 0 0 0 0 0 0 0 0 0    
     3|0 0 0 0 0 0 0 0 0 0   
     4|0 0 0 0 0 0 0 0 0 0   
     5|0 0 0 0 0 0 0 0 0 0
     6|0 0 0 0 0 - - 0 0 0
     7|0 0 0 0 0 - - - 0 0
     8|0 0 0 0 0 0 0 0 0 0
     9|0 0 0 0 0 0 0 0 0 0
    10|0 0 0 0 0 0 0 0 0 0
    
    #strategy: build this secondary hunting mode heatmap,
    calculate the new statistics maximum and shoot at that point. If hit, add to the positions around the point on line and column, if missed put 0 everywhere where you don't meet a hit point, else just substract the values that were otherwise added
    We have to check if nr_of_hits>length, means we continue with this heatmap
    '''

    @staticmethod
    def create_heatmap_matrix():
        '''
        Create an initial heatmap matrix where every position contains the probability of it being the position of a battleship from a classic game with 5 ships of lengths:5, 4, 3, 2, 1

        It puts every ship in all possible positions adding to the probability of a ship being in that position.
        :return: the matrix with the given values, a heatmap of where the ships could be
        '''
        heatmap = [[0 for _ in range(10)] for _ in range(10)]
        ship_lengths = [5, 4, 3, 3, 2]
        for x in range(10):
            for y in range(10):
                for ship_len in ship_lengths:
                    if y + 1 <= ship_len:
                        heatmap[x][y] += y + 1
                    elif 10 - y <= ship_len:
                        heatmap[x][y] += 10 - y
                    else:
                        heatmap[x][y] += ship_len

                    if x + 1 <= ship_len:
                        heatmap[x][y] += x + 1
                    elif 10 - x <= ship_len:
                        heatmap[x][y] += 10 - x
                    else:
                        heatmap[x][y] += ship_len

        return heatmap

    @staticmethod
    def check_free_space_of_n(target_grid, i, j, n, horizontal, vertical):
        '''
        Checks if from the positions [i,j] n positions in the horizontal or vertical direction are free to place a ship or not
        :param target_grid:list[list],  grid where the player marks its choices
        :param i:int, starting x position
        :param j:int, starting y positon
        :param n:int, length of the ship
        :param horizontal: boolean
        :param vertical: boolean
        :return:boolean value, True/ False
        '''
        for index in range(n):
            if i + index * vertical > 9 or j + index * horizontal > 9:
                return False
            elif target_grid[i + index * vertical][j + index * horizontal] != 0:
                return False

        return True

    def reconfigure_heatmap_matrix(self):
        target_grid = self._target_grid_repository[1].game_grid
        ship_lengths = [
            ship.length for ship in self._battle_ship_repository[1].repository if (
                    ship.length > ship.nr_of_blocks_hit
            )
        ]
        heatmap = [[0 for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                for ship_length in ship_lengths:
                    if self.check_free_space_of_n(target_grid, i, j, ship_length, 1, 0):
                        for index in range(ship_length):
                            heatmap[i][j + index] += 1
        for j in range(10):
            for i in range(10):
                for ship_length in ship_lengths:
                    if self.check_free_space_of_n(target_grid, i, j, ship_length, 0, 1):
                        for index in range(ship_length):
                            heatmap[i + index][j] += 1
        return heatmap

    # region AI version 1

    # @staticmethod
    # def clean_up_row_column(row, column, heatmap):
    #
    #     for index in range(10):
    #         heatmap[row][index] = 0
    #         heatmap[index][column] = 0

    # def update_heatmap_matrix(self, heatmap, position_x, position_y):
    #     target_grid = self._target_grid_repository[1].game_grid
    #     ship_lengths = [5, 4, 3, 3, 2]
    #     self.clean_up_row_column(position_x, position_y, heatmap)
    #
    #     for y in range(0, 10):
    #         for ship_length in ship_lengths:
    #             if self.check_free_space_of_n(target_grid, position_x, y, ship_length, 1, 0):
    #                 for index in range(ship_length):
    #                     heatmap[position_x][y + index] += 1
    #     for x in range(0, 10):
    #         for ship_length in ship_lengths:
    #             if self.check_free_space_of_n(target_grid, x, position_y, ship_length, 0, 1):
    #                 for index in range(ship_length):
    #                     heatmap[x + index][position_y] += 1
    # endregion
    @staticmethod
    def make_ai_choice(heatmap):
        '''
        Gets the position with the highest statistic probability of a ship being placed on that position
        :param heatmap:
        :return: the positions x and y cordinates, touple
        '''
        max_heatmap_value = 0
        max_position_x = -1
        max_position_y = -1

        for i in range(10):
            for j in range(10):
                if heatmap[i][j] > max_heatmap_value:
                    max_heatmap_value = heatmap[i][j]
                    max_position_x = i
                    max_position_y = j
        return max_position_x, max_position_y

    @staticmethod
    def make_ai_choice_inverse(heatmap):
        '''
        Gets the position with the highest statistic probability of a ship being placed on that position
        :param heatmap:
        :return: the positions x and y cordinates, touple
        '''
        min_heatmap_value = 10000
        min_position_x = -1
        min_position_y = -1

        for i in range(10):
            for j in range(10):
                if heatmap[i][j] < min_heatmap_value and heatmap[i][j] > 0:
                    min_heatmap_value = heatmap[i][j]
                    min_position_x = i
                    min_position_y = j
        return min_position_x, min_position_y

    def in_bounds(self, pos_x, pos_y):
        '''
        Checks if the positions given are in the bounds of the board
        :param pos_x:
        :param pos_y:
        :return:
        '''
        if pos_x < 0 or pos_x > 9 or pos_y < 0 or pos_y > 9:
            return False

        return True

    def check_if_not_guessed(self, x, y):
        '''
        Checks if a position composed by (x,y) has not yet been guessed by the AI
        :param x:
        :param y:
        :return:
        '''
        if self._target_grid_repository[1].game_grid[x][y] == 0:
            return True

        return False

    def add_hit_position(self, pos_x, pos_y):
        '''
        Adds to the positions hit by the AI in one continuous strike the position pair given and the direction given by the first hit element, in order to keep trying to hit more ship parts in that direction
        :param pos_x:
        :param pos_y:
        :return:
        '''
        if len(self.__hit_positions_array) == 0:
            self.__hit_positions_array.append((pos_x, pos_y, 0))
        else:
            self.__hit_positions_array.append((pos_x, pos_y, self.__hit_positions_array[0][2]))

    def check_if_all_hits_from_the_same_battleship(self):
        '''
        Check if all the hits from one continuous strike were to just one ship or if any other ships were shot when trying to sunk the original ship
        :return:
        '''
        if len(self.__hit_positions_array) == 0:
            return True

        return False

    def remove_ship_from_hits(self, ship):
        '''
        Removes all positions of the ship from the hits position in order to find the whole ship that was accidentally hit when trying to sink another ship
        :param ship:
        :return:
        '''
        ship_positions = []
        for x in range(ship.start_position[0], ship.end_position[0] + 1):
            for y in range(ship.start_position[1], ship.end_position[1] + 1):
                ship_positions.append((x, y))

        # print(ship_positions)

        self.__hit_positions_array = [(x, y, direction) for (x, y, direction) in self.__hit_positions_array if
                                      (x, y) not in ship_positions]
        # print(self.__hit_positions_array)

    def update_direction_of_hits(self, pos_x, pos_y, new_direction):
        '''
        Updates the directions in which we should continue the search from each position in order to find new possible ship positions
        :param pos_x:
        :param pos_y:
        :param new_direction:
        :return:
        '''
        for index, (x, y, direction) in enumerate(self.__hit_positions_array):
            if pos_x == x and pos_y == y:
                self.__hit_positions_array[index] = (pos_x, pos_y, new_direction)

    def find_ship_positions(self):
        '''
        Gives the A.I.'s guess of where the ship could be placed
        :return:the predicted coordinates (x,y)
        '''
        direction_x = [0, 0, -1, 1]
        direction_y = [1, -1, 0, 0]

        (x, y, direction) = self.__hit_positions_array[-1]

        index_d = 0
        new_x = x + direction_x[direction + index_d]
        new_y = y + direction_y[direction + index_d]
        while (not self.in_bounds(new_x, new_y) or not self.check_if_not_guessed(new_x, new_y)) and len(
                self.__hit_positions_array) == 1:
            index_d += 1
            direction = (direction + index_d) % 4
            new_x = x + direction_x[direction]
            new_y = y + direction_y[direction]
            self.update_direction_of_hits(x, y, direction)

        if len(self.__hit_positions_array) > 1:
            if (not self.in_bounds(new_x, new_y) or not self.check_if_not_guessed(new_x, new_y)):
                (x, y, direction) = self.__hit_positions_array[0]
                direction = (direction + 1) % 4
                new_x = x + direction_x[direction]
                new_y = y + direction_y[direction]
                while (not self.in_bounds(new_x, new_y) or not self.check_if_not_guessed(new_x, new_y)):
                    direction = (direction + 1) % 4
                    new_x = x + direction_x[direction]
                    new_y = y + direction_y[direction]

                self.update_direction_of_hits(x, y, direction)
        return new_x, new_y
