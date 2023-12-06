import re

class Cubes:
	def __init__(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue
		
	red = 0
	green = 0
	blue = 0

def GetCubes(line):
	regex_matches = re.search(r'Game (\d+): (.*)$', line)
	id = int(regex_matches.groups()[0])
	games = str.split(regex_matches.groups()[1], ';')
	cube_results = []
	
	def GetAmount(colour, game):
		amount = 0
		match = re.search(r'(\d+) ' + colour, game)
		if match != None:
			amount = int(match.groups()[0])
		return amount

	for game in games:
		red = GetAmount('red', game)
		green = GetAmount('green', game)
		blue = GetAmount('blue', game)
		cube_results.append(Cubes(red, green, blue))

	return [id, cube_results]

with open('2023/Day2_input.txt', 'r') as f:
	input = f.readlines()

	max_red = 12
	max_green = 13
	max_blue = 14
	id_sum = 0
	power_sum = 0
	for line in input:
		[id, cube_results] = GetCubes(line)
		possible = True
		seen_red = 0
		seen_green = 0
		seen_blue = 0
		for cubes in cube_results:
			seen_red = max(seen_red, cubes.red)
			seen_green = max(seen_green, cubes.green)
			seen_blue = max(seen_blue, cubes.blue)
			if cubes.red > max_red or cubes.green > max_green or cubes.blue > max_blue:
				possible = False
		if possible:
			id_sum += id
		power_sum += seen_red * seen_green * seen_blue
	print("Part 1: " + str(id_sum))
	print("Part 2: " + str(power_sum))
