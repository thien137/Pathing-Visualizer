#!/usr/bin/env Python
#
# Python
#
#

import math
from queue import PriorityQueue

#class Node:

#	def __init__(self, position, parent):
#		self.g = 0
#		self.h = 0
#		self.f = 0
#		self.list = None
#		self.position = position
#		self.parent = parent
#		self.type = 0

#	def __eq__(self, other):
#		return self.position == other.position

#	def __lt__(self, other):
#		return self.f < other.f

#class Grid:

#	def __init__(self, x, y):
#		self.width = x#surface.get_width()
#		self.length = y#surface.get_height()
#		self.grid = {(i, j) : Node((i, j), None) for i in range(0, self.width, 50) for j in range(0, self.length, 50)}

def AStar(start, end, grid):

	start_node = grid.grid[start]
	end_node = grid.grid[end]

	queue = PriorityQueue()

	queue.put((start_node.f, start_node))

	path = []

	while queue:

		current_node = queue.get()[1]

		grid.grid[current_node.position].list = False

		directions = [(0, 50), (0, -50), (50, 0), (-50, 0), (-50, -50), (-50, 50), (50, -50), (50, 50)]

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
		#	path = []
		#	while current_node.parent:
		#		path.append(current_node.position)
		#		current_node = current_node.parent
				return path

if __name__ == "__main__":
	grid = Grid(800, 800)
	start = (300, 550)
	end = (750, 350)
	print(AStar(start, end, grid))


