import pygame, random, sys
from pygame.locals import *

width, height = 640, 480
max_shape_radius = 40.0

pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Remember Me")

# Constants / methods used for level generation

colors = {
	"black": pygame.Color(0, 0, 0),
	"white": pygame.Color(255, 255, 255),
	"red": pygame.Color(255, 0, 0),
	"green": pygame.Color(0, 255, 0),
	"blue": pygame.Color(0, 0, 255),
}
shape_colors = ["white", "red", "green", "blue"]

def circle(shape):
	return pygame.draw.circle(window, shape["color"], shape["position"], int(max_shape_radius))

def square(shape):
	return pygame.draw.rect(window, shape["color"], (shape["position"]["x"] - shape["radius"], shape["position"]["y"] - shape["radius"] / 2, shape["radius"] * 2, shape["radius"] * 2))

# Global variables to store state information

shapes = [circle, square]

mousex, mousey = 0, 0
num_shapes = 3

level_shapes = []

# Functions

def get_level_shape_index(position):
	"""Get a shape index based on x, y coordinates"""
	for i, s in enumerate(level_shapes):
		if s["position"] == position:
			return i

def get_level_shape(position):
	"""Get shape based on x, y coordinates"""
	return level_shapes[get_level_shapes_index(position)]

def distanceBetween(a, b):
	"""Calculate the distance between two points"""
	return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y}"]) ** 2))

def doesShapeCollideWithOthers(shape):
	"""Check whether a shape overlaps the area (radius) of any others"""
	global level_shapes
	for other in level_shapes:
		if distanceBetween(shape["position"], other["position"]) < math.abs(shape["radius"] + other["radius"]):
			break:
	else:
		return false
	return true

def generate_level():
	"""Generate a new level"""
	global level_shapes

	for s in num_shapes:
		shape = {
			"x": random.range(0, width),
			"y": random.range(0, height),
			"radius": random.range(0, max_shape_radius),
			"color": colors[random.choice(shape_colors)],
			"shape": random.choice(shapes),
		}

def draw_level():
	"""Draw the shapes in the current level"""
	for s in level_shapes:
		if s["shape"] != None:
			s["shape"](s)

# Generate initial level

generate_level()

# Main game loop

while True:
	window.fill(colors.get("black"))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mousex, mousey = event.pos

	draw_level()

	pygame.display.update()
	fpsClock.tick(30)