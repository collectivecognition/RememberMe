import pygame, random, sys
from pygame.locals import *

width, height = 640, 480
max_shape_radius = 50.0
cols, rows = 5, 5

pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Remember Me")

colors = {
	"black": pygame.Color(0, 0, 0),
	"white": pygame.Color(255, 255, 255),
	"red": pygame.Color(255, 0, 0),
	"green": pygame.Color(0, 255, 0),
	"blue": pygame.Color(0, 0, 255),
}
shape_colors = ["white", "red", "green", "blue"]

def circle(x, y):
	return pygame.draw.circle(window, colors["blue"], (x, y), int(max_shape_radius))

shapes = [circle]

mousex, mousey = 0, 0
num_shapes = 3

level_shapes = []

# Get a shape index based on x, y coordinates
def get_level_shape_index(x, y):
	for i, s in enumerate(level_shapes):
		if s["x"] == x and s["y"] == y:
			return i

# Get shape based on x, y coordinates
def get_level_shape(x, y):
	return level_shapes[get_level_shapes_index(x, y)]

# Generate level
def generate_level():
	global level_shapes
	level_shapes = [{
		"x": x * width / cols,
		"y": y * height / rows,
		"shape": None,
	} for x in xrange(cols) for y in xrange(rows)]

	shapes_to_initialize = random.sample(level_shapes, num_shapes)
	for s in shapes_to_initialize:
		i = get_level_shape_index(s["x"], s["y"])
		print i
		level_shapes[i]["shape"] = random.choice(shapes)
		# TODO: Random position, color, rotation, etc..
	print level_shapes

# Draw the shapes in the current level
def draw_level():
	for s in level_shapes:
		if s["shape"] != None:
			s["shape"](s["x"], s["y"])

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