import pygame
from game import Game, AbsctractScene, convert
from pymunk import Space, Body, Vec2d, Circle, PivotJoint, PinJoint, SimpleMotor
from pygame import Surface
from math import sin, cos

class Ball:
    def __init__(self, pos: Vec2d, r: int, space: Space) -> None:
        self.body = Body()
        self.body.position = pos
        
        self.shape = Circle(self.body, r)
        self.shape.density = 1
        
        space.add(self.body, self.shape)

    def render(self, display: Surface, shift_x: float = 0) -> None:
        h = display.get_height()
        r = self.shape.radius
        target_position = convert(self.body.position, h)
        shifted_position = pygame.Vector2(target_position) - pygame.Vector2(shift_x, 0)
        pygame.draw.circle(display, (255, 0, 0), shifted_position, r)
        
        alpha = self.body.angle
        r = self.shape.radius
        
        if shift_x == 0:
            start_pos = convert(self.body.position, h)
            end_pos = (
                start_pos[0] + r * cos(alpha),
                start_pos[1] - r * sin(alpha),
            )
            pygame.draw.line(display, (0, 0, 0), start_pos, end_pos, 1)


class CustomPinJoint(PinJoint):
    def render(self, display: Surface):
        h = display.get_height()
        
        start_pos = self.a.local_to_world(self.anchor_a)
        end_pos = self.b.local_to_world(self.anchor_b)
        
        pygame.draw.line(display, (0, 0, 0), convert(start_pos, h), convert(end_pos, h), 2)


class PendulumScene(AbsctractScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = 0, -1000
        self.space.damping = 0.9
        
        self.ball1 = Ball(Vec2d(250, 250), 30, self.space)
        self.ball2 = Ball(Vec2d(400, 250), 50, self.space)
        self.ball2.shape.density = 0.1
               
        pivot = PivotJoint(self.ball1.body, self.space.static_body, (0, 0), (250, 250))
        self.space.add(pivot)
        
        self.pin = CustomPinJoint(self.ball1.body, self.ball2.body, (30, 0), (-50, 0))
        self.space.add(self.pin)
    
        self.motor = SimpleMotor(self.ball1.body, self.space.static_body, 3.14)
        self.space.add(self.motor)
        
    def update(self) -> None:
        self.space.step(1/60)
        
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_d]:
            self.motor.rate += 3.14/8
        if pressed[pygame.K_a]:
            self.motor.rate -= 3.14/8
        
        self.motor.rate *= 0.95
    
    def render(self, display: Surface) -> None:
        self.ball1.render(display)
        self.ball2.render(display)
        self.pin.render(display)


if __name__ == "__main__":
    game = Game(
        window_size=(500, 500),
        background_color=(255, 255, 255),
        fps=60,
    )

    game.load_scene(PendulumScene)
    game.run()