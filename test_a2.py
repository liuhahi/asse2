#!/usr/bin/env python3

import inspect
from pathlib import Path
from typing import Dict, List, Tuple

from testrunner import AttributeGuesser, OrderedTestCase, RedirectStdIO, TestMaster, skipIfFailed

Position = Tuple[int, int]


class Entity:
    def __init__(self): pass
    def get_id(self) -> str: pass
    def set_collide(self, collidable: bool): pass
    def can_collide(self) -> bool: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class Wall:
    def __init__(self): pass
    def get_id(self) -> str: pass
    def set_collide(self, collidable: bool): pass
    def can_collide(self) -> bool: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class Item:
    def __init__(self): pass
    def get_id(self) -> str: pass
    def set_collide(self, collidable: bool): pass
    def can_collide(self) -> bool: pass
    def on_hit(self, game: 'GameLogic'): pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class Key:
    def __init__(self): pass
    def get_id(self) -> str: pass
    def set_collide(self, collidable: bool): pass
    def can_collide(self) -> bool: pass
    def on_hit(self, game: 'GameLogic'): pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class MoveIncrease:
    def __init__(self, moves: int = 5): pass
    def get_id(self) -> str: pass
    def set_collide(self, collidable: bool): pass
    def can_collide(self) -> bool: pass
    def on_hit(self, game: 'GameLogic'): pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class Door:
    def __init__(self): pass
    def get_id(self) -> str: pass
    def set_collide(self, collidable: bool): pass
    def can_collide(self) -> bool: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class Player:
    def __init__(self, move_count: int): pass
    def get_id(self) -> str: pass
    def set_collide(self, collidable: bool): pass
    def can_collide(self) -> bool: pass
    def set_position(self, position: Position): pass
    def get_position(self) -> Position: pass
    def change_move_count(self, number: int): pass
    def moves_remaining(self) -> int: pass
    def add_item(self, item: Entity): pass
    def get_inventory(self) -> List[Entity]: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class GameLogic:
    def __init__(self, dungeon_name: str = "game1.txt"): pass
    def get_dungeon_size(self) -> int: pass
    def init_game_information(self) -> Dict[Position, Entity]: pass
    def get_game_information(self) -> Dict[Position, Entity]: pass
    def get_player(self) -> Player: pass
    def get_entity(self, position: Position) -> Entity: pass
    def get_entity_in_direction(self, direction: str) -> Entity: pass
    def collision_check(self, direction: str) -> bool: pass
    def new_position(self, direction: str) -> Position: pass
    def move_player(self, direction: str): pass
    def check_game_over(self) -> bool: pass
    def set_win(self, win: bool) : pass
    def won(self) -> bool: pass


class GameApp:
    def play(self): pass
    def draw(self): pass


class A2:
    Entity = Entity
    Wall = Wall
    Item = Item
    Key = Key
    MoveIncrease = MoveIncrease
    Door = Door
    Player = Player
    GameLogic = GameLogic
    GameApp = GameApp


class TestA2(OrderedTestCase):
    a2: A2


class TestFunctionality(TestA2):
    """ Base for all A2 functionality tests """

    TEST_DATA = (Path(__file__).parent / 'test_data').resolve()

    def load_test_data(self, filename: str):
        """ load test data from file """
        with open(self.TEST_DATA / filename, encoding='utf8') as file:
            return file.read()

    def write_test_data(self, filename: str, output: str):
        """ write test data to file """
        with open(self.TEST_DATA / filename, 'w', encoding='utf8') as file:
            file.write(output)


