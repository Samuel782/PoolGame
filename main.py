import pygame
import math
from ball import Ball
from table import Table
from collision import resolve_collision

pygame.init()

font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

background = pygame.image.load("Assets/Backgroud.png").convert()
running = True

table = Table(screen)

# ---------------- RACK SYSTEM ----------------
def create_rack(start_x, start_y, radius):
    balls = []
    ball_id = 1
    rows = 5
    for row in range(rows):
        for col in range(row + 1):
            # 1.732 è l'altezza di un triangolo equilatero
            x = start_x + row * (radius * 1.732) 
            y = start_y + (col * radius * 2) - (row * radius)
            balls.append(Ball(x, y, 0, 0, radius, ball_id))
            ball_id += 1
    return balls


# ---------------- BALLS ----------------
cue_ball = Ball(600, 410, 0, 0, 15, 0)

balls = [cue_ball]
balls.extend(create_rack(800, 400, 15))


# ---------------- STECCA ----------------
charging_up = False
charging_down = False

power = 0
max_power = 100
charge_speed = 80


# ---------------- UTILS ----------------
def is_still(ball):
    return abs(ball.vx) < 0.05 and abs(ball.vy) < 0.05


# ---------------- LOOP ----------------
while running:

    dt = clock.tick(60) / 1000

    # -------- INPUT --------
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

        # TIRO
        if event.type == pygame.MOUSEBUTTONDOWN and is_still(cue_ball):

            force = (power / max_power) ** 2 * 20

            cue_ball.vx += math.cos(angle) * force
            cue_ball.vy += math.sin(angle) * force

            power = 0

    # -------- POWER SYSTEM --------
    if charging_up:
        power += charge_speed * dt
    if charging_down:
        power -= charge_speed * dt

    power = max(0, min(max_power, power))


    # -------- FISICA --------
    for ball in balls:
        ball.move(dt)
        ball.bounce(*table.get_bounds())

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            resolve_collision(balls[i], balls[j])


    # -------- ANGLE --------
    mx, my = pygame.mouse.get_pos()

    dx = mx - cue_ball.x
    dy = my - cue_ball.y

    angle = math.atan2(dy, dx)


    # -------- RENDER --------
    screen.blit(background, (0, 0))

    table.draw()

    for ball in balls:
        ball.draw(screen)


    # -------- AIM LINE --------
    if is_still(cue_ball):

        length = (power / max_power) * 120

        end_x = cue_ball.x + math.cos(angle) * length
        end_y = cue_ball.y + math.sin(angle) * length

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (cue_ball.x, cue_ball.y),
            (end_x, end_y),
            3
        )


    # -------- UI --------
    screen.blit(font.render("N: carica potenza", True, (255,255,255)), (20, 20))
    screen.blit(font.render("M: scarica potenza", True, (255,255,255)), (20, 40))

    bar_x, bar_y = 20, 70
    bar_w, bar_h = 200, 20

    fill = (power / max_power) * bar_w

    pygame.draw.rect(screen, (255, 255, 255),
                     (bar_x, bar_y, bar_w, bar_h), 2)

    pygame.draw.rect(screen, (0, 255, 0),
                     (bar_x, bar_y, fill, bar_h))


    # -------- FPS --------
    fps = clock.get_fps()
    text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
    screen.blit(text, (1180, 10))


    pygame.display.flip()

pygame.quit()