import math, pygame, random, sys
from pygame.locals import *

width, height = 640, 480
center = (width / 2, height / 2)
min_shape_radius, max_shape_radius = 40, 100

# Event constants
COUNTDOWN = pygame.USEREVENT + 1

# Initialize pygame
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

pygame.font.init()
font = pygame.font.Font("resources/fonts/DroidSans-Bold.ttf", 64)

def circle(shape):
	"""Create a circle"""
	return pygame.draw.circle(window, shape["color"], shape["position"], shape["radius"])

def square(shape):
	"""Create a square that will fit inside a circle with radius shape.radius"""
	side_length = math.sqrt((shape["radius"] * 2) ** 2 / 2)
	return pygame.draw.rect(window, shape["color"], (shape["position"][0] - side_length / 2, shape["position"][1] - side_length / 2, side_length, side_length))

# Global variables to store state information
shapes = [circle, square]

mouse_x, mouse_y = 0, 0
num_shapes = 3
seconds_remaining = 10
current_guess = 0

level_shapes = []
guess_shapes = []

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
	"""Check whether the given shape is contained within the bounds of the screen"""
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
	global level_shapes, seconds_remaining

	for s in xrange(num_shapes):
		shape = None
		while True: # FIXME: Not terribly pythonic :P
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

	# Start the timer
	seconds_remaining = 1
	pygame.time.set_timer(COUNTDOWN, 1000)

def draw_level():
	"""Draw the shapes in the current level and level-specific UI elements"""
	draw_shapes(level_shapes)

	# Render countdown timer
	label = font.render("%i" % seconds_remaining, 1, colors["white"])
	pos = label.get_rect(centerx = center[0], centery = center[1])
	window.blit(label, pos)

def draw_guesses():
	"""Draw the current guesses"""
	draw_shapes(guess_shapes)

def draw_shapes(shapes):
	for s in shapes:
		if s["shape"] != None:
			s["shape"](s)

def draw_guess():
	"""Draw the current shape being placed at the location of the mouse cursor"""
	shape = level_shapes[current_guess]
	shape["shape"]({
		"position": [mouse_x, mouse_y],
		"radius": shape["radius"],
		"color": shape["color"],
	})

def next_level():
	"""Increment difficulty before generating the next level"""
	pass

def count_down():
	"""Count down by one"""
	global mode, seconds_remaining

	seconds_remaining -= 1

	if seconds_remaining <= 0:
		mode = "guess"

# Generate initial level
generate_level()

# Main game loop
mode = "show"

while True:
	window.fill(colors.get("black"))

	# Process event queue
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mouse_x, mouse_y = event.pos
		elif event.type == MOUSEBUTTONUP and mode == "guess":
			# Place shape at mouse coords
			shape = level_shapes[current_guess]
			shape["position"] = (mouse_x, mouse_y)
			guess_shapes.append(shape)
			current_guess += 1

			# Cancel timer
			pygame.time.set_timer(COUNTDOWN, 0)

			# End condition
			if current_guess >= num_shapes:
				mode = "results"
		elif event.type == COUNTDOWN:
			count_down()

	# Render
	if mode == "show":
		draw_level()
	elif mode == "guess":
		draw_guesses()
		draw_guess()
	elif mode == "results":
		pass

	# Update display and advance time
	pygame.display.update()
	fpsClock.tick(30)