#!/usr/bin/env python
#
# GUI Interface
#
#

import pygame
import math
import threading
from AStar import AStar

# Initialize

pygame.init()

# Window

window = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Pathing Visualizer')

def update_window(surface, grid):

	surface.fill((255, 255, 255))

	grid.draw(surface)

def check_inputs(surface, grid):

	global Start 
	global End
	global Path
	global Max
	global Down

	mouse = pygame.mouse.get_pressed()
	keys = pygame.key.get_pressed()

	if mouse[0]:
		x, y = pygame.mouse.get_pos()
		x = int(50 * (x//50))
		y = int(50 * (y//50))
		if Start == False:
			grid.grid[(x, y)].type = 2
			Start = (x, y)
		if End == False and grid.grid[(x, y)].type != 2:
			grid.grid[(x, y)].type = 3
			End = (x, y)
			Max = math.sqrt((Start[0] - End[0]) ** 2 + (Start[1] - End[1]) ** 2)

		if not Path and grid.grid[(x, y)].type == 0:
			grid.grid[(x, y)].type = 1
		elif not Path and grid.grid[(x, y)].type == 1:
			grid.grid[(x, y)].type = 0		

	if keys[pygame.K_SPACE] and Start and End and not Path:
		Path = AStar(Start, End, grid)[:-1]

	if keys[pygame.K_r] and Start and End:

		grid.grid = {(i, j) : Node((i, j), None) for i in range(0, grid.width, 50) for j in range(0, grid.length, 50)}
		Start = False
		End = False
		Path = False

# Grid

class Node:

	def __init__(self, position, parent):
		self.g = 0
		self.h = 0
		self.f = 0
		self.list = None
		self.position = position
		self.parent = parent
		self.type = 0

	def __eq__(self, other):
		return self.position == other.position

	def __lt__(self, other):
		return self.f < other.f

class Grid:

	def __init__(self, surface):
		self.width = surface.get_width()
		self.length = surface.get_height()
		self.grid = {(i, j) : Node((i, j), None) for i in range(0, self.width, 50) for j in range(0, self.length, 50)}

	def draw(self, surface):
		for i in range(0, self.width, 50):
			for j in range(0, self.length, 50):
				node = self.grid[(i, j)]
				if node.type == 0:
					pygame.draw.rect(surface, (0, 0, 0), (i, j, 50, 50), 1)
				elif node.type == 2:
					pygame.draw.rect(surface, (0, 0, 255), (i, j, 50, 50))
				elif node.type == 3:
					pygame.draw.rect(surface, (255, 0, 0), (i, j, 50, 50))
				elif node.type == 'path':
					if node.f - Max > 0:
						pygame.draw.rect(surface, (255, 0, 0), (i, j, 50, 50), 10)
					else:
						pygame.draw.rect(surface, (int(255 * (node.f / Max)), int(255 - (255 * node.f / Max)), 0), (i, j, 50, 50), 10)
				else:
					pygame.draw.rect(surface, (0, 0, 0), (i, j, 50, 50))	

# Variables
Map = Grid(window)
Max = 0
Start = False
End = False
Path = False
# Mainloop

run = True

while run:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	if Path:
		Map.grid[Path[0]].type = 'path'
		Path.pop(0)
		pygame.time.delay(100)

	check_inputs(window, Map)

	update_window(window, Map)

	pygame.display.update()

