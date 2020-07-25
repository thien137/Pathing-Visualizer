#!/usr/bin/env python
#
# A* PATHFINDING ALGORITHM
#
#

import math
import time
import pygame
from queue import PriorityQueue

def AStar(start, end, grid):

	start_node = grid.grid[start]
	end_node = grid.grid[end]

	queue = PriorityQueue()

	queue.put(start_node)

	start_node.list = True
	start_node.g = 0
	start_node.h = math.sqrt((end_node.position[0] - start_node.position[0])**2 + (end_node.position[1] - start_node.position[1])**2)
	start_node.f = start_node.g + start_node.h

	while not queue.empty():

		current_node = queue.get()

		current_node.list = False

		if grid.grid[current_node.position].type != 'start_pos':
			grid.grid[current_node.position].type = "closed_node"

		directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

		for x, y in directions:

			try:
				child_node = grid.grid[(current_node.position[0] + x, current_node.position[1] + y)]
			except:
				continue

			if child_node.type == "wall":
				continue

			if child_node.list == False:

				continue

			g = 1

			if x != 0 and y != 0:
				g = math.sqrt(2)

			if child_node.list == True:
				if child_node.f <= child_node.h + current_node.g + g:
					continue

			child_node.g = current_node.g + g
			child_node.h = math.sqrt((end_node.position[0] - child_node.position[0])**2 + (end_node.position[1] - child_node.position[1])**2)
			child_node.f = child_node.g + child_node.h
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
				
				return None

			child_node.list = True
			queue.put(child_node)
			grid.grid[(child_node.position)].type = "open_node"
			time.sleep(0.01)