class TestDesign(TestA2):
    def test_clean_import(self):
        """ test no prints on import """
        self.assertIsCleanImport(self.a2, msg="You should not be printing on import for a1.py")

    def test_classes_and_functions_defined(self):
        """ test all specified classes and functions defined correctly """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)

        self._aggregate_class_and_functions_defined(a2, Entity)
        self._aggregate_class_and_functions_defined(a2, Wall, 'Entity')
        self._aggregate_class_and_functions_defined(a2, Item, 'Entity')
        self._aggregate_class_and_functions_defined(a2, Key, 'Item')
        self._aggregate_class_and_functions_defined(a2, MoveIncrease, 'Item')
        self._aggregate_class_and_functions_defined(a2, Door, 'Entity')
        self._aggregate_class_and_functions_defined(a2, Player, 'Entity')
        self._aggregate_class_and_functions_defined(a2, GameLogic)
        self._aggregate_class_and_functions_defined(a2, GameApp)

        self.aggregate_tests()

    def _aggregate_class_and_functions_defined(self, module, test_class, sub_class=None):
        """ helper method to test a class has all the required methods and signatures """
        cls_name = test_class.__name__
        if not self.aggregate(self.assertClassDefined, module, cls_name, tag=cls_name):
            return

        if sub_class and hasattr(module, sub_class):
            self.aggregate(self.assertIsSubclass, getattr(module, cls_name), getattr(module, sub_class))

        cls = getattr(module, cls_name)
        empty = inspect.Parameter.empty
        for func_name, func in inspect.getmembers(test_class, predicate=inspect.isfunction):
            params = inspect.signature(func).parameters
            if self.aggregate(self.assertFunctionDefined, cls, func_name, len(params), tag=f'{cls_name}.{func_name}'):
                # logic should be moved to testrunner.py
                for p1, p2 in zip(params.values(), inspect.signature(getattr(cls, func_name)).parameters.values()):
                    if p1.default == empty and p2.default != empty:
                        self.aggregate(self.fail,
                                       msg=f"expected '{p2.name}' to not have default value but got '{p2.default}'",
                                       tag=f'{cls_name}.{func_name}.{p1.name}')
                    elif p1.default != empty and p2.default == empty:
                        self.aggregate(self.fail,
                                       msg=f"expected '{p2.name}' to have default value '{p1.default}'",
                                       tag=f'{cls_name}.{func_name}.{p1.name}')
                    else:
                        self.aggregate(self.assertEqual, p1.default, p2.default,
                                       msg=f"expected '{p2.name}' to have default value '{p1.default}' but got '{p2.default}'",
                                       tag=f'{cls_name}.{func_name}.{p1.name}')

    def test_doc_strings(self):
        """ test all classes and functions have documentation strings """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        ignored = frozenset(('__str__', '__repr__'))
        for func_name, func in inspect.getmembers(a2, predicate=inspect.isfunction):
            if not self._is_a2_object(func):
                continue

            if func_name == 'main':
                continue

            self.aggregate(self.assertDocString, func)

        for cls_name, cls in inspect.getmembers(a2, predicate=inspect.isclass):
            if not self._is_a2_object(cls):
                continue

            self.aggregate(self.assertDocString, cls)
            defined = vars(cls)
            for func_name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
                if func_name not in ignored and func_name in defined:
                    self.aggregate(self.assertDocString, func)

        self.aggregate_tests()

    def _is_a2_object(self, obj):
        """ Check if the given object was defined in a3.py """
        try:
            file = inspect.getfile(obj)
            return file == self.a2.__file__
        except TypeError:  # caused by trying to get the file of a builtin
            return False


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='Entity')
class TestEntity(TestFunctionality):
    """ Test Entity """

    def test_get_id(self):
        """ test Entity.get_id """
        entity = self.a2.Entity()
        result = entity.get_id()
        self.assertEqual(result, 'Entity')

    def test_can_collide(self):
        """ test Entity.can_collide """
        entity = self.a2.Entity()
        result = entity.can_collide()
        self.assertIs(result, True)

    @skipIfFailed(test_name=test_can_collide)
    def test_set_collide(self):
        """ test Entity.set_collide """
        entity = self.a2.Entity()
        entity.set_collide(False)
        result = entity.can_collide()
        self.assertIs(result, False)

    def test_str(self):
        """ test Entity.__str__ """
        entity = self.a2.Entity()
        result = str(entity)
        self.assertEqual(result, "Entity('Entity')")

    def test_repr(self):
        """ test Entity.__repr__ """
        entity = self.a2.Entity()
        result = repr(entity)
        self.assertEqual(result, "Entity('Entity')")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='Wall')
