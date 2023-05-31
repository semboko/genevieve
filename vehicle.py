import pygame
from pygame.surface import Surface
from game import AbsctractScene, Game, convert
from pymunk import Space, Body, Segment, Vec2d, Poly, Circle, PivotJoint, ShapeFilter, SimpleMotor
from math import ceil, degrees
from typing import Sequence


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
            
    def accelerate(self, rate: int):
        self.motor.rate += rate
    
    def render(self, display: Surface, shift_x: float):
        
        pos = convert(self.body.position, display.get_height())
        pos = pygame.Vector2(pos) - pygame.Vector2(shift_x, 0)
        
        dest_rect = self.img.get_rect(center=pos)
        display.blit(self.img, dest_rect)
        
        # vertices = self.shape.get_vertices()
        # points = []
        # for v in vertices:
        #     world_v = self.body.local_to_world(v)
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
    def __init__(self, width: int, y: int, space: Space) -> None:
        self.body = Body(body_type=Body.STATIC)
        self.body.position = width/2, y
        self.shape = Segment(self.body, (-width/2, 0), (width/2, 0), 1)
        self.shape.density = 1
        self.shape.friction = 1
        space.add(self.body, self.shape)
    
    def render(self, display: Surface, shift_x: float):
        h = display.get_height()
        a = convert(self.body.local_to_world(self.shape.a), h)
        b = convert(self.body.local_to_world(self.shape.b), h)
        
        a = pygame.Vector2(a) - pygame.Vector2(shift_x, 0)
        b = pygame.Vector2(b) - pygame.Vector2(shift_x, 0)
        
        pygame.draw.line(display, (255, 255, 255), a, b, 3)


class VehicleScene(AbsctractScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = 0, -1000
        self.car = Car(Vec2d(200, 300), self.space)
        self.terrain = Terrain(1500, 50, self.space)
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
        
        pk = pygame.key.get_pressed()
        self.handle_pressed_keys(pk)
        self.car.motor.rate *= 0.95
        
    def render(self, display: Surface) -> None:
        shift_x = self.get_distance()
        
        self.bg.render(display, shift_x)
        self.terrain.render(display, shift_x)
        self.car.render(display, shift_x)
        

game = Game(
    window_size=(1500, 500),
    background_color=(0, 8, 150),
    fps=60,
)
game.load_scene(VehicleScene)
game.run()