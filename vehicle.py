import pygame
from pygame.surface import Surface
from game import AbsctractScene, Game
from pymunk import Space


class Car:
    def render(self, display: Surface):
        pass
    

class Terrain:
    def render(self, display: Surface):
        pass


class VehicleScene(AbsctractScene):
    def __init__(self) -> None:
        self.space = Space()
        self.car = Car()
        self.terrain = Terrain()
        
    def update(self) -> None:
        self.space.step(1/60)
        
    def render(self, display: Surface) -> None:
        self.car.render(display)
        self.terrain.render(display)
        

game = Game(
    window_size=(1000, 500),
    background_color=(0, 8, 150),
    fps=60,
)
game.load_scene(VehicleScene)
game.run()