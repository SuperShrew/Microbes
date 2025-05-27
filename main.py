from cell import *
from microbe import *
from colours import *
import time
import os

environment = [[Cell("blank", -1)]*20]*20

# testing stuff below \/
print(environment)

test_struct = [
	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)],
	[Cell("blank", 1), Cell("mouth", 1), Cell("blank", 1)], 
	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)]]

test = Microbe(3, test_struct, 100, [4, 4], 1)


for i in test.structure:
	for x in i:
		print(x.icon, end=" ")
	print()



print()
print(test.size)
print(test.max_age)
print(test.health)

# end testing stuff

# assigning variables

microbes = [test]

while True:
	for i in microbes:
		i.tick()
	time.sleep(0.2)
	for i in range(0, len(environment)): # iterate numerically through first layer of environment
		for x in range(0, len(environment[0])): # iterate numerically through each item in the layer of environment
			if environment[i][x].type == "food":
				pass
			else: 
				environment[i][x] = Cell("blank", -1)