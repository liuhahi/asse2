class Entity(object):
	def __init__(self):
		super().__init__()
		self._entity = entity
		entity = Entity()

	def get_id(self):
		return self._entity

	def set_collide(self, collidable):
		True
	def can_collide(self) -> bool:
		collide = True
		collide =	False
	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.entity()})"
	def __repr__(self) -> str:
		return str(self)
