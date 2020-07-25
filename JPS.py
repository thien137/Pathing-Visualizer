#!/usr/bin/env python
#
# A* PATHFINDING ALGORITHM WITH JUMP POINT SEARCH
#
#

import math
import time
import pygame
import threading
import sys
from queue import PriorityQueue

def JPS(start, end, grid):

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

			child_node.type = 'closed_node'

			if x != 0 and y != 0:
				for node in diagonal_search(x, y, child_node, end_node, grid):
					queue.put(node)

			if x != 0 and y == 0:
				for node in horizontal_search(x, child_node, end_node, grid):
					queue.put(node)

			if x == 0 and y != 0:
				for node in vertical_search(y, child_node, end_node, grid):
					queue.put(node)

def calculate_attributes(node, end_node, grid, parent, g):

	node.g = parent.g + g
	node.h = math.sqrt((node.position[0] - end_node.position[0])**2 + (node.position[1] - end_node.position[1])**2)
	node.f = node.g + node.h
	node.parent = parent
	node.list = False

def horizontal_search(horizontal_distance, current_node, end_node, grid, parent = None):

	x, y = current_node.position

	horizontal_nodes = []

	while True:

		if (x, y) not in grid.grid:
			break

		if grid.grid[(x, y)].type == "wall":
			break

		if grid.grid[(x, y)] == end_node:

			horizontal_nodes.append(grid.grid[(x, y)])

			calculate_attributes(grid.grid[(x, y)], end_node, grid, grid.grid[(x - horizontal_distance, y)], 1)

			path = []

			current_node = grid.grid[(x, y)].parent

			while current_node.parent:

				path.append(current_node)
				current_node = current_node.parent

			for node in path[::-1]:
				node.type = 'final_path'
				time.sleep(0.05)

			grid.path = path[::-1]

			sys.exit()

			break

		calculate_attributes(grid.grid[(x, y)], end_node, grid, grid.grid[(x - horizontal_distance, y)], 1)

		grid.grid[(x, y)].type = 'open_node'

		try:
			if grid.grid[(x, y + 1)].type == 'wall' and grid.grid[(x + horizontal_distance, y + 1)].type != 'wall':
				horizontal_nodes.append(grid.grid[(x + horizontal_distance, y + 1)])
				calculate_attributes(grid.grid[(x + horizontal_distance, y + 1)], end_node, grid, grid.grid[(x, y)], math.sqrt(2))
				grid.grid[(x + horizontal_distance, y + 1)].type = 'closed_node'
				time.sleep(0.05)
		except:
			pass

		try:
			if grid.grid[(x, y - 1)].type == 'wall' and grid.grid[(x + horizontal_distance, y - 1)].type != 'wall':
				horizontal_nodes.append(grid.grid[(x + horizontal_distance, y - 1)])
				calculate_attributes(grid.grid[(x + horizontal_distance, y - 1)], end_node, grid, grid.grid[(x, y)], math.sqrt(2))
				grid.grid[(x + horizontal_distance, y - 1)].type = 'closed_node'
				time.sleep(0.05)
		except:
			pass

		x += horizontal_distance

	return horizontal_nodes

