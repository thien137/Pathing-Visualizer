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

window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Pathing Visualizer')

def update_window(surface, grid, *buttons):

	surface.fill((255, 255, 255))

	for button in buttons:

		button.draw(surface)

	grid.draw_nodes(surface)

	grid.draw_grid(surface)

def check_inputs(surface, grid, **buttons):

	global Start 
	global End
	global Path
	global Final_Path
	global Max
	global Down

	mouse = pygame.mouse.get_pressed()
	x, y = pygame.mouse.get_pos()
	x = int(grid.interval * (x//grid.interval))
	y = int(grid.interval * (y//grid.interval))

	keys = pygame.key.get_pressed()

	for button in buttons:

		buttons[button].check_highlight(x, y)

	if mouse[0]:

		for button in buttons:

			if buttons[button].highlight == True:

				buttons[button].check_active(buttons)

		# If Mouse Over A Grid, Interact Accordingly...

		if x < grid.width and y < grid.length:

			if buttons['start'].active:
				if Start:
					grid.grid[Start].type = 0
				grid.grid[(x, y)].type = 2
				Start = (x, y)

			if buttons['end'].active and grid.grid[(x, y)].type != 2:
				if End:
					grid.grid[End].type = 0
				grid.grid[(x, y)].type = 3
				End = (x, y)
				Max = math.sqrt((Start[0] - End[0]) ** 2 + (Start[1] - End[1]) ** 2)
			
			if  buttons['edit'].active and grid.grid[(x, y)].type == 0 and Down != True:
				grid.grid[(x, y)].type = 1
				Down = False
			elif not Path and not Final_Path and grid.grid[(x, y)].type == 1 and Down != False:
				grid.grid[(x, y)].type = 0
				Down = True

			if buttons['clear'].active:
				grid.reset()	

	else:
		Down = None

	for button in buttons:

		buttons[button].update()

	if keys[pygame.K_SPACE] and Start and End and not Final_Path:
		
		Path, Final_Path = AStar(Start, End, grid)

		if not Final_Path or not Path:
			grid.reset()

		else:
			Path = Path[:-1]
			Final_Path = Final_Path

	if keys[pygame.K_r] and Start and End:
		grid.reset()

# Color Generator

def color_generator(node, grid):

	red = 0
	green = 0

	if node.f > Max:
		red = 255 - 255 * (node.h/Max - 1)
	elif node.f <= Max:
		red = 255 * (node.h/Max)
		green = 255 - 255 * (node.h/Max)

	return red, green

# Button Functions

def Start_Function(buttons):
	for button in buttons:
		buttons[button].active = False

def End_Function(buttons):
	for button in buttons:
		buttons[button].active = False

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
		self.width = surface.get_width() - 200
		self.length = surface.get_height()
		self.interval = 50
		self.grid = {(i, j) : Node((i, j), None) for i in range(0, self.width, self.interval) for j in range(0, self.length, self.interval)}

	def draw_nodes(self, surface):
		for i in range(0, self.width, self.interval):
			for j in range(0, self.length, self.interval):
				node = self.grid[(i, j)]
				if node.type == 1:
					pygame.draw.rect(surface, (0, 0, 0), (i, j, self.interval, self.interval))
				elif node.type == 2:
					pygame.draw.rect(surface, (0, 255, 255), (i, j, self.interval, self.interval))
				elif node.type == 3:
					pygame.draw.rect(surface, (255, 255, 0), (i, j, self.interval, self.interval))
				elif node.type == 'path':
					red, green = color_generator(node, Max)
					pygame.draw.rect(surface, (red, green, 0), (i, j, self.interval, self.interval))
				elif node.type == 'final_path':
					pygame.draw.rect(surface, (255, 137, 255), (i, j, self.interval, self.interval))

	def draw_grid(self, surface):

		for i in range(0, self.width + self.interval, self.interval):
			pygame.draw.line(surface, (0, 0, 0), (i, 0), (i, self.length), 1)
		for i in range(0, self.length, self.interval):
			pygame.draw.line(surface, (0, 0, 0), (0, i), (self.width, i), 1)

	def reset(self):
		global Start 
		global End
		global Path
		global Final_Path
		global Max
		global Down

		self.grid = {(i, j) : Node((i, j), None) for i in range(0, self.width, self.interval) for j in range(0, self.length, self.interval)}
		Max = 0
		Start = False
		End = False
		Path = False
		Final_Path = False
		Down = None

# Interactive Buttons

class Button:

	def __init__(self, text, xy, color, function):
		self.font = pygame.font.Font('moonglade.ttf', 32)
		self.text = self.font.render(text, True, (0, 0, 0, 100))
		self.color = pygame.Color( *color)
		self.highlight = False
		self.active = False
		self.function = function
		self.x = xy[0]
		self.y = xy[1]
		self.width = 200
		self.length = 50

	def update(self):

		if self.highlight:
			self.color.hsva = (self.color.hsva[0], 60, self.color.hsva[2], self.color.hsva[3])
		else:
			self.color.hsva = (self.color.hsva[0], 100, self.color.hsva[2], self.color.hsva[3])


		if self.active:
			self.color.hsva = (self.color.hsva[0], self.color.hsva[1], 20, self.color.hsva[3])
		else:
			self.color.hsva = (self.color.hsva[0], self.color.hsva[1], 100, self.color.hsva[3])			

	def check_highlight(self, x, y):

		if x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.length:
			self.highlight = True
		else:
			self.highlight = False

	def check_active(self, buttons):

		for button in buttons:

			buttons[button].active = False

		self.active = True 

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.length))
		surface.blit(self.text, (self.x + (self.width - self.text.get_width()) / 2, self.y + (self.length - self.text.get_height()) / 2))

# Variables
Map = Grid(window)
Max = 0
Start = False
End = False
Path = False
Final_Path = False
Down = None

# Buttons

start_button = Button('START', (800, 100), (0, 255, 0), Start_Function)

end_button = Button('END', (800, 200), (255, 0, 0), End_Function)

edit_button = Button('EDIT', (800, 300), (255, 0, 255), None)

calculate_button = Button('CALCULATE', (800, 400), (255, 130, 200), None)

clear_button = Button('CLEAR', (800, 500), (255, 100, 100), None)

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
		if not Path:
			for position in Final_Path:
				Map.grid[position].type = 'final_path'
			Path = False


	check_inputs(window, Map, start = start_button, end = end_button, edit = edit_button, calculate = calculate_button, clear = clear_button)

	update_window(window, Map, start_button, end_button, edit_button, calculate_button, clear_button)

	pygame.display.update()

