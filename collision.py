import math

def resolve_collision(b1, b2):

    dx = b2.x - b1.x
    dy = b2.y - b1.y

    distance = math.hypot(dx, dy)
    min_dist = b1.radius + b2.radius

    # se non collidono, esci
    if distance == 0 or distance > min_dist:
        return

    # normalizzazione vettore collisione
    nx = dx / distance
    ny = dy / distance

    # overlap (quanto sono sovrapposte)
    overlap = min_dist - distance

    # separazione palle (evita incastro)
    b1.x -= nx * overlap / 2
    b1.y -= ny * overlap / 2
    b2.x += nx * overlap / 2
    b2.y += ny * overlap / 2

    # velocità relative
    tx = -ny
    ty = nx
    dpTan1 = b1.vx * tx + b1.vy * ty
    dpTan2 = b2.vx * tx + b2.vy * ty
    dpNorm1 = b1.vx * nx + b1.vy * ny
    dpNorm2 = b2.vx * nx + b2.vy * ny

    # scambio velocità normale (massa uguale)
    restitution = 0.9
    m1 = dpNorm2
    m2 = dpNorm1

    b1.vx = tx * dpTan1 + nx * m1 * restitution
    b1.vy = ty * dpTan1 + ny * m1 * restitution
    b2.vx = tx * dpTan2 + nx * m2 * restitution
    b2.vy = ty * dpTan2 + ny * m2 * restitution