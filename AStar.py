#!/usr/bin/env Python
#
# Python
#
#

import math
from queue import PriorityQueue

def AStar(start, end, grid):

	start_node = grid.grid[start]
	end_node = grid.grid[end]

	queue = PriorityQueue()

	queue.put((start_node.f, start_node))

	path = []

	while not queue.empty():

		current_node = queue.get()[1]

		grid.grid[current_node.position].list = False

		directions = [(0, grid.interval), (0, -grid.interval), (grid.interval, 0), (-grid.interval, 0), (-grid.interval, -grid.interval), (-grid.interval, grid.interval), (grid.interval, -grid.interval), (grid.interval, grid.interval)]

		for x, y in directions:

			try:
				child = grid.grid[(current_node.position[0] + x, current_node.position[1] + y)]
			except:
				continue

			if child.list == False:
				continue

			if child.type == 1:
				continue

			g = 1

			if x != 0 and y != 0:
				g = math.sqrt(2)

			child.g = current_node.g + g
			child.h = math.sqrt((end_node.position[0] - child.position[0]) ** 2 + (end_node.position[1] - child.position[1]) ** 2)
			child.f = child.g + child.h
			child.parent = current_node
			child.list = False
			queue.put((child.f, child))
			path.append(child.position)

			if child == end_node:
				final_path = []
				while child.parent:
					final_path.append(child.position)
					child = child.parent
				return path, final_path

	return False, False

if __name__ == "__main__":
	grid = Grid(800, 800)
	start = (300, 550)
	end = (750, 350)
	print(AStar(start, end, grid))


