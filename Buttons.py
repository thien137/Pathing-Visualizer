#!/usr/env/bin python
#
# Buttons
#
#

import pygame

class Button:

	def __init__(self, color, coordinates, width, height, text = ''):

		self.color = pygame.Color(*color)
		self.x, self.y = coordinates
		self.width = width
		self.height = height
		self.text = text
		self.active = False

	def isHover(self, mouse_x, mouse_y):

		if mouse_x > self.x and mouse_y < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height:
			return True

		return False

	def draw(self, surface):

		# Button Text Box
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

		# Text
		font = pygame.font.Font('moonglade.ttf', 24)
		text = font.render(self.text, True, (0, 0, 0))
		surface.blit(text, (self.x + (self.width - text.get_width()) / 2, self.y + (self.height - text.get_height()) / 2))

	def reset(self):
		self.color.hsva = (self.color.hsva[0], self.color.hsva[1], 100, self.color.hsva[3])
		self.active = False

	def __eq__(self, other):
		return self.text == other.text

class Algorithm_Button(Button):

	def __init__(self, color, coordinates, width, height,  function, text = ''):

		self.color = pygame.Color(*color)
		self.x, self.y = coordinates
		self.width = width
		self.height = height
		self.text = text
		self.active = False
		self.function = function

