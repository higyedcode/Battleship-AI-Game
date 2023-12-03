import sys
import time
import tkinter
from dataclasses import dataclass
import tkinter.messagebox as messagebox

from domain.battleShip import BattleShip
from service.battleShipService import BattleShipService
from tkinter import *


@dataclass
class GUI:
    _battle_ship_service: BattleShipService
    __number_of_misses = 0
    _button_list_player = []
    _button_list_ai = []
    __hunt_mode = False
    __heatmap = None
    __heatmap_inverse_strategy = None
    __window = Tk()
    _selected = False
    _selected_position = []
    _message_lbl = None
    _text = "    Welcome to BattleShip! Start configuration phase..."
    _active_ships_lbl = None
    _configuration_mode = True
    _player_index = 0

    def game_over(self, winner):
        if winner == 0:
            self._message_lbl.config(text='🤯🏆🏅CONGRATULATIONS! YOU WON!', background='green', foreground='white')
        else:
            self._message_lbl.config(text='😶‍🌫️😰😭GAME OVER! YOU LOST!', foreground='white', background='red')
        for i in range(10):
            for j in range(10):
                if type(self._battle_ship_service.get_game_grid(1)[i][j]) == BattleShip:
                    if self._button_list_ai[i][j]['bg'] != 'red':
                        self._button_list_ai[i][j].config(bg='yellow')
        self.__window.update()

    def place_hit(self, i, j):
        self._active_ships_lbl.config(text=f'You chose positions {i + 1}{chr(ord("A") + j)}')
        self._player_index, message = self._battle_ship_service.place_hit(i, j, 0)
        self._message_lbl.config(text=message)
        if 'hit' in message:
            self._button_list_ai[i][j].config(bg='red')
        if 'miss' in message:
            self._button_list_ai[i][j].config(bg='white')
        if 'sunk' in message:
            ship_id = int(message.split(',')[1])
            sunk_battle_ship = [ship for ship in self._battle_ship_service.ai_battle_ship_repository if
                                ship.id == ship_id]
            self._message_lbl.config(text=f'Hit and sunk ship of length {sunk_battle_ship[0].length}')
            self._battle_ship_service.remove_sunk_ship(ship_id, 1)
            if len(self._battle_ship_service.ai_battle_ship_repository) == 0:
                self.game_over(0)
        self.__window.update()
        if self._player_index == 1:
            for i in range(10):
                for j in range(10):
                    self._button_list_ai[i][j]['state'] = tkinter.DISABLED
            while self._player_index != 0:
                if not self.__hunt_mode:
                    self._player_index = self.place_ai_hit()
                    self.__window.update()
                else:
                    self._player_index = self.place_ai_hit_hunting_mode()
                    self.__window.update()
            time.sleep(2)
            for i in range(10):
                for j in range(10):
                    self._button_list_ai[i][j]['state'] = tkinter.NORMAL

    def place_ai_hit(self):
        time.sleep(2)
        if self.__number_of_misses > 4:
            print("INVERSE MODE!")
            pos_x, pos_y = self._battle_ship_service.make_ai_choice_inverse(self.__heatmap_inverse_strategy)
            # in inverse strategy we just put the already chosen points as 0
        else:
            pos_x, pos_y = self._battle_ship_service.make_ai_choice(self.__heatmap)

        player_index, message = self._battle_ship_service.place_hit(pos_x, pos_y, 1)

        self.__heatmap = self._battle_ship_service.reconfigure_heatmap_matrix()
        self._active_ships_lbl.config(text=f'AI chose positions {pos_x + 1}{chr(ord("A") + pos_y)}')
        self.__heatmap_inverse_strategy[pos_x][pos_y] = 0

        if 'hit' in message:
            self.__number_of_misses = 0
            self._message_lbl.config(text=f'AI Target status: {message}')
            self._button_list_player[pos_x][pos_y].config(bg='red', text='X', fore='white')

            if message == 'hit':
                self.__hunt_mode = True
                self._battle_ship_service.add_hit_position(pos_x, pos_y)

        else:
            self._message_lbl.config(text=f'AI Target status: {message}')
            self.__number_of_misses += 1

        self.__window.update()
        return player_index

    def place_ai_hit_hunting_mode(self):
        time.sleep(2)

        pos_x, pos_y = self._battle_ship_service.find_ship_positions()

        player_index, message = self._battle_ship_service.place_hit(pos_x, pos_y, 1)
        self.__heatmap = self._battle_ship_service.reconfigure_heatmap_matrix()
        self.__heatmap_inverse_strategy[pos_x][pos_y] = 0

        self._active_ships_lbl.config(text=f'AI chose positions {pos_x + 1}{chr(ord("A") + pos_y)}')

        if 'hit' in message:
            self.__number_of_misses = 0
            self._button_list_player[pos_x][pos_y].config(bg='red', text='X', fore='white')
            self._battle_ship_service.add_hit_position(pos_x, pos_y)
            self._message_lbl.config(text=f'AI Target status: hit')
            if 'hit and sunk' in message:
                ship_id = int(message.split(',')[1])
                sunk_battle_ship = [ship for ship in self._battle_ship_service.player_battle_ship_repository if
                                    ship.id == ship_id]
                self._message_lbl.config(
                    text=f'AI Target status: hit and sunk ship of length: {sunk_battle_ship[0].length}')

                self._battle_ship_service.remove_ship_from_hits(sunk_battle_ship[0])
                if self._battle_ship_service.check_if_all_hits_from_the_same_battleship():
                    self.__hunt_mode = False
                else:
                    self.__hunt_mode = True

                self._battle_ship_service.remove_sunk_ship(ship_id, 0)
                if len(self._battle_ship_service.player_battle_ship_repository) == 0:
                    self.game_over(1)


        else:
            self.__number_of_misses += 1
            self._message_lbl.config(text=f'Target status: miss')

        self.__window.update()
        return player_index

    def place_ship(self, i, j):
        if self._selected:
            length = abs(i - self._selected_position[0] + j - self._selected_position[1]) + 1
            print(length, i, j, self._selected_position[0], self._selected_position[1])
            start_x = min(i, self._selected_position[0])
            end_x = max(i, self._selected_position[0])
            start_y = min(j, self._selected_position[1])
            end_y = max(j, self._selected_position[1])
            self._battle_ship_service.place_battle_ship(length, (start_x, start_y),
                                                        (end_x, end_y), 0)

            for i in range(start_x, end_x + 1):
                for j in range(start_y, end_y + 1):
                    self._button_list_player[i][j].config(bg=f"#{2 + length * 2 - 3}42b2b")
            self._active_ships_lbl.config(
                text=f'Place one of your remaining ships of length {self._battle_ship_service.ships_len_not_yet_placed_by_player} on the game board')

            if len(self._battle_ship_service.ships_len_not_yet_placed_by_player) == 0:
                for i in range(10):
                    for j in range(10):
                        self._button_list_ai[i][j]['state'] = tkinter.NORMAL
                for i in range(10):
                    for j in range(10):
                        self._button_list_player[i][j]['state'] = tkinter.DISABLED
                self._message_lbl.config(text='Game ON!')
                self._active_ships_lbl.config(
                    text='Target one of your opponent\'s ships and try to sink his ships before he sinks yours!')

            self.__window.update()
            self._selected = False
            self._selected_position.clear()
        else:
            self._selected = True
            self._selected_position.append(i)
            self._selected_position.append(j)

    def configure_board(self):
        self._message_lbl = Label(text=self._text, font=('Cascadia Mono', 15), bg='#3176a3', pady=30,
                                  foreground='white', anchor='n')
        self._message_lbl.grid(columnspan=24, row=0, column=0)
        for z in range(2):
            label = Button(width=6, height=2, bg='#3176a3')
            label.grid(column=1 + 13 * z, row=1)
            for i in range(10):
                label = Button(width=6, height=2, bg='#3176a3', text=f'{chr(ord("A") + i)}', foreground='white')
                label.grid(column=(i + 1) + 13 * z, row=1)

        for i in range(10):
            row = []
            for j in range(10):
                label = Button(width=6, height=2, bg='#3176a3', text=f'{j + 1}', foreground='white', border=1)
                label.grid(column=0, row=j + 2)
                button = Button(text='', bg='#5bb7f5', fg='black', width=6, height=2,
                                command=lambda x=i, y=j: self.place_ship(x, y))
                button.grid(column=j + 1, row=i + 2)

                row.append(button)
            self._button_list_player.append(row)

        for i in range(10):
            label = Label(width=4, height=2, bg='#3176a3')
            label.grid(column=11, row=i + 2)
        for i in range(10):
            label = Label(width=4, height=2, bg='#3176a3')
            label.grid(column=12, row=i + 2)

        for i in range(10):
            row = []
            for j in range(10):
                label = Button(width=6, height=2, bg='#3176a3', text=f'{j + 1}', foreground='white', border=1)
                label.grid(column=13, row=j + 2)
                button = Button(text='', bg='#5bb7f5', fg='black', width=6, height=2, state=tkinter.DISABLED,
                                command=lambda x=i, y=j: self.place_hit(x, y))
                button.grid(column=14 + j, row=i + 2)
                row.append(button)
            self._button_list_ai.append(row)
        self._active_ships_lbl = Label(
            text=f'Place one of your remaining ships of length {self._battle_ship_service.ships_len_not_yet_placed_by_player} on the game board',
            font=('Cascadia Mono', 10), bg='#3176a3', pady=30, foreground='white')
        self._active_ships_lbl.grid(row=12, column=2, columnspan=24)

    def end(self):
        self.__window.destroy()
        sys.exit()

    def run(self):
        self.__heatmap = self._battle_ship_service.create_heatmap_matrix()
        self.__heatmap_inverse_strategy = self._battle_ship_service.create_heatmap_matrix()
        self._battle_ship_service.configure_game()

        self.__window.title("BattleShip Game")
        self.__window.configure(padx=30, pady=5, bg='#3176a3')
        self.configure_board()
        self.__window.protocol("WM_DELETE_WINDOW", lambda: self.end())

        while True:
            try:
                self.__window.mainloop()
            except Exception as e:
                self._selected_position.clear()
                self._selected = False
                messagebox.showerror('Error! ', str(e))
