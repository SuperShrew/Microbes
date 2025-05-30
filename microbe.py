from cell import Cell
import random


class Microbe:
	def __init__(self, structure, life_mult, coords, id, size=0):
		self.size = size # defines the hitbox of the  (not currently needed)
		self.structure = structure # dictionary of cells and their coords relative to the top left corner
		self.coords = coords # top left corner of hitbox
		self.cell_amount = len(structure)
		self.id = id
		self.max_age = self.cell_amount*life_mult
		self.health = self.cell_amount
		self.food = 0
		self.food_counter = 50
		self.mover = False

		for i in self.structure:
			if structure[i].type == "mover":
				self.mover = True
				break

	def tick(self, microbes, env):
		if self.food_counter > 0:
			self.food_counter -= 1
		elif self.food_counter == 0 and self.food > 0:
			self.food -= 1
			self.food_counter = 50
		elif self.food_counter == 0 and self.food == 0:
			self.health -= 0.1

		if self.health <= 0:
			for i in range(0, len(microbes)):
				if microbes[i].id == self.id:
					microbes.pop(i)

		if self.mover: # IMPORTANT: ADD COLLISIONS ASAP
			direction = random.randint(1, 2)
			if direction == 1:
				self.coords[0] += random.randint(-1, 1)
			if direction == 2:
				self.coords[1] += random.randint(-1, 1)
		else:
			for i in self.structure:
				if self.structure[i].type == "producer":
					if random.randint(1, 100) >= 75:
						side = random.randint(1, 4)
						if side == 1:
							if env[self.coords[1] + i[1]+1][self.coords[0] + i[0]].type == "blank":
								env[self.coords[1] + i[1]+1][self.coords[0] + i[0]] = Cell("food", -1)
						elif side == 2:
							if env[self.coords[1] + i[1]][self.coords[0] + i[0]+1].type == "blank":
								env[self.coords[1] + i[1]][self.coords[0] + i[0]+1] = Cell("food", -1)
						elif side == 3:
							if env[self.coords[1] + i[1]-1][self.coords[0] + i[0]].type == "blank":
								env[self.coords[1] + i[1]-1][self.coords[0] + i[0]] = Cell("food", -1)
						elif side == 4:
							if env[self.coords[1] + i[1]][self.coords[0] + i[0]-1].type == "blank":
								env[self.coords[1] + i[1]][self.coords[0] + i[0]-1] = Cell("food", -1)
		for i in self.structure:
			if self.structure[i].type == "mouth":
				if env[self.coords[1] + i[1]+1][self.coords[0] + i[0]].type == "food":
					env[self.coords[1] + i[1]+1][self.coords[0] + i[0]] = Cell("blank", -1)
					self.food += 1
				if env[self.coords[1] + i[1]][self.coords[0] + i[0]+1].type == "food":
					env[self.coords[1] + i[1]][self.coords[0] + i[0]+1] = Cell("blank", -1)
					self.food += 1
				if env[self.coords[1] + i[1]-1][self.coords[0] + i[0]].type == "food":
					env[self.coords[1] + i[1]-1][self.coords[0] + i[0]] = Cell("blank", -1)
					self.food += 1
				if env[self.coords[1] + i[1]][self.coords[0] + i[0]-1].type == "food":
					env[self.coords[1] + i[1]][self.coords[0] + i[0]-1] = Cell("blank", -1)
					self.food += 1

		# TODO: program killer
		return env

	def draw(self, env):
		for i in self.structure:
			env[self.coords[1]+i[1]][self.coords[0]+i[0]] = self.structure[i]
		return env
