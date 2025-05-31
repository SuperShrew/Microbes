from cell import *
from microbe import *
from colours import *
import time
import os

environment = [[Cell("blank", -1) for _ in range(0, 40)] for _ in range(0, 40)]

# testing stuff below \/
print(environment)

#test_struct = [
#	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)],
#	[Cell("blank", 1), Cell("mouth", 1), Cell("blank", 1)], 
#	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)]]

test_struct = {
	(1, 1): Cell("mouth", 1),
	(2, 2): Cell("producer", 1),
	#(1, 1): Cell("mouth", 1),
	(0, 0): Cell("producer", 1),
	#(2, 2): Cell("producer", 1)
}

fly_struct = {
	(0, 1): Cell("mouth", 2),
	(1, 0): Cell("mouth", 2),
	(2, 1): Cell("mouth", 2),
	(1, 2): Cell("mouth", 2),
	(1, 1): Cell("mover", 2)
}

test = Microbe(test_struct, 100, [4, 4], 1)
fly = Microbe(fly_struct, 150, [7, 7], 2)

#for i in test.structure:
#	for x in i:
#		print(x.icon, end=" ")
#	print()


print()
print(test.size)
print(test.max_age)
print(test.health)
for i in test.structure:
	environment[test.coords[1]+i[1]][test.coords[0]+i[0]] = test.structure[i]

def draw_env():
	global environment
	for i in range(0, len(environment)):
		for x in environment[i]:
			print(x.icon, end=" ")
		print()
# end testing stuff

# assigning variables
next_id = 3

microbes = [test, fly]

while True:
	for a, i in enumerate(microbes):
		i.tick(microbes, environment)
		#print("id:", i.id)
		#print("food:", i.food)
		#print("health:", i.health)
		#print("age:", i.age)
	for a, i in enumerate(microbes):
		new = i.attempt_mitosis(next_id, microbes, environment)
		if new:
			microbes = new
			next_id += 1
	draw_env()
	print("organism count:", len(microbes))
	time.sleep(0.1)
	for i in range(0, len(environment)): # iterate numerically through first layer of environment
		for x in range(0, len(environment[0])): # iterate numerically through each item in the layer of environment
			if environment[i][x].type == "food":
				pass
			else: 
				environment[i][x] = Cell("blank", -1)
	os.system("clear")
	for i in microbes:
		i.draw(environment)