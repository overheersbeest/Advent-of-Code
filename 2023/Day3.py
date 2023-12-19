import re

class GearData:
	def __init__(self, ratio, connections):
		self.ratio = ratio
		self.connections = connections
	ratio = 0
	connections = 0

with open('2023/Day3_input.txt', 'r') as f:
	input = f.readlines()
	input = [x.strip() + "." for x in input] # add trailing character so we always terminate at the end

	sum = 0
	gears = {}
	for row in range(len(input)):
		line = input[row]
		current_number = 0
		num_number_characters = 0 # not needed, but easier
		for column in range(len(line)):
			character = line[column]
			if character.isnumeric():
				current_number *= 10
				current_number += int(character)
				num_number_characters += 1
			else:
				if current_number != 0:
					is_part = False
					first_viable_column = max(0, column - num_number_characters - 1)
					last_viable_column = column
					first_viable_row = max(0, row - 1)
					last_viable_row = min(len(input) - 1, row + 1)
					for r in range(first_viable_row, last_viable_row + 1):
						for c in range(first_viable_column, last_viable_column + 1):
							check_character = input[r][c]
							if not check_character.isnumeric() and not check_character.isalpha() and check_character != ".":
								is_part = True
								if check_character == "*":
									pos_hash = r * len(input) + c
									found = gears.get(pos_hash)
									if found == None:
										gears[pos_hash] = GearData(current_number, 1)
									else:
										gears[pos_hash].ratio *= current_number
										gears[pos_hash].connections += 1
					if is_part:
						sum += current_number
				current_number = 0
				num_number_characters = 0
	print("Part 1: " + str(sum))
	gear_sum = 0
	for gear in gears:
		if gears[gear].connections == 2:
			gear_sum += gears[gear].ratio
	print("Part 2: " + str(gear_sum))
