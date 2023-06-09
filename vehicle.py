import pygame
from random import randint
from pygame.surface import Surface
from game import AbsctractScene, Game, convert
from pymunk import Space, Body, Segment, Vec2d, Poly, Circle, PivotJoint, ShapeFilter, SimpleMotor, GearJoint, Shape
from math import ceil, degrees
from typing import Sequence, Tuple
from vnoise import Noise


x0 = 200
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 500

class Background:
    def __init__(self) -> None:
        self.images = [
            pygame.image.load("./assets/bg-0.png"),
            pygame.image.load("./assets/bg-1.png"),
            pygame.image.load("./assets/bg-2.png"),
        ]
        self.scroll_x = 0
        
    def step(self, d: int) -> None:
        self.scroll_x -= d
    
    def render(self, display: Surface, shift_x: float):
        display_width = display.get_width()
        image_width = self.images[0].get_width()
        
        number_of_images = ceil(display_width/image_width) + 5
        
        # for image in self.images:
        for image_idx in range(len(self.images)):
            image = self.images[image_idx]
            for i in range(number_of_images):
                x_shift = (shift_x * (image_idx + 1) * 0.3) % image.get_width()
                # x_shift = shift_x % image_width
                display.blit(image, ((i * image_width * 0.99  - x_shift), 0))


class Car:
    def __init__(self, origin: Vec2d, space: Space) -> None:
        self.cg = ShapeFilter(group=0b1)
        
        self.img = pygame.image.load("./assets/rover.png")
        
        self.origin = origin
        self.origin_shift = Vec2d(89, -58)
        self.body = Body()
        self.body.position = origin + self.origin_shift
        
        figma_coordinates = (
            Vec2d(20, 0),
            Vec2d(20, 57),
            Vec2d(0, 76),
            Vec2d(0, 93),
            Vec2d(7, 115),
            Vec2d(14, 93),
            Vec2d(64, 83),
            Vec2d(95, 83),
            Vec2d(84, 115),
            Vec2d(111, 87),
            Vec2d(147, 87),
            Vec2d(155, 115),
            Vec2d(162, 87),
            Vec2d(145, 65),
            Vec2d(175, 51),
            Vec2d(161, 25),
            Vec2d(128, 28),
            Vec2d(111, 40),
            Vec2d(55, 40),
            Vec2d(55, 0),
        )
        
        shape_vertices = [
            Vec2d(
                fc[0] - self.origin_shift.x, 
                -1 * self.origin_shift.y - fc[1]
            )
            for fc in figma_coordinates
        ]
        
        self.shape = Poly(self.body, shape_vertices)
        self.shape.density = 1
        self.shape.filter = self.cg
        
        space.add(self.body, self.shape)
        
        self.wheels = [
            Wheel(origin + Vec2d(7, -115), self.cg, space),
            Wheel(origin + Vec2d(85, -115), self.cg, space),
            Wheel(origin + Vec2d(155, -115), self.cg, space),
        ]
        
        for wheel in self.wheels:
            pj = PivotJoint(
                wheel.body, 
                self.body,
                (0, 0),
                self.body.world_to_local(wheel.body.position)
            )
            space.add(pj)
            
        self.motor = SimpleMotor(self.wheels[0].body, self.body, 0)
        space.add(self.motor)
        
        space.add(
            GearJoint(self.wheels[0].body, self.wheels[1].body, 0, 1),
            GearJoint(self.wheels[0].body, self.wheels[2].body, 0, 1),
        )
            
    def accelerate(self, rate: int):
        self.motor.rate += rate
    
    def render(self, display: Surface, shift_x: float):
        
        pos = convert(self.body.position, display.get_height())
        pos = pygame.Vector2(pos) - pygame.Vector2(shift_x, 0)
        
        rotated_img = pygame.transform.rotate(self.img, degrees(self.body.angle))
        dest_rect = rotated_img.get_rect(center=pos)
        display.blit(rotated_img, dest_rect)
        
        # vertices = self.shape.get_vertices()
        # points = []
        # for v in vertices:
        #     world_v = self.body.local_to_world(v) - Vec2d(shift_x, 0)
        #     point = convert(world_v, display.get_height())
        #     points.append(point)
        
        # pygame.draw.polygon(display, (255, 255, 255), points, 1)
        # pygame.draw.circle(display, (255, 0, 0), pos, 5)
        
        for wheel in self.wheels:
            wheel.render(display, shift_x)
        

