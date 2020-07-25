#!/usr/bin/env python
#
#
#
#

#!/usr/bin/env python
#
# A* PATHFINDING ALGORITHM
#
#

import math
import time
import pygame
import Grid
from queue import PriorityQueue

def Djikstra(start, end, grid):

	queue = PriorityQueue()

	for pos in grid.grid:

		if grid.grid[pos].type not in ['wall', 'start_pos']:

			grid.grid[pos].f = math.inf

			grid.grid[pos].parent = None

	start_node = grid.grid[start]

	end_node = grid.grid[end]

	start_node.h = math.sqrt((end_node.position[0] - start_node.position[0])**2 + (end_node.position[1] - start_node.position[1])**2)

	start_node.f = 0

	queue.put(start_node)

	while not queue.empty():

		current_node = queue.get()

		current_node.list = False

		if current_node.type != 'start_pos':
			current_node.type = 'closed_node'

		time.sleep(0.01)

		directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, -1), (1, 1)]

		for x, y in directions:

			try:
				child_node = grid.grid[(current_node.position[0] + x, current_node.position[1] + y)]
			except:
				continue

			if child_node.type not in ['empty', 'end_pos']:
				continue

			alt = current_node.f + math.sqrt(abs(x) + abs(y))

			if alt < child_node.f:

				child_node.h = math.sqrt((end_node.position[0] - child_node.position[0])**2 + (end_node.position[1] - child_node.position[1])**2)
				child_node.f = alt
				child_node.parent = current_node

				if child_node == end_node:

					path = []

					child_node = child_node.parent

					while child_node.parent:
						path.append(child_node)
						child_node = child_node.parent

					for node in path[::-1]:
						node.type = 'final_path'
						time.sleep(0.05)

					grid.path = path[::-1]

					return

				child_node.type = "closed_node"
				queue.put(child_node)
				time.sleep(0.01)
	return
