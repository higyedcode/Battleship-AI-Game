import copy
import tkinter

from domain.battleShip import BattleShip
from repository.GameGridRepository import GameGridRepository
from repository.battleShipRepository import BattleShipRepository
from service.battleShipService import BattleShipService
from ui.console import Console
from ui.gui import GUI

player1_battle_ship_repository = BattleShipRepository()
player1_game_grid_repository = GameGridRepository()
player1_target_grid_repository = GameGridRepository()

player2_battle_ship_repository = BattleShipRepository()
player2_game_grid_repository = GameGridRepository()
player2_target_grid_repository = GameGridRepository()

battle_ship_service = BattleShipService([player1_battle_ship_repository, player2_battle_ship_repository],
                                        [player1_game_grid_repository, player2_game_grid_repository],
                                        [player1_target_grid_repository, player2_target_grid_repository])

console = Console(battle_ship_service)
gui = GUI(battle_ship_service)


class TkExceptionHandler:
    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        if self.subst:
            args = self.subst(*args)
        return self.func(*args)


tkinter.CallWrapper = TkExceptionHandler

if __name__ == '__main__':
    # console.run_console()
    gui.run()
