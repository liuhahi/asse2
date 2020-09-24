"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from a2_support import *

# Fill these in with your details
__author__ = "{{user.name}} ({{user.id}})"
__email__ = ""
__date__ = ""

# Write your code here

class GameLogic:
    def __init__(self, dungeon_name="game1.txt"):
        """Constructor of the GameLogic class.
        Parameters:
            dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        #you need to implement the Player class first.
        self._player = Player(GAME_LEVELS[dungeon_name])
        #you need to implement the init_game_information() method for this.
        self._game_information = self.init_game_information()
        self._win = False

    def init_game_information(self):
        dungeon = {}
        for i in range(self._dungeon_size):            
            for j in range(self._dungeon_size):
                entity = ""
                if self._dungeon[i][j] == WALL:
                    entity = Wall()
                elif self._dungeon[i][j] == KEY:
                    entity = Key()
                elif self._dungeon[i][j] == PLAYER:
                    self._player.set_position((i,j))
                    entity = self._player
                elif self._dungeon[i][j] == DOOR:
                    entity = DOOR
                if entity != "":                                          
                    dungeon[(i,j)] = entity
        return dungeon
    def get_game_information(self):
        return self._game_information

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.
        Parameters:
            entity (str): the id of an entity.
        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))
        return positions

    # Write your code here
    def get_player(self):
        return self._player
    
    def get_entity(self, position):
        if position in self._game_information:
            return self._game_information[position]
        else:
            return None
    def get_entity_in_direction(self, direction):
        direction = self._player.get_position() + DIRECTIONS[direction]
        print(direction)
        if direction[0] > self._dungeon_size or direction[1] > self._dungeon_size or direction[0] < 0 or direction[1] < 0:
            return None
        else:
            return self._game_information[direction]
    def collision_check(self, direction):
        current = self._player.get_position()
        position = (current[0] + DIRECTIONS[direction][0], current[1] + DIRECTIONS[direction][1])
        if position[0] > self._dungeon_size or position[1] > self._dungeon_size or position[0] < 0 or position[1] < 0:
            return False
        elif position in self._game_information and self._game_information[position].get_id() == WALL:
            return False
        else:
            return True
    def new_position(self, direction):
        return (self._player.get_position()[0] + DIRECTIONS[direction][0], self._player.get_position()[1] + DIRECTIONS[direction][1])
        
    def move_player(self, direction):
        self._player.set_position(self.new_position(direction))
    def check_game_over(self):
        return self._win
    def set_win(self, win):
        self._win = win
    def won(self):
        return self._win
    def get_dungeon_size(self):
        return self._dungeon_size
        
class Entity:
    ''' entity class'''
    def __init__(self):
        self.id = 'Entity'
        self.collidable = True
    def get_id(self):
        return self.id
    def set_collide(self, collidable):
        self.collidable = collidable
    def can_collide(self):
        return self.collidable
    def __str__(self):
        return f"{self.__class__.__name__}('{self.id}')"
    def __repr__(self):
        return str(self)

class Wall(Entity):
    ''' wall class'''
    def __init__(self):
        super().__init__()
        self.id = '#'    	

class Item(Entity):
    ''' item class'''
    def __init__(self):
        super().__init__()
    def on_hit(self, game):
        raise NotImplementedError()

class Key(Item):
    ''' key class'''
    def __init__(self):
        super().__init__()
        self.id = KEY
    def on_hit(self, game):
        raise NotImplementedError()	

class MoveIncrease():
    ''' key class'''
    def __init__(self):
        super().__init__()
        self.id = MOVE_INCREASE
    def on_hit(self, game):
        raise NotImplementedError()	      

class Door(Entity):
    ''' key class'''
    def __init__(self):
        super().__init__()
        self.id = DOOR
    def on_hit(self, game):
        print("You don't have the key!")

class Player(Entity):
    def __init__(self, move_count):
        super().__init__()
        self.move_count = move_count
        self.id = PLAYER
        self.position = tuple()
        self.move = 0
        self.inventory = []

    def set_position(self, position):
        self.position = position
    def get_position(self):
        return self.position
    def change_move_count(self, number):
        self.move += number
    def moves_remaining(self):
        return self.move
    def add_item(self, item):
        self.inventory.append(item)        
    def get_inventory(self):
        return self.inventory

class GameApp:
    game = GameLogic()
    game.init_game_information()
    print(game.get_positions(PLAYER))
    print(game.get_positions(WALL))
    print(game.get_player())
    print(game.get_game_information())
    print(game.get_player().get_position())
    print(game.collision_check("W"))
    print(game.new_position("D"))
    print(game.check_game_over())
    print(game.set_win(True))
    print(game.won())
    pass


def main():
    GameApp()

if __name__ == "__main__":
    main()