class TestWall(TestFunctionality):
    """ Test Wall """

    def test_get_id(self):
        """ test Wall.get_id """
        wall = self.a2.Wall()
        result = wall.get_id()
        self.assertEqual(result, '#')

    def test_can_collide(self):
        """ test Wall.can_collide """
        wall = self.a2.Wall()
        result = wall.can_collide()
        self.assertIs(result, False)

    @skipIfFailed(test_name=test_can_collide)
    def test_set_collide(self):
        """ test Wall.set_collide """
        wall = self.a2.Wall()
        wall.set_collide(True)
        result = wall.can_collide()
        self.assertIs(result, True)

    def test_str(self):
        """ test Wall.__str__ """
        wall = self.a2.Wall()
        result = str(wall)
        self.assertEqual(result, "Wall('#')")

    def test_repr(self):
        """ test Wall.__repr__ """
        wall = self.a2.Wall()
        result = repr(wall)
        self.assertEqual(result, "Wall('#')")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='Item')
class TestItem(TestFunctionality):
    """ Test Item """

    def test_get_id(self):
        """ test Item.get_id """
        item = self.a2.Item()
        result = item.get_id()
        self.assertEqual(result, 'Entity')

    def test_can_collide(self):
        """ test Item.can_collide """
        item = self.a2.Item()
        result = item.can_collide()
        self.assertIs(result, True)

    @skipIfFailed(test_name=test_can_collide)
    def test_set_collide(self):
        """ test Item.set_collide """
        item = self.a2.Item()
        item.set_collide(False)
        result = item.can_collide()
        self.assertIs(result, False)

    def test_on_hit(self):
        """ test Item.on_hit """
        item = self.a2.Item()
        with self.assertRaises(NotImplementedError):
            # none is passed instead of an actual GameLogic object as
            # this method doesn't even need it and don't want to rely on
            # GameLogic.__init__ working to test this
            item.on_hit(None)

    def test_str(self):
        """ test Item.__str__ """
        item = self.a2.Item()
        result = str(item)
        self.assertEqual(result, "Item('Entity')")

    def test_repr(self):
        """ test Item.__repr__ """
        item = self.a2.Item()
        result = repr(item)
        self.assertEqual(result, "Item('Entity')")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='Key')
class TestKey(TestFunctionality):
    """ Test Key """

    def test_get_id(self):
        """ test Key.get_id """
        key = self.a2.Key()
        result = key.get_id()
        self.assertEqual(result, 'K')

    def test_can_collide(self):
        """ test Key.can_collide """
        key = self.a2.Key()
        result = key.can_collide()
        self.assertIs(result, True)

    @skipIfFailed(test_name=test_can_collide)
    def test_set_collide(self):
        """ test Key.set_collide """
        key = self.a2.Key()
        key.set_collide(False)
        result = key.can_collide()
        self.assertIs(result, False)

    def test_str(self):
        """ test Key.__str__ """
        key = self.a2.Key()
        result = str(key)
        self.assertEqual(result, "Key('K')")

    def test_repr(self):
        """ test Key.__repr__ """
        key = self.a2.Key()
        result = repr(key)
        self.assertEqual(result, "Key('K')")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='MoveIncrease')
class TestMoveIncrease(TestFunctionality):
    """ Test MoveIncrease """

    def test_get_id(self):
        """ test MoveIncrease.get_id """
        move_increase = self.a2.MoveIncrease(5)
        result = move_increase.get_id()
        self.assertEqual(result, 'M')

    def test_can_collide(self):
        """ test MoveIncrease.can_collide """
        move_increase = self.a2.MoveIncrease(5)
        result = move_increase.can_collide()
        self.assertIs(result, True)

    @skipIfFailed(test_name=test_can_collide)
    def test_set_collide(self):
        """ test MoveIncrease.set_collide """
        move_increase = self.a2.MoveIncrease(5)
        move_increase.set_collide(False)
        result = move_increase.can_collide()
        self.assertIs(result, False)

    def test_str(self):
        """ test MoveIncrease.__str__ """
        move_increase = self.a2.MoveIncrease(5)
        result = str(move_increase)
        self.assertEqual(result, "MoveIncrease('M')")

    def test_repr(self):
        """ test MoveIncrease.__repr__ """
        move_increase = self.a2.MoveIncrease(5)
        result = repr(move_increase)
        self.assertEqual(result, "MoveIncrease('M')")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='Door')
