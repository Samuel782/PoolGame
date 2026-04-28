import pygame
from ball import Ball
from table import Table
from collision import *

pygame.init()
font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
background = pygame.image.load("Assets/Backgroud.png").convert()
running = True

table = Table(screen)
balls = [
    Ball(600, 410, 0, 0, 10, 0), #CUEBALL
    Ball(800, 400, 0, 0, 10, 8),
    Ball(800, 420, 0, 0, 10, 2)
]

## STECCA
charging = False
power = 0
max_power = 100
charge_speed = 80

##UI 
bar_x = 20
bar_y = 50
bar_width = 200
bar_height = 20

while running:

    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            table.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            charging = True
            power = 0

        if event.type == pygame.MOUSEBUTTONUP and charging:
            charging = False
            balls[0].vx += power * 0.1
            # balls[0].vy += power * 0.1
            power = 0

    screen.blit(background, (0, 0))

    table.draw()

    for ball in balls:
        ball.move(dt)
        ball.bounce(*table.get_bounds())

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            resolve_collision(balls[i], balls[j])

    for ball in balls:
        ball.draw(screen)

    if charging:
        power += charge_speed * dt
        if power > max_power:
            power = max_power


    ### UI STECCA
    fill_width = (power / max_power) * bar_width

    # contorno
    pygame.draw.rect(screen, (255, 255, 255),
                 (bar_x, bar_y, bar_width, bar_height), 2)

    # riempimento
    pygame.draw.rect(screen, (0, 255, 0),
                 (bar_x, bar_y, fill_width, bar_height))





    fps = clock.get_fps()
    text_surface = font.render(f"FPS: {fps:.1f}", True, (255,255,255))
    screen.blit(text_surface, (10, 10))
    
    pygame.display.flip()

   

pygame.quit()