def vertical_search(vertical_distance, current_node, end_node, grid, parent = None):

	x, y = current_node.position

	vertical_nodes = []

	while True:

		if (x, y) not in grid.grid:
			break

		if grid.grid[(x, y)].type == "wall":
			break

		if grid.grid[(x, y)] == end_node:

			vertical_nodes.append(grid.grid[(x, y)])

			calculate_attributes(grid.grid[(x, y)], end_node, grid, grid.grid[(x, y - vertical_distance)], 1)

			
			path = []

			current_node = grid.grid[(x, y)].parent

			while current_node.parent:

				path.append(current_node)
				current_node = current_node.parent

			for node in path[::-1]:
				node.type = 'final_path'
				time.sleep(0.05)

			grid.path = path[::-1]

			sys.exit()


			break

		calculate_attributes(grid.grid[(x, y)], end_node, grid, grid.grid[(x, y - vertical_distance)], 1)

		grid.grid[(x, y)].type = 'open_node'

		try:
			if grid.grid[(x + 1, y)].type == 'wall' and grid.grid[(x + 1, y + vertical_distance)].type != 'wall':
				vertical_nodes.append(grid.grid[(x + 1, y + vertical_distance)])
				calculate_attributes(grid.grid[(x + 1, y + vertical_distance)], end_node, grid, grid.grid[(x, y)], math.sqrt(2))
				grid.grid[(x + 1, y + vertical_distance)].type = 'closed_node'
				time.sleep(0.05)
		except:
			pass

		try:
			if grid.grid[(x - 1, y)].type == 'wall' and grid.grid[(x - 1, y + vertical_distance)].type != 'wall':
				vertical_nodes.append(grid.grid[(x - 1, y + vertical_distance)])
				calculate_attributes(grid.grid[(x - 1, y + vertical_distance)], end_node, grid, grid.grid[(x, y)], math.sqrt(2))
				grid.grid[(x - 1, y + vertical_distance)].type = 'closed_node'
				time.sleep(0.05)
		except:
			pass

		y += vertical_distance

	return vertical_nodes


def diagonal_search(horizontal_distance, vertical_distance, current_node, end_node, grid, parent = None):

	x, y = current_node.position

	diagonal_nodes = []

	while True:

		if (x, y) not in grid.grid:
			break

		if grid.grid[(x, y)].type == "wall":
			break

		if grid.grid[(x, y)] == end_node:

			diagonal_nodes.append(grid.grid[(x, y)])

			calculate_attributes(grid.grid[(x, y)], end_node, grid, grid.grid[(x - horizontal_distance, y - vertical_distance)], math.sqrt(2))

			
			path = []

			current_node = grid.grid[(x, y)].parent

			while current_node.parent:

				path.append(current_node)
				current_node = current_node.parent

			for node in path[::-1]:
				node.type = 'final_path'
				time.sleep(0.05)

			grid.path = path[::-1]

			sys.exit()


			break

		calculate_attributes(grid.grid[(x, y)], end_node, grid, grid.grid[(x - horizontal_distance, y - vertical_distance)], math.sqrt(2))

		grid.grid[(x, y)].type = 'open_node'


		try:
			if grid.grid[(x - horizontal_distance, y)].type == 'wall' and grid.grid[(x - horizontal_distance, y + vertical_distance)].type != 'wall':
				diagonal_nodes.append(grid.grid[(x - horizontal_distance, y + vertical_distance)])
				calculate_attributes(grid.grid[(x - horizontal_distance, y + vertical_distance)], end_node, grid, grid.grid[(x, y)], math.sqrt(2))
				grid.grid[(x - horizontal_distance, y + vertical_distance)].type = 'closed_node'	
				time.sleep(0.05)			
		except:
			pass

		try:
			if grid.grid[(x + horizontal_distance, y)].type == 'wall' and grid.grid[(x + horizontal_distance, y + vertical_distance)].type != 'wall':
				diagonal_nodes.append(grid.grid[(x + horizontal_distance, y + vertical_distance)])
				calculate_attributes(grid.grid[(x + horizontal_distance, y + vertical_distance)], end_node, grid, grid.grid[(x, y)], math.sqrt(2))
				grid.grid[(x + horizontal_distance, y + vertical_distance)].type = 'closed_node'
				time.sleep(0.05)	
		except:
			pass

		if (x + horizontal_distance, y) in grid.grid:
			diagonal_nodes += horizontal_search(horizontal_distance, grid.grid[(x + horizontal_distance, y)], end_node, grid)

		if (x, y + vertical_distance) in grid.grid:
			diagonal_nodes += vertical_search(vertical_distance, grid.grid[(x, y + vertical_distance)], end_node, grid)


		x += horizontal_distance
		y += vertical_distance

	return diagonal_nodes