class TestDoor(TestFunctionality):
    """ Test Door """

    def test_get_id(self):
        """ test Door.get_id """
        door = self.a2.Door()
        result = door.get_id()
        self.assertEqual(result, 'D')

    def test_can_collide(self):
        """ test Door.can_collide """
        door = self.a2.Door()
        result = door.can_collide()
        self.assertIs(result, True)

    @skipIfFailed(test_name=test_can_collide)
    def test_set_collide(self):
        """ test Door.set_collide """
        door = self.a2.Door()
        door.set_collide(False)
        result = door.can_collide()
        self.assertIs(result, False)

    def test_str(self):
        """ test Door.__str__ """
        door = self.a2.Door()
        result = str(door)
        self.assertEqual(result, "Door('D')")

    def test_repr(self):
        """ test Door.__repr__ """
        door = self.a2.Door()
        result = repr(door)
        self.assertEqual(result, "Door('D')")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='Player')
class TestPlayer(TestFunctionality):
    """ Test Player """

    def test_get_id(self):
        """ test Player.get_id """
        player = self.a2.Player(5)
        result = player.get_id()
        self.assertEqual(result, 'O')

    def test_can_collide(self):
        """ test Player.can_collide """
        player = self.a2.Player(5)
        result = player.can_collide()
        self.assertIs(result, True)

    @skipIfFailed(test_name=test_can_collide)
    def test_set_collide(self):
        """ test Player.set_collide """
        player = self.a2.Player(5)
        player.set_collide(False)
        result = player.can_collide()
        self.assertIs(result, False)

    def test_get_position(self):
        """ test Player.get_position """
        player = self.a2.Player(5)
        result = player.get_position()
        self.assertIsNone(result)

    def test_set_position(self):
        """ test Player.set_position """
        player = self.a2.Player(5)
        player.set_position((1, 2))
        result = player.get_position()
        self.assertEqual(result, (1, 2))

    def test_moves_remaining(self):
        """ test Player.moves_remaining """
        player = self.a2.Player(5)
        result = player.moves_remaining()
        self.assertEqual(result, 5)

    @skipIfFailed(test_name=test_moves_remaining)
    def test_change_move_count_inc(self):
        """ test Player.change_move_count increase """
        player = self.a2.Player(5)
        player.change_move_count(2)
        result = player.moves_remaining()
        self.assertEqual(result, 7)

    @skipIfFailed(test_name=test_moves_remaining)
    def test_change_move_count_dec(self):
        """ test Player.change_move_count decrease """
        player = self.a2.Player(5)
        player.change_move_count(-1)
        result = player.moves_remaining()
        self.assertEqual(result, 4)

    def test_get_inventory(self):
        """ test Player.get_inventory """
        player = self.a2.Player(5)
        inventory = player.get_inventory()
        self.assertEqual(inventory, [])
        self.assertIs(inventory, player.get_inventory())

    @skipIfFailed(test_name=test_get_inventory)
    @skipIfFailed(TestKey, TestKey.test_repr)
    def test_add_item(self):
        """ test Player.add_item """
        player = self.a2.Player(5)
        key = self.a2.Key()
        player.add_item(key)
        result = player.get_inventory()
        self.assertEqual(result, [key])

    def test_str(self):
        """ test Player.__str__ """
        player = self.a2.Player(5)
        result = str(player)
        self.assertEqual(result, "Player('O')")

    def test_repr(self):
        """ test Player.__repr__ """
        player = self.a2.Player(5)
        result = repr(player)
        self.assertEqual(result, "Player('O')")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='GameLogic')
