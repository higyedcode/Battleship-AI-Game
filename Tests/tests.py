import unittest

from domain.battleShip import BattleShip
from exceptions.exceptions import InvalidShipProperty
from repository.GameGridRepository import GameGridRepository
from repository.battleShipRepository import BattleShipRepository
from service.battleShipService import BattleShipService


class DomainTests(unittest.TestCase):
    def setUp(self):
        self.ship = BattleShip(1, 4, 3)
        self.ship.start_position = (0, 0)
        self.ship.end_position = (1, 6)

    def testAttributes(self):
        self.assertEqual(self.ship.id, 1)
        self.assertEqual(self.ship.length, 4)
        self.assertEqual(self.ship.nr_of_blocks_hit, 3)
        self.assertEqual(self.ship.start_position, (0, 0))
        self.assertEqual(self.ship.end_position, (1, 6))


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repository = BattleShipRepository()
        self.game_grid = GameGridRepository()

    def testRepositoryIntialValue(self):
        self.assertEqual(len(self.repository.repository), 5)
        self.assertEqual(self.repository.repository[0], BattleShip(1, 5, 0))
        self.assertEqual(self.repository.repository[2], BattleShip(3, 3, 0))

    def test_find_by_length(self):
        self.assertTrue(self.repository.find_by_length(5), BattleShip(1, 5, 0))

    def test_remove(self):
        self.repository.remove(3)
        self.assertEqual(len(self.repository.repository), 4)
        self.assertEqual(self.repository.repository,
                         [BattleShip(1, 5, 0), BattleShip(2, 4, 0), BattleShip(4, 3, 0), BattleShip(5, 2, 0)])

    def test_game_grid_initial_value(self):
        for i in range(10):
            for j in range(10):
                self.assertEqual(self.game_grid.game_grid[i][j], 0)

    def test_update_grid(self):
        self.game_grid.update(1,6,10)
        self.assertEqual(self.game_grid.game_grid[1][6], 10)

class ServiceTests(unittest.TestCase):
    def setUp(self):
        self._battle_ship_service = BattleShipService([BattleShipRepository(), BattleShipRepository()],[GameGridRepository(),GameGridRepository()], [GameGridRepository(), GameGridRepository()])
        self._battle_ship_service.place_battle_ship(5, (0, 0), (4, 0), 0)
        self._battle_ship_service.place_battle_ship(4, (2, 6), (5, 6), 0)
        self._battle_ship_service.place_battle_ship(3, (4, 3), (4, 5), 0)
        self._battle_ship_service.place_battle_ship(3, (6, 5), (6, 7), 0)
        self._battle_ship_service.place_battle_ship(2, (0, 1), (0, 2), 0)
        self._battle_ship_service.place_battle_ship(5, (1, 0), (5, 0), 1)
        self._battle_ship_service.place_battle_ship(4, (3, 6), (6, 6), 1)
        self._battle_ship_service.place_battle_ship(3, (9, 6), (9, 8), 1)
        self._battle_ship_service.place_battle_ship(3, (6, 0), (6, 2), 1)
        self._battle_ship_service.place_battle_ship(2, (8, 1), (8, 2), 1)
    def test_place_ships(self):
        with self.assertRaises(InvalidShipProperty):
            self._battle_ship_service.place_battle_ship(2, (8, 1), (8, 2), 1)
        for i in range(8, 9):
            for j in range(1, 3):
                self.assertEqual(self._battle_ship_service.get_game_grid(1)[i] [j], BattleShip(5,2,0))
    def test_check_position(self):
        self.assertTrue(self._battle_ship_service.check_position(5, (0, 0),(0,4), 1))

    def test_game_over(self):
        self.assertFalse(self._battle_ship_service.game_over(0))

    def test_placing_hits(self):
        player_index, message = self._battle_ship_service.place_hit(8,1,0)
        self.assertEqual(player_index,0)
        self.assertEqual(message, 'hit')
        player_index, message = self._battle_ship_service.place_hit(8, 2, 0)
        self.assertEqual(player_index, 1)
        self.assertEqual(message, 'hit and sunk,5')
        player_index, message = self._battle_ship_service.place_hit(6, 7, 0)
        self.assertEqual(player_index, 1)
        self.assertEqual(message, 'miss')

    def test_initial_heatmap(self):
        expected_heatmap = []
        expected_heatmap.append([10, 15, 19, 21, 22, 22, 21, 19,15,10])
        expected_heatmap.append([15,20,24,26,27,27,26,24,20 , 15])
        expected_heatmap.append([19,24,28,30,31,31,30,28,24,19])
        expected_heatmap.append([21,26,30,32,33,33,32,30,26,21])
        expected_heatmap.append([22,27,31,33,34,34,33,31,27,22])
        expected_heatmap.append([22,27,31,33,34,34,33,31,27,22])
        expected_heatmap.append([21,26,30,32,33,33,32,30,26,21])
        expected_heatmap.append([19,24,28,30,31,31,30,28,24,19])
        expected_heatmap.append([15,20,24,26,27,27,26,24,20,15])
        expected_heatmap.append([10,15,19,21,22,22,21,19,15,10])

        heatmap = self._battle_ship_service.create_heatmap_matrix()
        self.assertEqual(
            heatmap,expected_heatmap
        )


if __name__ == '__main__':
    unittest.main()
