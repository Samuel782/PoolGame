#
#   -- Pool Game --
#     Class Ball
#
# Author: Samuel Luggeri
#

import pygame

class Ball:
    # Colori Palle
    COLORS = {
        0: (255, 255, 255),
        1: (255, 215, 0),
        2: (30, 144, 255),
        3: (220, 20, 60),
        4: (128, 0, 128),
        5: (255, 140, 0),
        6: (34, 139, 34),
        7: (139, 69, 19),
        8: (0, 0, 0),
        9: (255, 215, 0),
        10: (30, 144, 255),
        11: (220, 20, 60),
        12: (128, 0, 128),
        13: (255, 140, 0),
        14: (34, 139, 34),
        15: (139, 69, 19)
    }
    def __init__(self, x, y, vx, vy, radius, ball_id):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = self.COLORS.get(ball_id, (255, 255, 255))

    def stop_if_slow(self):
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0

    # 🏃 movimento + attrito
    def move(self, dt=1):
        # spostamento
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # attrito (tempo-indipendente)
        friction = 0.98
        self.vx *= friction
        self.vy *= friction

        # stop naturale (evita jitter)
        self.stop_if_slow()

    # 🎨 disegno
    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )


    def bounce(self, left, right, top, bottom):
        RESTITUTION = 0.85

        # sinistra
        if self.x - self.radius <= left:
            self.x = left + self.radius
            self.vx *= -RESTITUTION

        # destra
        elif self.x + self.radius >= right:
            self.x = right - self.radius
            self.vx *= -RESTITUTION

        # alto
        if self.y - self.radius <= top:
            self.y = top + self.radius
            self.vy *= -RESTITUTION

        # basso
        elif self.y + self.radius >= bottom:
            self.y = bottom - self.radius
            self.vy *= -RESTITUTION