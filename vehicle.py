import pygame
from pygame.surface import Surface
from game import AbsctractScene, Game, convert
from pymunk import Space, Body, Segment
from math import ceil
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
        # if self.scroll_x > self.images[0].get_width():
        #     self.scroll_x = 0
        # if self.scroll_x < 0:
        #     self.scroll_x = self.images[0].get_width()
    
    def render(self, display: Surface):
        display_width = display.get_width()
        image_width = self.images[0].get_width()
        
        number_of_images = ceil(display_width/image_width) + 5
        
        # for image in self.images:
        for image_idx in range(len(self.images)):
            image = self.images[image_idx]
            for i in range(number_of_images):
                x_shift = (self.scroll_x * (image_idx + 1) * 0.3) % image.get_width()
                display.blit(image, ((i * image_width * 0.99 - x_shift), 0))


class Car:
    def render(self, display: Surface):
        pass
    

class Terrain:
    def __init__(self, width: int, y: int, space: Space) -> None:
        self.body = Body(body_type=Body.STATIC)
        self.body.position = width/2, y
        self.shape = Segment(self.body, (-width/2, 0), (width/2, 0), 1)
        self.shape.density = 1
        space.add(self.body, self.shape)
    
    def render(self, display: Surface):
        h = display.get_height()
        a = convert(self.body.local_to_world(self.shape.a), h)
        b = convert(self.body.local_to_world(self.shape.b), h)
        pygame.draw.line(display, (255, 255, 255), a, b, 3)


class VehicleScene(AbsctractScene):
    def __init__(self) -> None:
        self.space = Space()
        self.car = Car()
        self.terrain = Terrain(1500, 50, self.space)
        self.bg = Background()
        
    def handle_pressed_keys(self, pressed: Sequence[bool]):
        if pressed[pygame.K_a]:
            self.bg.step(5)
        if pressed[pygame.K_d]:
            self.bg.step(-5)
        
    def update(self) -> None:
        self.space.step(1/60)
        
        pk = pygame.key.get_pressed()
        self.handle_pressed_keys(pk)
        
    def render(self, display: Surface) -> None:
        self.bg.render(display)
        self.terrain.render(display)
        self.car.render(display)
        

game = Game(
    window_size=(1500, 500),
    background_color=(0, 8, 150),
    fps=60,
)
game.load_scene(VehicleScene)
game.run()