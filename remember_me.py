import math, pygame, random, sys
from pygame.locals import *

width, height = 640, 480
min_shape_radius, max_shape_radius = 40.0, 100.0

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

	return pygame.draw.circle(window, shape["color"], shape["position"], shape["radius"])

def square(shape):
	"""Create a square that will fit inside a circle with radius shape.radius"""
	side_length = math.sqrt(shape["radius"] ** 2 / 2)
	return pygame.draw.rect(window, shape["color"], (shape["position"][0] - side_length / 2, shape["position"][1] - side_length / 2, side_length, side_length))

# Global variables to store state information

shapes = [circle, square]

mouse_x, mouse_y = 0, 0
num_shapes = 10

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

def distance_between(a, b):
	"""Calculate the distance between two points"""
	return math.hypot(a[0] - b[0], a[1] - b[1])

def is_shape_in_bounds(shape):
	if shape["position"][0] > shape["radius"] and shape["position"][0] < width - shape["radius"]:
		if shape["position"][1] > shape["radius"] and shape["position"][1] < height - shape["radius"]:
			return True
	return False

def does_shape_collide_with_others(shape):
	"""Check whether a shape overlaps the area (radius) of any others"""
	global level_shapes
	for other in level_shapes:
		if distance_between(shape["position"], other["position"]) < shape["radius"] + other["radius"]:
			break
	else:
		return False
	return True

def generate_level():
	"""Generate a new level"""
	global level_shapes

	for s in xrange(num_shapes):
		shape = None
		while True: # FIXME: Not terribly pythonic :P
			print "Trying..."
			shape = {
				"position": [
					random.randint(0, width),
					random.randint(0, height),
				],
				"radius": random.randint(min_shape_radius, max_shape_radius),
				"color": colors[random.choice(shape_colors)],
				"shape": random.choice(shapes),
			}
			if not does_shape_collide_with_others(shape):
				if is_shape_in_bounds(shape):
					break
		level_shapes.append(shape)

def draw_level():
	"""Draw the shapes in the current level"""
	for s in level_shapes:
		if s["shape"] != None:
			s["shape"](s)

def next_level():
	"""Increment difficulty before generating the next level"""
	pass

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
			mouse_x, mouse_y = event.pos

	draw_level()

	circle({
		"position": [mouse_x, mouse_y],
		"radius": 10,
		"color": colors["white"]
	})

	window.set_alpha(100)

	pygame.display.update()
	fpsClock.tick(30)