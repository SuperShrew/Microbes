from cell import Cell
import random


class Microbe:
	def __init__(self, structure, life_mult, coords, id):
		self.e = 40
		self.size = 0 # defines the hitbox of the  (not currently needed)
		self.structure = structure # dictionary of cells and their coords relative to the top left corner
		self.coords = coords # top left corner of hitbox
		self.cell_amount = len(structure)
		self.id = id
		self.max_age = self.cell_amount*life_mult
		self.age = 0
		self.life_mult = life_mult
		self.health = self.cell_amount
		self.food = 0
		self.food_counter = 50
		self.mover = False
		self.br_coords = [0, 0]
		self.calc_br()
		for i in self.structure:
			if structure[i].type == "mover":
				self.mover = True
				break

	def calc_br(self):
		xs = [p[0] for p in self.structure]
		ys = [p[1] for p in self.structure]

		max_x = max(xs)
		max_y = max(ys)

		self.br_coords = [self.coords[0] + max_x, self.coords[1] + max_y]
		self.size = max(max_x, max_y)

	def tick(self, microbes, env):
		# TODO: clean this mess up and replace try excepts with actual bound checkers
		self.age += 1

		if self.food_counter > 0:
			self.food_counter -= 1
		elif self.food_counter == 0 and self.food > 0:
			self.food -= 1
			self.food_counter = 50
		elif self.food_counter == 0 and self.food == 0:
			self.health -= 0.1

		if self.health <= 0 or self.age >= self.max_age:
			for i, m in enumerate(microbes):
				if m.id == self.id:
					for x in self.structure:
						env[self.coords[1] + x[1]][self.coords[0] + x[0]] = Cell("food", -1)
					del microbes[i]
					break
			return env

		if self.mover: # IMPORTANT: ADD COLLISIONS ASAP
			direction = random.randint(1, 2)
			if direction == 1:
				self.coords[0] += random.randint(-1, 1)
			if direction == 2:
				self.coords[1] += random.randint(-1, 1)
			if self.coords[0] < 0:
				self.coords[0] = -self.coords[0]
			if self.coords[1] < 0:
				self.coords[1] = -self.coords[1]
			self.calc_br()
			while self.br_coords[0] >= self.e-1 or self.br_coords[1] >= self.e-1 or self.coords[0] >= self.e-1 or self.coords[1] >= self.e-1:
				if self.br_coords[0] >= self.e-1 or self.coords[0] >= self.e-1:
					self.coords[0] -= 1
				if self.br_coords[1] >= self.e-1 or self.coords[1] >= self.e-1:
					self.coords[1] -= 1
				self.calc_br()
		else:
			for i in self.structure:
				if self.structure[i].type == "producer":
					if random.randint(1, 100) >= 95:
						side = random.randint(1, 4)
						if side == 1:
							try:
								if env[self.coords[1] + i[1]+1][self.coords[0] + i[0]].type == "blank":
									env[self.coords[1] + i[1]+1][self.coords[0] + i[0]] = Cell("food", -1)
							except:
								pass
						elif side == 2:
							try:
								if env[self.coords[1] + i[1]][self.coords[0] + i[0]+1].type == "blank":
									env[self.coords[1] + i[1]][self.coords[0] + i[0]+1] = Cell("food", -1)
							except:
								pass
						elif side == 3:
							try:
								if env[self.coords[1] + i[1]-1][self.coords[0] + i[0]].type == "blank":
									env[self.coords[1] + i[1]-1][self.coords[0] + i[0]] = Cell("food", -1)
							except:
								pass
						elif side == 4:
							try:
								if env[self.coords[1] + i[1]][self.coords[0] + i[0]-1].type == "blank":
									env[self.coords[1] + i[1]][self.coords[0] + i[0]-1] = Cell("food", -1)
							except:
								pass
		for i in self.structure:
			if self.structure[i].type == "mouth":
				try:
					if env[self.coords[1] + i[1]+1][self.coords[0] + i[0]].type == "food":
						env[self.coords[1] + i[1]+1][self.coords[0] + i[0]] = Cell("blank", -1)
						self.food += 1
				except:
					pass
				try:
					if env[self.coords[1] + i[1]][self.coords[0] + i[0]+1].type == "food":
						env[self.coords[1] + i[1]][self.coords[0] + i[0]+1] = Cell("blank", -1)
						self.food += 1
				except:
					pass
				try:
					if env[self.coords[1] + i[1]-1][self.coords[0] + i[0]].type == "food":
						env[self.coords[1] + i[1]-1][self.coords[0] + i[0]] = Cell("blank", -1)
						self.food += 1
				except:
					pass
				try:
					if env[self.coords[1] + i[1]][self.coords[0] + i[0]-1].type == "food":
						env[self.coords[1] + i[1]][self.coords[0] + i[0]-1] = Cell("blank", -1)
						self.food += 1
				except:
					pass

		# TODO: program killer
		return env

	def attempt_mitosis(self, next_id, microbes, env):

		if self.food < self.cell_amount*2:
			return False

		d = random.randint(1, 4)

		if d == 1:
			tempcoords = [self.coords[0] + 2 + self.size, self.coords[1]]
		if d == 2:
			tempcoords = [self.coords[0], self.coords[1] + 2 + self.size]
		if d == 3:
			tempcoords = [self.coords[0] - 2 - self.size, self.coords[1]]
		if d == 4:
			tempcoords = [self.coords[0], self.coords[1] - 2 - self.size]

		#for i in self.structure:
		#	if env[i[]]

		if self.coords[0] + 2 + self.size < self.e-1:
			if d == 1:
				microbes.append(Microbe(self.structure, self.life_mult, [self.coords[0] + 2 + self.size, self.coords[1]], next_id))
		if self.coords[1] + 2 + self.size < self.e-1:
			if d == 2:
				microbes.append(Microbe(self.structure, self.life_mult, [self.coords[0], self.coords[1] + 2 + self.size], next_id))
		if self.coords[0] - 2 - self.size < self.e-1:
			if d == 3:
				microbes.append(Microbe(self.structure, self.life_mult, [self.coords[0] - 2 - self.size, self.coords[1]], next_id))
		if self.coords[1] - 2 - self.size < self.e-1:
			if d == 4:
				microbes.append(Microbe(self.structure, self.life_mult, [self.coords[0], self.coords[1] - 2 - self.size], next_id))
		self.food -= self.cell_amount*2
		return microbes

	def draw(self, env):
		for i in self.structure:
			env[self.coords[1]+i[1]][self.coords[0]+i[0]] = self.structure[i]
		return env
