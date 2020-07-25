#!\usr\bin\env python 
#
# PathFinding Visualizer Using Pygame
#
#

import pygame
import threading
import sys
from Grid import Node, Grid
from Buttons import Button, Algorithm_Button
from JPS import JPS
from AStar import AStar
from Djikstra import Djikstra

# Initialize Pygame

pygame.init()

screen = pygame.display.set_mode((1000, 800))

pygame.display.set_caption('PathFinding Visualizer')

# Screen Functions

def event_check(surface, grid, *buttons):

	""" CHECKING FOR USER INPUTS """

	global run
	global pathfinding_algorithm # Which Algorithm To Use

	# Check Game Events
	for event in pygame.event.get():

		# IF CLOSE BUTTON PRESSED
		if event.type == pygame.QUIT:
			run = False

		# If Not Pathfinding
		if threading.active_count() == 1:

			# IF MOUSE MOVED
			if event.type == pygame.MOUSEMOTION:

				mouse_x, mouse_y = pygame.mouse.get_pos() # Mouse Position

				for button in buttons:

					color = button.color.hsva

					if button.isHover(mouse_x, mouse_y):

						button.color.hsva = (color[0], 60, color[2], color[3]) # Change Button Color On Hover

					else:

						button.color.hsva = (color[0], 100, color[2], color[3]) # Revert Button Color If Not Hover


				if mouse_x > 0 and mouse_x < grid.width and mouse_y > 0 and mouse_y < grid.height: # If Mouse Is On Top Of Grid

					x, y = (mouse_x//grid.interval), (mouse_y//grid.interval) # Rounded Coordinates For Which Square Mouse Is On

					if grid.wall_edit == True: # If Initially Pressed On Empty Space

						if grid.grid[(x, y)].type == 'empty': # If The Node The Mouse Is Above Is Empty Space

							grid.grid[(x, y)].type = 'wall' # Change Node To A Wall

					elif grid.wall_edit == False: # If Initially Pressed On A Wall

						if grid.grid[(x, y)].type == 'wall': # If The Node The Mouse Is Above A Wall

							grid.grid[(x, y)].type = 'empty' # Change Node To Empty Space

			# IF MOUSECLICK
			if event.type == pygame.MOUSEBUTTONDOWN:

				# COORDINATES OF MOUSE
				mouse_x, mouse_y = pygame.mouse.get_pos()

				for button in buttons:

					# COLOR OF BUTTON IN HSVA
					color = button.color.hsva

					# WHEN MOUSECLICK OVER A BUTTON
					if button.isHover(mouse_x, mouse_y):

						# CHANGE BUTTON'S COLOR
						button.color.hsva = (color[0], color[1], 20, color[3])

						# MAKE BUTTON ACTIVE
						button.active = True

						# DEACTIVATE THE OTHER BUTTONS
						for other_button in buttons:

							# IF BUTTON IS THE SAME TYPE AS THE ONE PRESSED
							if type(other_button) != type(button):
								continue

							# OTHER BUTTON'S COLOR
							other_color = other_button.color.hsva

							# IF OTHER BUTTON ISNT THE CURRENT BUTTON, REVERT ITS COLOR
							if button == other_button:
								continue

							else:
								other_button.color.hsva = (other_color[0], other_color[1], 100, other_color[3])
								other_button.active = False

				# CHECKING ALGORITHM BUTTONs

				# IF A* BUTTON PRESSED...
				if astar_button.active:

					pathfinding_algorithm = astar_button.function # USE A* AS PATHFINDING ALGORITHM

					if grid.path:

						grid.soft_reset() # GET RID OF THE PREVIOUS PATH FOUND IN CASE USER WANTS TO REUSE WALLS

				# IF JPS BUTTON PRESSED...
				if jps_button.active:

					pathfinding_algorithm = jps_button.function # USE A* + JUMP POINT SEARCH PATHFINDING ALGORITHM

					if grid.path:

						grid.soft_reset() # GET RID OF THE PREVIOUS PATH FOUND IN CASE USER WANTS TO REUSE WALLS

				# IF DJIKSTRA BUTTON PRESSED...
				if djikstra_button.active:

					pathfinding_algorithm = djikstra_button.function # USE DJIKSTRA AS PATHFINDING ALGORITHM

					if grid.path:

						grid.soft_reset() # GET RID OF THE PREVIOUS PATH FOUND IN CASE USER WANTS TO REUSE WALLS

				# IF CALCULATE BUTTON PRESSED...
				if calculate_button.active and pathfinding_algorithm and grid.starting_position and grid.ending_position and not grid.path:

					# CREATE THREAD TARGETING PATHFINDING ALGORITHM
					algorithm_thread = threading.Thread(target = pathfinding_algorithm, args = (grid.starting_position, grid.ending_position, grid))

					# START THREAD
					algorithm_thread.start()

					# RESET ALGORITHM BUTTONS
					astar_button.reset()

					jps_button.reset()

					djikstra_button.reset()

				# IF MOUSE CURRENTLY ABOVE THE GRID
				if mouse_x > 0 and mouse_x < grid.width and mouse_y > 0 and mouse_y < grid.height and not grid.path:

					# NODE "HITBOX"
					x, y = (mouse_x//grid.interval), (mouse_y//grid.interval)
					
					if start_button.active:

						# Replace the current starting position
						if grid.starting_position:
							grid.grid[grid.starting_position].type = 'empty'

						# Create New Starting Position
						grid.grid[(x, y)].type = 'start_pos'
						grid.starting_position = (x, y)

					if end_button.active:

						# Replace the current ending position
						if grid.ending_position:
							grid.grid[grid.ending_position].type = 'empty'

						# Create New Ending Position
						grid.grid[(x, y)].type = 'end_pos'
						grid.ending_position = (x, y)

					if edit_button.active:

						# IF NODE IS EMPTY, MAKE IT A WALL
						if grid.grid[(x, y)].type == 'empty':
							grid.grid[(x, y)].type = 'wall'
							grid.wall_edit = True

						# IF NODE IS WALL, MAKE IT EMPTY
						elif grid.grid[(x, y)].type == 'wall':
							grid.grid[(x, y)].type = 'empty'
							grid.wall_edit = False

				# IF CLEAR BUTTON IS PRESSED AND CURRENTLY NOT PATHFINDING
				if clear_button.active and threading.active_count() == 1:
					grid.reset()

		# IF MOUSE BUTTON RELEASED
		if event.type == pygame.MOUSEBUTTONUP:

			# RESET WHETHER WALLS ARE ADDED OR DELETED WHEN EDIT IS ACTIVE
			grid.wall_edit = None

			# AFTER CLEAR BUTTON IS PRESSED, RESET IT, IT SHOULD BE ONE TIME CLICK ONLY
			if clear_button.active:

				clear_button.reset()

			# AFTER CALCULATE BUTTON IS PRESSED, RESET IT, IT SHOULD BE ONE TIME CLICK ONLY
			if calculate_button.active:

				calculate_button.reset()

def blit_machine(surface, grid, *buttons):

	""" BLITS OBJECTS ONTO THE SURFACE"""

	# FILL SCREEN WITH WHITE
	screen.fill((255, 255, 255))

	# ADD BUTTONS
	for button in buttons:
		button.draw(surface)

	# DRAW LINES AND NODES
	grid.draw(surface)

# Pygame Objects

pathfinding_algorithm = None

grid = Grid(screen.get_width(), screen.get_height())

start_button = Button((255, 0, 0), (800, 0), 200, 50,'Start.Point')
end_button = Button((0, 255, 0), (800, 100), 200, 50, 'End.Point')
edit_button = Button((150, 0, 155), (800, 200), 200, 50, 'Edit.Walls')
calculate_button = Button((255, 100, 255), (800, 300), 200, 50, 'Calculate.Path')
clear_button = Button((100, 150, 255), (800, 400), 200, 50, 'Clear.Grid')

astar_button = Algorithm_Button((23, 245, 100), (800, 500), 200, 50,  AStar, 'A*')
jps_button = Algorithm_Button((23, 245, 100), (800, 600), 200, 50, JPS, 'A*.JPS')
djikstra_button = Algorithm_Button((23, 245, 100), (800, 700), 200, 50, Djikstra, 'Djikstra')


# Mainloop

run = True

while run:



	blit_machine(screen, grid, start_button, end_button, edit_button, calculate_button, clear_button, astar_button, jps_button, djikstra_button)

	event_check(screen, grid, start_button, end_button, edit_button, calculate_button, clear_button, astar_button, jps_button, djikstra_button)

	pygame.display.update()

