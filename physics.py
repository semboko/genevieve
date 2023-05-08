import pygame
from typing import Tuple
from pymunk import Space, Body, Circle, Segment
from math import sin, cos


pygame.init()
display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

space = Space()
space.gravity = 0, -1000

body = Body()
body.position = 250, 250

shape = Circle(body, 30)
shape.density = 1
shape.elasticity = 1
shape.friction = 1

space.add(body, shape)

floor_body = Body(body_type=Body.STATIC)
floor_body.position = 250, 60

floor_shape = Segment(floor_body, (-250, 10), (250, -10), 1)
floor_shape.density = 1
floor_shape.elasticity = 1
floor_shape.friction = 1

space.add(floor_body, floor_shape)

def convert(pos: Tuple[float, float], h: int) -> Tuple[int, int]:
    x, y = pos
    return round(x), round(h - y)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    display.fill((255, 255, 255))
    a = convert(body.position, 500)
    pygame.draw.circle(display, (255, 0, 0), a, 30)
    
    start_pos = convert(floor_body.local_to_world(floor_shape.a), 500)
    end_pos = convert(floor_body.local_to_world(floor_shape.b), 500)
    pygame.draw.line(display, (0, 0, 0), start_pos, end_pos, 1)
    
    b_x = a[0] + cos(body.angle) * 30
    b_y = a[1] - sin(body.angle) * 30
    
    pygame.draw.line(display, (0, 0, 0), a, (b_x, b_y), 1)
    
    pygame.display.update()
    clock.tick(60)
    space.step(1/60)