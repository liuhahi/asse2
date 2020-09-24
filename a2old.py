"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from a2_support import *

# Fill these in with your details
__author__ = "{{hongfei.shen}} ({{s4610279}})"
__email__ = "hongfei.shen@uqconnect.edu.au"
__date__ = "28.9.2020"
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
class Entity:
	def __init__(self):
		super().__init__()
		self._entity 

	def get_id(self):
		return self._entity

	def set_collide(self, collidable):
		True
	def can_collide(self) -> bool:
		collidable = True
		collidable = False
	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.entity()})"
	def __repr__(self) -> str:
		return str(self)


class Wall(Entity):
	def __init__(self,wall): pass
	def get_id(self) -> str: pass
	def set_collide(self, collidable: bool): pass
	def can_collide(self) -> bool: pass
	def __str__(self) -> str: pass
	def __repr__(self) -> str: pass


class Item(Entity):
	def __init__(self): pass
	def get_id(self) -> str: pass
	def set_collide(self, collidable: bool): pass
	def can_collide(self) -> bool: pass
	def on_hit(self, game: 'GameLogic'): pass
	def __str__(self) -> str: pass
	def __repr__(self) -> str: pass


class Key(Item):
	def __init__(self): pass
	def get_id(self) -> str: pass
	def set_collide(self, collidable: bool): pass
	def can_collide(self) -> bool: pass
	def on_hit(self, game: 'GameLogic'): pass
	def __str__(self) -> str: pass
	def __repr__(self) -> str: pass


class MoveIncrease(Item):
	def __init__(self, moves: int = 5): pass
	def get_id(self) -> str: pass
	def set_collide(self, collidable: bool): pass
	def can_collide(self) -> bool: pass
	def on_hit(self, game: 'GameLogic'): pass
	def __str__(self) -> str: pass
	def __repr__(self) -> str: pass


class Door(Entity):
	def __init__(self): pass
	def get_id(self) -> str: pass
	def set_collide(self, collidable: bool): pass
	def can_collide(self) -> bool: pass
	def __str__(self) -> str: pass
	def __repr__(self) -> str: pass





class GameApp:
	pass


	




def main():
	GameApp()

if __name__ == "__main__":
	main()
