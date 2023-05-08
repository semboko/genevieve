import pygame
from math import sin, cos, radians

pygame.init()
display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

x, y = 250, 250
alpha = 0
r = 40

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         print("Rise the coordinate + 10 px")
        #         pass
        
    pk = pygame.key.get_pressed()
    if pk[pygame.K_UP]:
        y -= 10
    if pk[pygame.K_DOWN]:
        y += 10
    if pk[pygame.K_LEFT]:
        x -= 10
    if pk[pygame.K_RIGHT]:
        x += 10
    if pk[pygame.K_a]:
        alpha += radians(5)
    if pk[pygame.K_d]:
        alpha -= radians(5)
    if pk[pygame.K_w]:
        r *= 1.05
    if pk[pygame.K_s]:
        r *= 0.95
    
    display.fill((255, 255, 255))
    pygame.draw.circle(display, (255, 0, 0), (x, y), r)
    
    end_x = x + cos(alpha) * r
    end_y = y - sin(alpha) * r
    
    pygame.draw.line(display, (0, 0, 0), (x, y), (end_x, end_y), 2)
    pygame.display.update()
    clock.tick(60)