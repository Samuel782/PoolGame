import pygame
import math
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
charging_up = False
charging_down = False
angle = 0
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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                charging_up = True
            if event.key == pygame.K_m:
                charging_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_n:
                charging_up = False
            if event.key == pygame.K_m:
                charging_down = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            force = power * 0.2
            balls[0].vx += math.cos(angle) * force
            balls[0].vy += math.sin(angle) * force
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

    mx, my = pygame.mouse.get_pos()
    dx = mx - balls[0].x
    dy = my - balls[0].y
    angle = math.atan2(dy, dx)

    if charging_up:
        power += charge_speed * dt
    if charging_down:
        power -= charge_speed * dt
    power = max(0, min(max_power, power))


    length = (power / max_power) * 100

    end_x = balls[0].x + math.cos(angle) * length
    end_y = balls[0].y + math.sin(angle) * length

    pygame.draw.line(
            screen,
            (255, 255, 255),
            (balls[0].x, balls[0].y),
            (end_x, end_y),
            3
        )




    fps = clock.get_fps()
    text_surface = font.render(f"FPS: {fps:.1f}", True, (255,255,255))
    screen.blit(text_surface, (10, 10))
    
    pygame.display.flip()

   

pygame.quit()