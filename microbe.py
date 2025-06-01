from cell import Cell
import random
import time


class Microbe:
	def __init__(self, structure, life_mult, coords, id, mutation_rate=10):
		self.e = 130
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
		self.mutation_rate = mutation_rate
		for i in self.structure:
			if self.structure[i].type == "mover":
				self.mover = True
				break

	def mutate(self, next_id):
		new_struct = {}
		for i in self.structure:
			new_struct[i] = self.structure[i]
			new_struct[i].id = next_id

		mutation_type = random.choice(['remove', 'change', 'add'])

		# Must have at least 2 cells to remove
		if mutation_type == 'remove' and len(new_struct) > 1:
			key = random.choice(list(new_struct.keys()))
			del new_struct[key]

		elif mutation_type == 'change':
			key = random.choice(list(new_struct.keys()))
			cell = new_struct[key]
			options = ["mouth", "producer", "mover", "armour", "killer"]
			options.remove(cell.type)
			new_type = random.choice(options)
			new_struct[key] = Cell(new_type, self.id)
		elif mutation_type == 'add':
			# Pick a random existing cell
			existing_keys = list(new_struct.keys())
			base_x, base_y = random.choice(existing_keys)

			# Try to place a new cell adjacent to it
			directions = [(1,0), (-1,0), (0,1), (0,-1)]
			random.shuffle(directions)
			for dx, dy in directions:
				new_pos = (base_x + dx, base_y + dy)
				if new_pos not in new_struct:
					new_type = random.choice(["mouth", "producer", "mover", "armour", "killer"])
					new_struct[new_pos] = Cell(new_type, self.id)
					break  # only add one cell
		return new_struct

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

		if self.mover:
			dx = random.randint(-1, 1)
			dy = random.randint(-1, 1)

			# Proposed new coordinates
			new_coords = [self.coords[0] + dx, self.coords[1] + dy]

			# Clamp to grid bounds
			new_coords[0] = max(0, min(new_coords[0], self.e - 1))
			new_coords[1] = max(0, min(new_coords[1], self.e - 1))

			# Calculate bottom-right bounds of the structure at new location
			xs = [p[0] for p in self.structure]
			ys = [p[1] for p in self.structure]
			br_x = new_coords[0] + max(xs)
			br_y = new_coords[1] + max(ys)

			current_positions = set(self.occupied_positions())

			# Check if it fits in the environment bounds
			if br_x >= self.e or br_y >= self.e:
				return  # Reject move

			# Collision detection: check if any cell in the new location is occupied
			collision = False
			for rel in self.structure:
				x = new_coords[0] + rel[0]
				y = new_coords[1] + rel[1]
				if not (0 <= x < self.e and 0 <= y < self.e):
					collision = True
					break
				cell_type = env[y][x].type
				if cell_type not in ("blank", "food")  and (x, y) not in current_positions:
					collision = True
					break


			if not collision:
				self.coords = new_coords
				self.calc_br()

		else:
			for i in self.structure:
				if self.structure[i].type == "producer":
					if random.randint(1, 100) >= 95:
						side = random.randint(1, 4)
						x = self.coords[0] + i[0]
						y = self.coords[1] + i[1]

						# down
						if side == 1:
							if 0 <= y + 1 < self.e and 0 <= x < self.e:
								if env[y + 1][x].type == "blank":
									env[y + 1][x] = Cell("food", -1)

						# right
						elif side == 2:
							if 0 <= y < self.e and 0 <= x + 1 < self.e:
								if env[y][x + 1].type == "blank":
									env[y][x + 1] = Cell("food", -1)

						# up
						elif side == 3:
							if 0 <= y - 1 < self.e and 0 <= x < self.e:
								if env[y - 1][x].type == "blank":
									env[y - 1][x] = Cell("food", -1)

						# left
						elif side == 4:
							if 0 <= y < self.e and 0 <= x - 1 < self.e:
								if env[y][x - 1].type == "blank":
									env[y][x - 1] = Cell("food", -1)
		directions = [(0,1), (1,0), (0,-1), (-1,0)]
		for i in self.structure:
			if self.structure[i].type == "mouth":
				x = self.coords[0] + i[0]
				y = self.coords[1] + i[1]
				for dx, dy in directions:
					nx, ny = x + dx, y + dy
					if 0 <= nx < self.e and 0 <= ny < self.e and env[ny][nx].type == "food":
						env[ny][nx] = Cell("blank", -1)
						self.food += 1

		# TODO: program killer
		return env

	def attempt_mitosis(self, next_id, microbes, env):
		if self.food < self.cell_amount*2:
			return False
		if random.randint(1, 100) <= self.mutation_rate:
			new_struct = self.mutate(next_id)
		else:
			new_struct = {}
			for i in self.structure:
				new_struct[i] = self.structure[i]
				new_struct[i].id = next_id
			
		#print(new_struct)
		#input()
		d = random.randint(1, 4)

		if d == 1:
			tempcoords = [self.coords[0] + 2 + self.size, self.coords[1]]
		if d == 2:
			tempcoords = [self.coords[0], self.coords[1] + 2 + self.size]
		if d == 3:
			tempcoords = [self.coords[0] - 2 - self.size, self.coords[1]]
		if d == 4:
			tempcoords = [self.coords[0], self.coords[1] - 2 - self.size]
		try:
			for i in new_struct:
				if not(env[i[1] + tempcoords[1]][i[0] + tempcoords[0]].type == "blank"):# or env[i[1] + tempcoords[1]][i[0] + tempcoords[0]].type == "food"):
					return False
		except IndexError:
			return False

		if self.coords[0] + 2 + self.size < self.e-1 and self.coords[0] + 2 + self.size >= 0:
			if d == 1:
				microbes.append(Microbe(new_struct, self.life_mult, [self.coords[0] + 2 + self.size, self.coords[1]], next_id))
		if self.coords[1] + 2 + self.size < self.e-1 and self.coords[1] + 2 + self.size >= 0:
			if d == 2:
				microbes.append(Microbe(new_struct, self.life_mult, [self.coords[0], self.coords[1] + 2 + self.size], next_id))
		if self.coords[0] - 2 - self.size < self.e-1 and self.coords[0] - 2 - self.size >= 0:
			if d == 3:
				microbes.append(Microbe(new_struct, self.life_mult, [self.coords[0] - 2 - self.size, self.coords[1]], next_id))
		if self.coords[1] - 2 - self.size < self.e-1 and self.coords[1] - 2 - self.size >= 0:
			if d == 4:
				microbes.append(Microbe(new_struct, self.life_mult, [self.coords[0], self.coords[1] - 2 - self.size], next_id))
		self.food -= self.cell_amount*2
		return microbes

	def draw(self, env):
		for i in self.structure:
			env[self.coords[1]+i[1]][self.coords[0]+i[0]] = self.structure[i]
		return env
	def occupied_positions(self):
		return [(self.coords[0] + p[0], self.coords[1] + p[1]) for p in self.structure]