class Wheel:
    def __init__(self, pos: Vec2d, cgroup: ShapeFilter, space: Space) -> None:
        self.body = Body()
        self.body.position = pos
        
        self.shape = Circle(self.body, 15)
        self.shape.density = 1
        self.shape.friction = 1
        self.shape.elasticity = 0.9
        self.shape.filter = cgroup
        
        space.add(self.body, self.shape)
        
        self.img = pygame.image.load("./assets/wheel.png")
    
    def render(self, display: Surface, shift_x: float) -> None:
        rotated_img = pygame.transform.rotate(self.img, degrees(self.body.angle))
        pos = convert(self.body.position, display.get_height())
        pos = pygame.Vector2(pos) - pygame.Vector2(shift_x, 0)
        
        dest_rect = rotated_img.get_rect(center=pos)
        display.blit(rotated_img, dest_rect)
        
        # pygame.draw.circle(display, (255, 0, 0), pos, 15, 1)
    

class Terrain:
    def __init__(
        self, 
        x_min: float, 
        x_max: float, 
        steps: int, 
        y_min: float, 
        y_max: float, 
        space: Space,
    ) -> None:
        
        terrain_width = x_max - x_min
        self.segment_width = terrain_width // steps
        self.space = space
        self.segments = []
        
        
        noise = Noise().noise1
        
        self.get_y = lambda x: y_min + noise(x/500) * (y_max - y_min)
        
        for x_start in range(x_min, x_max, self.segment_width):
            if not self.segments:
                y_start = self.get_y(x_start)
            else:   
                prev_body, prev_shape = self.segments[-1]
                prev_world_b = prev_body.local_to_world(prev_shape.b)
                y_start = prev_world_b.y
            
            x_end = x_start + self.segment_width
            y_end = self.get_y(x_start)
            
            body, shape = self.create_segment(Vec2d(x_start, y_start), Vec2d(x_end, y_end))
            space.add(body, shape)
            self.segments.append((body, shape))
            
    def create_segment(self, a: Vec2d, b: Vec2d) -> Tuple[Body, Shape]:
        body = Body(body_type=Body.STATIC)
        body.position = a
        
        shape = Segment(body, (0, 0), body.world_to_local(b), 5)
        shape.density = 1
        shape.friction = 1
        return (body, shape)
            
    def update_segments(self, shift_x: int):
        rx = self.segments[-1][0].position.x + self.segment_width
        lx = self.segments[0][0].position.x
        
        xrscreen = x0 + shift_x + WINDOW_WIDTH - x0
        # TODO: xlscreen = 
        
        if rx < xrscreen:
            for x_start in range(int(rx), int(xrscreen), self.segment_width):
                x_end = x_start + self.segment_width
                last_body, last_shape = self.segments[-1]
                y_start = last_body.local_to_world(last_shape.b).y
                y_end = self.get_y(x_end)
                new_segment = self.create_segment(Vec2d(x_start, y_start), Vec2d(x_end, y_end))
                self.space.add(*new_segment)
                self.segments.append(new_segment)
        
        # if lx > xlscreen:
            # for ...
        
    def render(self, display: Surface, shift_x: float):
        h = display.get_height()
        for body, shape in self.segments:
            a = convert(body.local_to_world(shape.a), h)
            b = convert(body.local_to_world(shape.b), h)
            
            a = pygame.Vector2(a) - pygame.Vector2(shift_x, 0)
            b = pygame.Vector2(b) - pygame.Vector2(shift_x, 0)
            
            pygame.draw.line(display, (255, 255, 255), a, b, 3)


class VehicleScene(AbsctractScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = 0, -1000
        self.car = Car(Vec2d(x0, 300), self.space)
        self.terrain = Terrain(0, 1500, 100, 50, 150, self.space)
        self.bg = Background()
        
        self.origin_x = self.car.body.position.x
        
    def get_distance(self):
        return self.car.body.position.x - self.origin_x
        
    def handle_pressed_keys(self, pressed: Sequence[bool]):
        if pressed[pygame.K_a]:
            # self.bg.step(5)
            self.car.accelerate(1)
        if pressed[pygame.K_d]:
            # self.bg.step(-5)
            self.car.accelerate(-1)
        
    def update(self) -> None:
        self.space.step(1/60)
        self.terrain.update_segments(self.get_distance())
        pk = pygame.key.get_pressed()
        self.handle_pressed_keys(pk)
        self.car.motor.rate *= 0.95
        
    def render(self, display: Surface) -> None:
        shift_x = self.get_distance()
        
        self.bg.render(display, shift_x)
        self.terrain.render(display, shift_x)
        self.car.render(display, shift_x)
        

game = Game(
    window_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
    background_color=(0, 8, 150),
    fps=60,
)
game.load_scene(VehicleScene)
game.run()