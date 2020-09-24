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
                entity = None
                if self._dungeon[i][j] == KEY:
                    entity = Key()
                    dungeon[(i,j)] = entity
        for i in range(self._dungeon_size):            
            for j in range(self._dungeon_size):
                entity = None                        
                if self._dungeon[i][j] == DOOR:
                    entity = Door()    
                    dungeon[(i,j)] = entity                  
        for i in range(self._dungeon_size):            
            for j in range(self._dungeon_size):
                entity = None                    
                if self._dungeon[i][j] == WALL:
                    entity = Wall() 
                    dungeon[(i,j)] = entity 
        for i in range(self._dungeon_size):            
            for j in range(self._dungeon_size):
                entity = None                    
                if self._dungeon[i][j] == MOVE_INCREASE:
                    entity = MoveIncrease() 
                    dungeon[(i,j)] = entity
                if self._dungeon[i][j] == PLAYER:
                    self._player.set_position((i,j))
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
        current = self._player.get_position()
        position = (current[0] + DIRECTIONS[direction][0], current[1] + DIRECTIONS[direction][1])
        if position[0] > self._dungeon_size or position[1] > self._dungeon_size or position[0] < 0 or position[1] < 0:
            return None
        elif position not in self._game_information.keys():
            return None
        else:
            return self._game_information[position]
    def collision_check(self, direction):
        current = self._player.get_position()
        position = (current[0] + DIRECTIONS[direction][0], current[1] + DIRECTIONS[direction][1])
        if position[0] > self._dungeon_size or position[1] > self._dungeon_size or position[0] < 0 or position[1] < 0:
            return False
        elif position in self._game_information and self._game_information[position].can_collide() == False:
            return True
        else:
            return False
    def new_position(self, direction):
        return (self._player.get_position()[0] + DIRECTIONS[direction][0], self._player.get_position()[1] + DIRECTIONS[direction][1])
        
    def move_player(self, direction):
        self._player.set_position(self.new_position(direction))
        
    def check_game_over(self):
        return self._player.moves_remaining() <= 0 or self.won()
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
        self.id = WALL
        self.collidable = False         	

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
        player = game.get_player()
        player.add_item(self)
        game_info = game.get_game_information() 
        for item in game.get_positions(KEY):
            game_info.pop(item)

class MoveIncrease(Item):
    ''' key class'''
    def __init__(self, move_count=5):
        super().__init__()
        self.id = MOVE_INCREASE
        self.move_count = move_count
    def on_hit(self, game):
        player = game.get_player()
        player.change_move_count(self.move_count)
        game_info = game.get_game_information() 
        for item in game.get_positions(MOVE_INCREASE):            
            game_info.pop(item)                	      

class Door(Entity):
    ''' key class'''
    def __init__(self):
        super().__init__()
        self.id = DOOR
    def on_hit(self, game):
        player = game.get_player()
        for item in player.get_inventory():
            if str(item) == str(Key()):
                game.set_win(True)
                return
        print("You don't have the key!")

class Player(Entity):
    def __init__(self, move_count):
        super().__init__()
        self.move_count = move_count
        self.id = PLAYER
        self.position = None
        self.inventory = []

    def set_position(self, position):
        self.position = position
    def get_position(self):        
        return self.position
    def change_move_count(self, number):
        self.move_count += number
    def moves_remaining(self):
        return self.move_count
    def add_item(self, item):
        self.inventory.append(item)        
    def get_inventory(self):
        return self.inventory

def prompt(action):
    """(str) Prompts the user for input and return a response"""
    return input(action)

class GameApp:
    ''' key class'''
    def __init__(self):      
        self.game = GameLogic()
        self.game_info = self.game.get_game_information()
        self.player = self.game.get_player()
        # self.play()

    def draw(self):
        display = Display(self.game_info, self.game._dungeon_size)        
        player_pos = self.player.get_position()
        moves = self.player.moves_remaining()
        display.display_game(player_pos)
        display.display_moves(moves)

    def play(self):
        q_flag = False
        while self.game.check_game_over() == False:
            self.draw()
            action = prompt("Please input an action: ")            
            if action in VALID_ACTIONS:
                if action == HELP:
                    print(HELP_MESSAGE)
                elif action == QUIT:
                    action = prompt('Are you sure you want to quit? (y/n): ')
                    if action == 'y':
                        q_flag = True
                        break         
                elif action == INVESTIGATE:
                    continue           
                else:
                    self.player.change_move_count(-1)
                    if self.game.collision_check(action):
                        print(INVALID)
                    else:                                               
                        new_position = self.game.new_position(action)
                        entity = self.game.get_entity(new_position)
                        if entity:
                            entity.on_hit(self.game)                        
                        self.game.move_player(action) 
                            
            elif len(action.split()) == 2:
                first = action.split()[0]
                second = action.split()[1]
                if first == INVESTIGATE:                    
                    if second in VALID_ACTIONS:
                        self.player.change_move_count(-1)
                        check_position = (self.player.get_position()[0] + DIRECTIONS[second][0], self.player.get_position()[1] + DIRECTIONS[second][1])
                        entity = self.game.get_entity(check_position)
                        print('{} is on the {} side.'.format(entity, second))  
                    else:
                        print(INVALID)             
            else:
                print(INVALID)
        if q_flag:
            return

        if self.game.won():
            print(WIN_TEXT)
        else:
            print(LOSE_TEST)
    pass


def main():
    GameApp()

if __name__ == "__main__":
    main()