class TestGameLogic(TestFunctionality):
    """ Test GameLogic """

    def test_get_dungeon_size(self):
        """ test GameLogic.get_dungeon_size """
        game = self.a2.GameLogic('game1.txt')
        result = game.get_dungeon_size()
        self.assertEqual(result, 5)

    @skipIfFailed(TestWall, TestWall.test_repr)
    @skipIfFailed(TestKey, TestKey.test_repr)
    @skipIfFailed(TestDoor, TestDoor.test_repr)
    @skipIfFailed(TestPlayer, TestPlayer.test_repr)
    def test_init_game_information_1(self):
        """ test GameLogic.init_game_information game1.txt """
        game = self.a2.GameLogic('game1.txt')
        result = game.init_game_information()
        self.assertEqual(repr(result), "{(1, 3): Key('K'), (3, 2): Door('D'), (0, 0): Wall('#'), (0, 1): Wall('#'), (0, 2): Wall('#'), (0, 3): Wall('#'), (0, 4): Wall('#'), (1, 0): Wall('#'), (1, 2): Wall('#'), (1, 4): Wall('#'), (2, 0): Wall('#'), (2, 4): Wall('#'), (3, 0): Wall('#'), (3, 4): Wall('#'), (4, 0): Wall('#'), (4, 1): Wall('#'), (4, 2): Wall('#'), (4, 3): Wall('#'), (4, 4): Wall('#')}")

    @skipIfFailed(test_name=test_init_game_information_1)
    @skipIfFailed(TestMoveIncrease, TestMoveIncrease.test_repr)
    def test_init_game_information_2(self):
        """ test GameLogic.init_game_information game2.txt """
        game = self.a2.GameLogic('game2.txt')
        result = game.init_game_information()
        self.assertEqual(repr(result), "{(1, 6): Key('K'), (6, 3): Door('D'), (0, 0): Wall('#'), (0, 1): Wall('#'), (0, 2): Wall('#'), (0, 3): Wall('#'), (0, 4): Wall('#'), (0, 5): Wall('#'), (0, 6): Wall('#'), (0, 7): Wall('#'), (1, 0): Wall('#'), (1, 4): Wall('#'), (1, 7): Wall('#'), (2, 0): Wall('#'), (2, 7): Wall('#'), (3, 0): Wall('#'), (3, 7): Wall('#'), (4, 0): Wall('#'), (4, 1): Wall('#'), (4, 2): Wall('#'), (4, 7): Wall('#'), (5, 0): Wall('#'), (5, 7): Wall('#'), (6, 0): Wall('#'), (6, 7): Wall('#'), (7, 0): Wall('#'), (7, 1): Wall('#'), (7, 2): Wall('#'), (7, 3): Wall('#'), (7, 4): Wall('#'), (7, 5): Wall('#'), (7, 6): Wall('#'), (7, 7): Wall('#'), (6, 6): MoveIncrease('M')}")

    @skipIfFailed(test_name=test_init_game_information_2)
    def test_init_game_information_3(self):
        """ test GameLogic.init_game_information game3.txt """
        game = self.a2.GameLogic('game3.txt')
        result = game.init_game_information()
        self.assertEqual(repr(result), "{(8, 3): Key('K'), (1, 1): Door('D'), (0, 0): Wall('#'), (0, 1): Wall('#'), (0, 2): Wall('#'), (0, 3): Wall('#'), (0, 4): Wall('#'), (0, 5): Wall('#'), (0, 6): Wall('#'), (0, 7): Wall('#'), (0, 8): Wall('#'), (0, 9): Wall('#'), (0, 10): Wall('#'), (0, 11): Wall('#'), (1, 0): Wall('#'), (1, 11): Wall('#'), (2, 0): Wall('#'), (2, 11): Wall('#'), (3, 0): Wall('#'), (3, 11): Wall('#'), (4, 0): Wall('#'), (4, 11): Wall('#'), (5, 0): Wall('#'), (5, 11): Wall('#'), (6, 0): Wall('#'), (6, 11): Wall('#'), (7, 0): Wall('#'), (7, 1): Wall('#'), (7, 2): Wall('#'), (7, 3): Wall('#'), (7, 11): Wall('#'), (8, 0): Wall('#'), (8, 6): Wall('#'), (8, 7): Wall('#'), (8, 8): Wall('#'), (8, 9): Wall('#'), (8, 11): Wall('#'), (9, 0): Wall('#'), (9, 9): Wall('#'), (9, 11): Wall('#'), (10, 0): Wall('#'), (10, 11): Wall('#'), (11, 0): Wall('#'), (11, 1): Wall('#'), (11, 2): Wall('#'), (11, 3): Wall('#'), (11, 4): Wall('#'), (11, 5): Wall('#'), (11, 6): Wall('#'), (11, 7): Wall('#'), (11, 8): Wall('#'), (11, 9): Wall('#'), (11, 10): Wall('#'), (11, 11): Wall('#'), (9, 8): MoveIncrease('M')}")

    @skipIfFailed(test_name=test_init_game_information_1)
    def test_init_game_information_unique_walls(self):
        """ test GameLogic.init_game_information unique Walls """
        game = self.a2.GameLogic('game3.txt')
        result = game.init_game_information()
        walls = set(e for e in result.values() if isinstance(e, self.a2.Wall))
        self.assertEqual(len(walls), 52)

    def test_get_game_information(self):
        """ test GameLogic.get_game_information """
        game = self.a2.GameLogic('game1.txt')
        result = game.get_game_information()
        self.assertEqual(repr(result), "{(1, 3): Key('K'), (3, 2): Door('D'), (0, 0): Wall('#'), (0, 1): Wall('#'), (0, 2): Wall('#'), (0, 3): Wall('#'), (0, 4): Wall('#'), (1, 0): Wall('#'), (1, 2): Wall('#'), (1, 4): Wall('#'), (2, 0): Wall('#'), (2, 4): Wall('#'), (3, 0): Wall('#'), (3, 4): Wall('#'), (4, 0): Wall('#'), (4, 1): Wall('#'), (4, 2): Wall('#'), (4, 3): Wall('#'), (4, 4): Wall('#')}")

    @skipIfFailed(TestPlayer, TestPlayer.test_repr)
    def test_get_player(self):
        """ test GameLogic.get_player """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        self.assertIsInstance(player, self.a2.Player)
        self.assertEqual(repr(player), "Player('O')")
        self.assertIs(game.get_player(), player)
        self.assertEqual(player.moves_remaining(), 7)

    def test_init_game_sets_player_pos(self):
        """ test GameLogic.init_game_information sets player position """
        game = self.a2.GameLogic('game1.txt')
        game.get_game_information()
        player = game.get_player()
        result = player.get_position()
        self.assertEqual(result, (2, 1))

    def test_get_entity_none(self):
        """ test GameLogic.get_entity None """
        game = self.a2.GameLogic('game1.txt')
        entity = game.get_entity((2, 1))
        self.assertIsNone(entity)

    @skipIfFailed(TestWall, TestWall.test_repr)
    def test_get_entity_found(self):
        """ test GameLogic.get_entity found """
        game = self.a2.GameLogic('game1.txt')
        entity = game.get_entity((0, 0))
        self.assertIsInstance(entity, self.a2.Wall)
        self.assertEqual(repr(entity), "Wall('#')")

    def test_get_entity_out_of_bounds(self):
        """ test GameLogic.get_entity out_of_bounds """
        game = self.a2.GameLogic('game1.txt')
        result = game.get_entity((10, 10))
        self.assertIsNone(result)

    def test_get_entity_in_direction_wall(self):
        """ test GameLogic.get_entity_in_direction Wall """
        game = self.a2.GameLogic('game1.txt')
        entity = game.get_entity_in_direction('A')
        self.assertIsInstance(entity, self.a2.Wall)
        self.assertEqual(repr(entity), "Wall('#')")

    def test_get_entity_in_direction_empty(self):
        """ test GameLogic.get_entity_in_direction Empty """
        game = self.a2.GameLogic('game1.txt')
        entity = game.get_entity_in_direction('W')
        self.assertIsNone(entity)

    def test_collision_check_wall(self):
        """ test GameLogic.collision_check Wall """
        game = self.a2.GameLogic('game1.txt')
        result = game.collision_check('A')
        self.assertIs(result, True)

    def test_collision_check_empty(self):
        """ test GameLogic.collision_check Empty """
        game = self.a2.GameLogic('game1.txt')
        result = game.collision_check('D')
        self.assertIs(result, False)

    @skipIfFailed(test_name=test_get_player)
    def test_collision_check_entity(self):
        """ test GameLogic.collision_check Entity """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        player.set_position((2, 2))
        result = game.collision_check('S')
        self.assertIs(result, False)

    def test_new_position_w(self):
        """ test GameLogic.new_position W """
        game = self.a2.GameLogic('game1.txt')
        result = game.new_position('W')
        self.assertEqual(result, (1, 1))

    def test_new_position_s(self):
        """ test GameLogic.new_position S """
        game = self.a2.GameLogic('game1.txt')
        result = game.new_position('S')
        self.assertEqual(result, (3, 1))

    def test_new_position_a(self):
        """ test GameLogic.new_position S """
        game = self.a2.GameLogic('game1.txt')
        result = game.new_position('A')
        self.assertEqual(result, (2, 0))

    def test_new_position_d(self):
        """ test GameLogic.new_position S """
        game = self.a2.GameLogic('game1.txt')
        result = game.new_position('D')
        self.assertEqual(result, (2, 2))

    @skipIfFailed(test_name=test_get_player)
    @skipIfFailed(TestPlayer, test_name=TestPlayer.test_get_position)
    def test_move_player_open(self):
        """ test GameLogic.move_player open """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        game.move_player('W')
        result = player.get_position()
        self.assertEqual(result, (1, 1))
        self.assertEqual(player.moves_remaining(), 7)

    @skipIfFailed(test_name=test_move_player_open)
    def test_move_player_wall(self):
        """ test GameLogic.move_player wall """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        game.move_player('A')
        result = player.get_position()
        self.assertEqual(result, (2, 0))
        self.assertEqual(player.moves_remaining(), 7)

    def test_check_game_over_false(self):
        """ test GameLogic.check_game_over False """
        game = self.a2.GameLogic('game1.txt')
        result = game.check_game_over()
        self.assertIs(result, False)

    @skipIfFailed(test_name=test_get_player)
    def test_check_game_over_true(self):
        """ test GameLogic.check_game_over True """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        player.change_move_count(-7)
        result = game.check_game_over()
        self.assertIs(result, True)

    def test_won(self):
        """ test GameLogic.won """
        game = self.a2.GameLogic('game1.txt')
        result = game.won()
        self.assertIs(result, False)

    @skipIfFailed(test_name=test_won)
    def test_set_win(self):
        """ test GameLogic.set_win """
        game = self.a2.GameLogic('game1.txt')
        game.set_win(True)
        result = game.won()
        self.assertIs(result, True)

    @skipIfFailed(test_name=test_get_player)
    @skipIfFailed(test_name=test_get_entity_found)
    @skipIfFailed(test_name=test_get_entity_none)
    def test_key_on_hit(self):
        """ test GameLogic with Key.on_hit """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        player.set_position((1, 3))
        key = game.get_entity((1, 3))
        key.on_hit(game)
        self.assertIn(key, player.get_inventory())
        self.assertIsNone(game.get_entity((1, 3)))

    @skipIfFailed(test_name=test_get_player)
    @skipIfFailed(test_name=test_get_entity_found)
    @skipIfFailed(test_name=test_get_entity_none)
    @skipIfFailed(TestPlayer, TestPlayer.test_set_position)
    def test_move_increase_on_hit(self):
        """ test GameLogic with MoveIncrease.on_hit """
        game = self.a2.GameLogic('game2.txt')
        player = game.get_player()
        player.set_position((6, 6))
        move_increase = game.get_entity((6, 6))
        move_increase.on_hit(game)
        self.assertIsNone(game.get_entity((6, 6)))
        self.assertEqual(player.moves_remaining(), 17)

    @skipIfFailed(test_name=test_key_on_hit)
    @skipIfFailed(test_name=test_won)
    def test_door_on_hit_with_key(self):
        """ test GameLogic with Door.on_hit with Key """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        player.set_position((1, 3))
        key = game.get_entity((1, 3))
        key.on_hit(game)
        door = game.get_entity((3, 2))
        door.on_hit(game)
        self.assertIs(game.won(), True)

    @skipIfFailed(test_name=test_won)
    def test_door_on_hit_without_key(self):
        """ test GameLogic with Door.on_hit without Key """
        game = self.a2.GameLogic('game1.txt')
        player = game.get_player()
        player.set_position((1, 3))
        door = game.get_entity((3, 2))
        with RedirectStdIO(stdout=True) as stdio:
            door.on_hit(game)
        self.assertIs(game.won(), False)
        self.assertEqual(stdio.stdout, "You don't have the key!\n")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='GameApp')
