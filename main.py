from cell import *
from microbe import *
from colours import *

test_struct = [
	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)],
	[Cell("blank", 1), Cell("mouth", 1), Cell("blank", 1)], 
	[Cell("producer", 1), Cell("blank", 1), Cell("producer", 1)]]

test = Microbe(3, test_struct, 100, [4, 4])

for i in test.structure:
	for x in i:
		print(x.icon, end=" ")
	print()
print()
print(test.size)
print(test.max_age)
print(test.health)