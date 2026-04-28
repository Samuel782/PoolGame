import pygame
from ball import Ball
from table import Table

pygame.init()
font = pygame.font.SysFont("Arial", 20)


screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

table = Table(screen)

balls = [
    Ball(800, 200, 12, 8, 10, 8),
    Ball(300, 200, 7, 2, 10, 2)
]

background = pygame.image.load("Assets/Backgroud.png").convert()

while running:

    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            table.update()

    screen.blit(background, (0, 0))

    table.draw()

    for ball in balls:
        ball.move(dt=dt)
        ball.bounce(*table.get_bounds())
        ball.draw(screen)

    fps = clock.get_fps()
    text_surface = font.render(f"FPS: {fps:.1f}", True, (255,255,255))
    screen.blit(text_surface, (10, 10))
    
    pygame.display.flip()

   

pygame.quit()