from cell import Cell
import random


class Microbe:
	def __init__(self, size, structure, life_mult, coords, id):
		self.size = size # defines the hitbox of the cell
		self.structure = structure # 2D array of cells
		self.coords = coords # top left corner of hitbox
		self.cell_amount = 0
		self.id = id

		for i in self.structure:
			for x in i:
				if not(x.type == "blank"):
					self.cell_amount += 1
		
		self.max_age = self.cell_amount*life_mult
		self.health = self.cell_amount
		self.food = 0

	def tick(self):
		"""
		returns a dictionary of cells to update
		"""
		pass # still trying to figure out how i would update cells ourside the structure

	def draw(self, env):
		pass
