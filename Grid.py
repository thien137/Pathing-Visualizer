#!/usr/bin/env python
#
# Grid
#
#

import pygame

class Node:

	def __init__(self, position, parent):

		self.g = 0
		self.h = 0
		self.f = 0
		self.position = position
		self.parent = parent
		self.type = 'empty'
		self.list = None

	def generate_color(self, start_distance):

		if self.h >= start_distance:
			red = 255 - (self.h/start_distance - 1) * 255
			green = 0

		else:
			red = 255 * (self.h/start_distance)
			green = 255 * (1 - self.h/start_distance)

		return (red, green, 0)

	def __eq__(self, other):
		return self.position == other.position

	def __lt__(self, other):
		return self.f <  other.f

class Grid:

	def __init__(self, width, height):

		self.width = width - 200
		self.height = height
		self.interval = 20
		self.starting_position = None
		self.ending_position = None
		self.wall_edit = None
		self.path = None
		self.grid = {(i, j) : Node((i, j), None) for i in range(0, self.width//self.interval) for j in range(0, self.height//self.interval)}
		self.colors = {'empty' : (255, 255, 255),'start_pos' : (0, 255, 255), 'end_pos' : (255, 0, 255), 'wall' : (0, 0, 0), 'open_node' : (150, 150, 150), 'closed_node' : (255, 0, 0), 'final_path' : (150, 250, 177)}

	def draw(self, surface):

		for node in self.grid.values():

			if node.type != 'closed_node':
				color = self.colors[node.type]
			else:
				color = node.generate_color(self.grid[self.starting_position].h)

			pygame.draw.rect(surface, color, (node.position[0] * self.interval, node.position[1] * self.interval, self.interval, self.interval))

		for i in range(0, self.width//self.interval + 1):

			pygame.draw.line(surface, (0, 0, 0), (i * self.interval, 0), (i * self.interval, self.height))

		for j in range(0, self.height//self.interval + 1):

			pygame.draw.line(surface, (0, 0, 0), (0, j * self.interval), (self.width, j * self.interval))

	def reset(self):

		self.starting_position = None
		self.ending_position = None
		self.wall_edit = None
		self.path = None
		self.grid = {(i, j) : Node((i, j), None) for i in range(0, self.width//self.interval) for j in range(0, self.height//self.interval)}

	def soft_reset(self):

		self.wall_edit = None
		self.path = None

		for pos in self.grid:
			self.grid[pos].g = 0
			self.grid[pos].h = 0
			self.grid[pos].f = 0
			self.grid[pos].list = None
			if self.grid[pos].type in ['open_node', 'closed_node', 'final_path']:
				self.grid[pos].type = 'empty'

