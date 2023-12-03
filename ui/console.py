import random
import time

from texttable import Texttable

from service.battleShipService import *
from colorama import *


@dataclass
class Console:
    _battle_ship_service: BattleShipService
    __hunt_mode = False
    __heatmap = None
    __number_of_misses = 0

    @staticmethod
    def parse_position_data_from_console(position_string):
        if position_string[1] == '0':
            return 9, ord(position_string[2]) - ord('A')

        return int(position_string[0]) - 1, ord(position_string[1]) - ord('A')

    def place_ship_from_console(self, player_index):
        if player_index == 0:
            print(Fore.GREEN + f"Player {player_index}, place a ship:" + Style.RESET_ALL)
        else:
            print(Fore.BLUE + f"Player {player_index}, place a ship:" + Style.RESET_ALL)

        ship_length = int(input(
            f"Length of ship(available ships lengths: {self._battle_ship_service.ships_len_not_yet_placed_by_player}): "))

        position_data = input("Start position(ex: 8C): ")
        start_position = self.parse_position_data_from_console(position_data)

        position_data = input("End position(ex: 10D): ")
        end_position = self.parse_position_data_from_console(position_data)

        if start_position[0] >= end_position[0] and start_position[1] >= end_position[1]:
            start_position, end_position = end_position, start_position

        self._battle_ship_service.place_battle_ship(ship_length, start_position, end_position, player_index)

    def place_hit_from_console(self, player_index):
        position_data = input(Fore.GREEN + f'Player 0, choose target(ex: 6A) : ' + Style.RESET_ALL)

        (pos_x, pos_y) = self.parse_position_data_from_console(position_data)

        player_index, message = self._battle_ship_service.place_hit(pos_x, pos_y, player_index)
        if 'sunk' in message:
            ship_id = int(message.split(',')[1])
            sunk_battle_ship = [ship for ship in self._battle_ship_service.ai_battle_ship_repository if
                                ship.id == ship_id]
            # for el in self._battle_ship_service.ai_battle_ship_repository:
            #     print(el, end="\n")
            # print("id = ", sunk_battle_ship[0].id)
            print(Fore.RED + 'Target status: ', 'hit and sunk ship of length: ', sunk_battle_ship[0].length,
                  Style.RESET_ALL)
            self._battle_ship_service.remove_sunk_ship(ship_id, 1)
        elif 'hit' in message:
            print(Fore.RED + 'Target status: ', message, Style.RESET_ALL)
        else:
            print(Fore.LIGHTCYAN_EX + 'Target status: ', message, Style.RESET_ALL)
        return player_index

    def place_ai_hit(self):
        time.sleep(2)
        # if self.__number_of_misses > 5:
        #     pos_x, pos_y = self._battle_ship_service.make_ai_choice_inverse(self.__heatmap)
        #     print(Fore.LIGHTMAGENTA_EX + "AI INVERSE STRATEGY" + Style.RESET_ALL)
        # else:
        pos_x, pos_y = self._battle_ship_service.make_ai_choice(self.__heatmap)
        # self.print_game_boards(1)

        player_index, message = self._battle_ship_service.place_hit(pos_x, pos_y, 1)
        # version 1 of the AI
        # self._battle_ship_service.update_heatmap_matrix(heatmap, pos_x, pos_y)
        # version 2 of the AI
        self.__heatmap = self._battle_ship_service.reconfigure_heatmap_matrix()
        print(Fore.BLUE + 'AI chose positions ', pos_x + 1, chr(ord('A') + pos_y), Style.RESET_ALL)
        # self.print_heatmap()

        if 'hit' in message:
            self.__number_of_misses = 0
            print(Fore.RED + 'Target status: ', message, Style.RESET_ALL)
            # self._nr_of_hits += 1
            if message == 'hit':
                self.__hunt_mode = True
                self._battle_ship_service.add_hit_position(pos_x, pos_y)
                # self._hunt_x = pos_x
                # self._hunt_y = pos_y




        else:
            print(Fore.LIGHTCYAN_EX + 'Target status: ', message, Style.RESET_ALL)
            self.__number_of_misses += 1
        return player_index

    def place_ai_hit_hunting_mode(self):
        time.sleep(2)
        # pos_x, pos_y = self._battle_ship_service.make_ai_choice(self.__hunt_mode_heatmap)
        pos_x, pos_y = self._battle_ship_service.find_ship_positions()
        # self.print_game_boards(1)

        player_index, message = self._battle_ship_service.place_hit(pos_x, pos_y, 1)
        self.__heatmap = self._battle_ship_service.reconfigure_heatmap_matrix()
        # self._battle_ship_service.update_heatmap_matrix(heatmap, pos_x, pos_y)
        print(Fore.BLUE + 'AI chose positions ', pos_x + 1, chr(ord('A') + pos_y), Style.RESET_ALL)
        # self.print_heatmap()

        if 'hit' in message:
            self.__number_of_misses = 0
            # self._nr_of_hits += 1

            # self.__hunt_mode_heatmap = self._battle_ship_service.update_hunt_mode_heatmap(self.__hunt_mode_heatmap,
            #                                                                               pos_x, pos_y, 1)
            # print(f"Hits: {self._nr_of_hits}")
            self._battle_ship_service.add_hit_position(pos_x, pos_y)
            print(Fore.RED + 'Target status: ', 'hit', Style.RESET_ALL)
            if 'hit and sunk' in message:
                ship_id = int(message.split(',')[1])
                # print(ship_id)
                sunk_battle_ship = [ship for ship in self._battle_ship_service.player_battle_ship_repository if
                                    ship.id == ship_id]
                print(Fore.RED + 'Target status: ', 'hit and sunk ship of length: ', sunk_battle_ship[0].length,
                      Style.RESET_ALL)
                self._battle_ship_service.remove_ship_from_hits(sunk_battle_ship[0])
                if self._battle_ship_service.check_if_all_hits_from_the_same_battleship():
                    self.__hunt_mode = False
                else:
                    self.__hunt_mode = True

                self._battle_ship_service.remove_sunk_ship(ship_id, 0)


        else:
            self.__number_of_misses += 1
            # self.__hunt_mode_heatmap = self._battle_ship_service.update_hunt_mode_heatmap(self.__hunt_mode_heatmap,
            #                                                                               pos_x, pos_y, 0)
            # # if self.__hunt_mode is True:
            #     self._direction_index = (self._direction_index + 1) % 4

            print(Fore.LIGHTCYAN_EX + 'Target status: ', message, Style.RESET_ALL)
            # self._hunt_x = x
            # self._hunt_y = y

        return player_index

    def print_game_boards_texttable(self, player_index):
        board = []
        print(f"#####     Game Board     ######       ######    Target Board   ######")
        game_grid = self._battle_ship_service.get_game_grid(player_index)
        target_grid = self._battle_ship_service.get_target_grid(
            self._battle_ship_service.opposite_player_index(player_index))
        game_board = [[' ' for i in range(22)] for j in range(10)]
        target_board = self._battle_ship_service.get_target_grid(player_index)
        for i in range(10):
            for j in range(22):
                if j > 11:
                    game_board[i][j] = target_board[i][j-12]
                elif j == 10 or j == 11:
                    game_board[i][j] = ' '
                elif type(game_grid[i][j]) == BattleShip:
                    if game_grid[i][j].nr_of_blocks_hit == game_grid[i][j].length:
                        game_board[i][j] = 'X'
                    elif target_grid[i][j] == 1:
                        game_board[i][j] = 'X'
                    else:
                        game_board[i][j] = 'S'

        board.append(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                      'J', ' ', ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                      'J'])
        for line in game_board:
            board.append(line)

        board_img = Texttable()
        board_img.set_cols_width([1]*22)
        board_img.add_rows(board)
        print(board_img.draw())


    def print_game_boards(self, player_index):
        if player_index == 0:
            print(Fore.GREEN + f"#####   Player {player_index}   #######" + Style.RESET_ALL)
        else:
            print(Fore.BLUE + f"#####   Player {player_index}   #######" + Style.RESET_ALL)
        print(f"#####     Game Board     ######       ######    Target Board   ######")
        print(
            Fore.LIGHTWHITE_EX + "   A  B  C  D  E  F  G  H  I  J          A  B  C  D  E  F  G  H  I  J" + Style.RESET_ALL)
        game_grid = self._battle_ship_service.get_game_grid(player_index)
        target_grid = self._battle_ship_service.get_target_grid(
            self._battle_ship_service.opposite_player_index(player_index))
        game_board = [[0 for i in range(10)] for j in range(10)]
        for i in range(10):
            for j in range(10):
                if type(game_grid[i][j]) == BattleShip:
                    if game_grid[i][j].nr_of_blocks_hit == game_grid[i][j].length:
                        game_board[i][j] = 8
                    elif target_grid[i][j] == 1:
                        game_board[i][j] = 8
                    else:
                        game_board[i][j] = 1

        target_board = self._battle_ship_service.get_target_grid(player_index)

        for i in range(10):
            print(Fore.LIGHTWHITE_EX + f'{i + 1}' + (' ' if i == 9 else '  ') + Style.RESET_ALL, end='')
            for el in game_board[i]:
                if el == 8:
                    print(Fore.RED + 'X  ' + Style.RESET_ALL, end='')
                elif el == 1:
                    print(Fore.GREEN + '1  ' + Style.RESET_ALL, end='')
                else:
                    print(el, ' ', end='')
            print(end='     ')
            print(Fore.LIGHTWHITE_EX + f'{i + 1}' + (' ' if i == 9 else '  ') + Style.RESET_ALL, end='')
            for el in target_board[i]:
                if el == -1:
                    print(Fore.LIGHTCYAN_EX + '0  ' + Style.RESET_ALL, end='')
                elif el == 1:
                    print(Fore.RED + '1  ' + Style.RESET_ALL, end='')
                else:
                    print(el, ' ', end='')
            print()
            # print(chr(ord('A') + i), game_board[i], '    ', chr(ord('A') + i), target_board[i])

    def print_heatmap(self):
        print("HEATMAP: ")
        print("   A   B   C   D   E   F   G   H   I   J ")
        for index, line in enumerate(self.__heatmap):
            print(f'{index + 1}  ', end='')
            for el in line:
                print(el, end="  ")
            print()

    def run_console(self):
        configuration_phase_player_0 = True
        # configuration_phase_player_0 = False
        # player 1 is the AI
        # configuration_phase_player_1 = False
        print(
            Fore.RED + "Start configuration phase of the game, where each player places their ships on the board" + Style.RESET_ALL)
        player_index = 0

        self.__heatmap = self._battle_ship_service.create_heatmap_matrix()

        self._battle_ship_service.configure_game()
        # self.print_game_boards(0)
        self.print_game_boards_texttable(0)
        while True:
            try:
                if configuration_phase_player_0:
                    self.place_ship_from_console(0)

                    # self.print_game_boards(0)
                    self.print_game_boards_texttable(0)

                    if self._battle_ship_service.configuration_phase_finished(0):
                        print(
                            Fore.GREEN + "CONFIGURATION PHASE FINISHED!\nSTARTING THE GAME...\n\n" + Style.RESET_ALL)
                        configuration_phase_player_0 = False
                else:
                    if player_index == 1:  # the ai
                        # self.print_heatmap()
                        if not self.__hunt_mode:
                            index = self.place_ai_hit()
                        else:
                            index = self.place_ai_hit_hunting_mode()

                    else:
                        # self.print_game_boards(0)
                        self.print_game_boards_texttable(0)

                        # cheat mode for testing
                        # print("Game Board AI")
                        # self.print_game_boards(1)
                        index = self.place_hit_from_console(0)

                    if self._battle_ship_service.game_over(
                            self._battle_ship_service.opposite_player_index(player_index)):
                        print(f"🏆🏅🏆Player {'human' if player_index == 0 else 'ai'} won! Congratulations!")
                        self.print_game_boards(0)
                        self.print_game_boards(1)
                        # sys.exit()
                        break
                    player_index = index
            except Exception as e:
                print(Fore.RED + "Exception! ", e, Style.RESET_ALL)