class TestGameApp(TestFunctionality):
    """ Test GameApp """

    def _run_play(self, file_in: str, file_out: str, stop_early: bool):
        """ runs the play function and captures output """
        data_in = self.load_test_data(file_in)

        error = None
        result = None
        game = self.a2.GameApp()
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.stdin = data_in
            try:
                result = game.play()
            except EOFError as err:
                error = err

        # self.write_test_data(file_out, stdio.stdinout)
        expected = self.load_test_data(file_out)
        if error is not None and not stop_early:
            last_output = "\n\n".join(stdio.stdinout.rsplit("\n\n")[-4:])
            raise AssertionError(
                f'Your program is asking for more input when it should have ended\nEOFError: {error}\n\n{last_output}'
            ).with_traceback(error.__traceback__)

        return expected, result, stdio

    def assertPlay(self, file_in: str, file_out: str, stop_early: bool = False):
        """ assert the play function ran correctly """
        expected, result, stdio = self._run_play(file_in, file_out, stop_early=stop_early)
        self.assertMultiLineEqual(stdio.stdinout, expected)
        if stdio.stdin != '':
            self.fail(msg="Not all input was read")
        self.assertIsNone(result, msg="play function should not return a non None value")

    def test_draw(self):
        """ test GameApp.draw """
        app = self.a2.GameApp()
        with RedirectStdIO(stdout=True) as stdio:
            app.draw()

        expected = self.load_test_data('game_draw.out')
        self.assertEqual(stdio.stdout, expected)

    def test_play_help(self):
        """ test GameApp.play help """
        self.assertPlay('game_help.in', 'game_help.out', stop_early=True)

    def test_play_quit_y(self):
        """ test GameApp.play quit y """
        self.assertPlay('game_quit_y.in', 'game_quit_y.out')

    def test_play_quit_n(self):
        """ test GameApp.play quit n """
        self.assertPlay('game_quit_n.in', 'game_quit_n.out', stop_early=True)

    def test_play_win(self):
        """ test GameApp.play win """
        self.assertPlay('game_win.in', 'game_win.out')

    def test_play_lose(self):
        """ test GameApp.play lose """
        self.assertPlay('game_lose.in', 'game_lose.out')

    def test_play_investigate(self):
        """ test GameApp.play investigate """
        self.assertPlay('game_investigate.in', 'game_investigate.out')

    def test_invalid(self):
        """ test GameApp.play invalid inputs """
        self.assertPlay('game_invalid.in', 'game_invalid.out', stop_early=True)

    @skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined, tag='GameLogic.__init__.dungeon_name')
    def test_move_increase(self):
        """ test GameApp.play game2.txt MoveIncrease """
        # have to patch the defaults since GameApp.__init__ doesn't take the filename
        _defaults = self.a2.GameLogic.__init__.__defaults__
        self.a2.GameLogic.__init__.__defaults__ = ('game2.txt',)

        try:
            self.assertPlay('game_move_inc.in', 'game_move_inc.out')
        finally:
            # make sure to restore defaults even on test fail
            self.a2.GameLogic.__init__.__defaults__ = _defaults


def main():
    test_cases = [
        TestDesign,
        TestEntity,
        TestWall,
        TestItem,
        TestKey,
        TestMoveIncrease,
        TestDoor,
        TestPlayer,
        TestGameLogic,
        TestGameApp
    ]

    master = TestMaster(max_diff=None,
                        timeout=1,
                        suppress_stdout=True,
                        include_no_print=True,
                        scripts=[
                            ('a2', 'a2.py')
                        ])
    master.run(test_cases)


if __name__ == '__main__':
    main()
