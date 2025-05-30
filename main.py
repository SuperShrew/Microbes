from cell import *
from microbe import *
from colours import *
import time
import os

environment = [[Cell("blank", -1) for _ in range(0, 20)] for _ in range(0, 20)]

# testing stuff below \/
print(environment)

#test_struct = [
#	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)],
#	[Cell("blank", 1), Cell("mouth", 1), Cell("blank", 1)], 
#	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)]]

test_struct = {
	(0, 0): Cell("producer", 1),
	(0, 2): Cell("producer", 1),
	(1, 1): Cell("mouth", 1),
	(2, 0): Cell("producer", 1),
	(2, 2): Cell("producer", 1)
}

test = Microbe(test_struct, 100, [4, 4], 1)


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

microbes = [test]

while True:
	for i in microbes:
		environment = i.tick(microbes, environment)
		print("food:", i.food)
		print("health:", i.health)
	draw_env()
	time.sleep(0.2)
	for i in range(0, len(environment)): # iterate numerically through first layer of environment
		for x in range(0, len(environment[0])): # iterate numerically through each item in the layer of environment
			if environment[i][x].type == "food":
				pass
			else: 
				environment[i][x] = Cell("blank", -1)
	os.system("clear")
	for i in microbes:
		i.draw(environment)