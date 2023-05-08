import pygame
from pygame import Vector2 as V2
from typing import Set
from random import randint

pygame.init()
display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


class Particle:
    def __init__(self, loc: V2) -> None:
        self.loc = loc
        self.r = 5
        self.velocity = V2(randint(-5, 5), 3)
        self.lifetime = 255
        
    def update_loc(self) -> None:
        self.loc += self.velocity
        self.velocity.x *= 0.97
        self.velocity.y *= 1.04
        self.lifetime *= 0.96
            
    def draw(self) -> None:
        cv = 255 - self.lifetime
        pygame.draw.circle(display, (cv, cv, cv), self.loc, self.r)
        

class ParticleSystem:
    def __init__(self) -> None:
        self.particles: Set[Particle] = set()
        
    def emit(self, loc: V2) -> None:
        p = Particle(loc)
        self.particles.add(p)
    
    def draw(self) -> None:
        particles_to_remove = set()
        for p in self.particles:
            p.update_loc()
            p.draw()
            
            if p.lifetime <= 1:
                particles_to_remove.add(p)
                
        for p in particles_to_remove:
            self.particles.remove(p)
            print("Particle", p, "was removed")
            
ps = ParticleSystem()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           exit()
    
    pk = pygame.key.get_pressed()
    
    if pk[pygame.K_SPACE]:
       ps.emit(V2(250, 50)) 
    
    display.fill((255, 255, 255))
    ps.draw()
    pygame.display.update()
    clock.tick(60)