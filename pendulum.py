import pygame
from game import Game, AbsctractScene, convert
from pymunk import Space, Body, Vec2d, Circle, PivotJoint, PinJoint
from pygame import Surface


class Ball:
    def __init__(self, pos: Vec2d, r: int, space: Space) -> None:
        self.body = Body()
        self.body.position = pos
        
        self.shape = Circle(self.body, r)
        self.shape.density = 1
        
        space.add(self.body, self.shape)

    def render(self, display: Surface) -> None:
        h = display.get_height()
        r = self.shape.radius
        pygame.draw.circle(display, (255, 0, 0), convert(self.body.position, h), r)


class PendulumScene(AbsctractScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = 0, -1000
        self.space.damping = 0.9
        
        self.ball1 = Ball(Vec2d(250, 250), 5, self.space)
        self.ball2 = Ball(Vec2d(400, 250), 50, self.space)
        
        pivot = PivotJoint(self.ball1.body, self.space.static_body, (0, 0), (250, 250))
        self.space.add(pivot)
        
        pin = PinJoint(self.ball1.body, self.ball2.body, (0, 0), (0, 0))
        self.space.add(pin)
        
    def update(self) -> None:
        self.space.step(1/60)
    
    def render(self, display: Surface) -> None:
        self.ball1.render(display)
        self.ball2.render(display)


game = Game(
    window_size=(500, 500),
    background_color=(255, 255, 255),
    fps=60,
)

game.load_scene(PendulumScene)
game.run()