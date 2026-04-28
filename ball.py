import pygame
import math

class Ball:
    def __init__(self, x, y, vx, vy, radius, ball_id):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.ball_id = ball_id
        
        # --- CARICAMENTO E OTTIMIZZAZIONE TEXTURE ---
        # Carichiamo l'immagine originale
        img = pygame.image.load(f"Assets/balls/poolballs{ball_id}.png").convert_alpha()
        w, h = img.get_size()

        # 1. GESTIONE CROP (RITAGLIO)
        # Per evitare che la palla sembri "piena", non dobbiamo tagliare troppo bianco.
        # Tagliamo solo il 15% sopra e sotto per centrare bene la fascia numerata.
        margin = int(h * 0.15)
        stripe_h = h - (margin * 2)
        crop_rect = pygame.Rect(0, margin, w, stripe_h)
        cropped_img = img.subsurface(crop_rect)

        # 2. STRETCH ORIZZONTALE
        # L'altezza della texture deve essere il diametro: $2 \times radius$.
        self.tex_height = int(radius * 2)
        
        # Per evitare il numero "stretto e lungo", la larghezza deve coprire 
        # quasi tutta la circonferenza visibile. Usiamo un fattore di 3.0.
        self.tex_width = int(self.tex_height * 3.0) 
        
        # Scaliamo la texture forzando le proporzioni
        self.texture = pygame.transform.smoothscale(cropped_img, (self.tex_width, self.tex_height))
        
        self.tex_offset = 0
        
        # --- MASCHERA CIRCOLARE (Pre-calcolata per performance) ---
        self.mask = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.mask, (255, 255, 255, 255), (radius, radius), radius)

        # --- FISICA ---
        self.friction = 0.985
        self.restitution = 0.85

    def move(self, dt=1):
        # Il dt che passi è in secondi (es. 0.016), lo scaliamo per il framerate
        scale = dt * 60
        self.x += self.vx * scale
        self.y += self.vy * scale

        # Attrito
        self.vx *= self.friction
        self.vy *= self.friction

        # Soglia di arresto
        if abs(self.vx) < 0.1: self.vx = 0
        if abs(self.vy) < 0.1: self.vy = 0
        
        # ROTAZIONE: L'offset della texture segue la velocità sull'asse X
        # Dividiamo per un fattore (es. 0.8) per rendere la rotazione fluida
        if self.vx != 0:
            self.tex_offset = (self.tex_offset + self.vx * 0.8) % self.tex_width

    def draw(self, screen):
        r = self.radius
        # 1. Creiamo la superficie della palla
        ball_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        
        # 2. Disegniamo la texture con "infinite wrapping"
        # Calcoliamo dove far partire il primo blit
        rel_x = - (self.tex_offset % self.tex_width)
        
        # Disegniamo la texture tre volte affiancata per coprire ogni buco durante il loop
        ball_surface.blit(self.texture, (rel_x, 0))
        ball_surface.blit(self.texture, (rel_x + self.tex_width, 0))
        ball_surface.blit(self.texture, (rel_x - self.tex_width, 0))
        
        # 3. Ritaglio a cerchio (Alpha Masking)
        ball_surface.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        
        # 4. Posizionamento sullo schermo
        screen.blit(ball_surface, (int(self.x - r), int(self.y - r)))

        # 5. EFFETTO 3D (Ombra e Luce)
        # Questo strato non ruota, dando l'illusione di una sfera solida
        overlay = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        
        # Ombra sferica profonda sui bordi
        pygame.draw.circle(overlay, (0, 0, 0, 70), (r, r), r, width=int(r * 0.2))
        
        # Punto luce (Highlight) in alto a sinistra
        pygame.draw.circle(overlay, (255, 255, 255, 90), (int(r * 0.6), int(r * 0.6)), int(r * 0.3))
        
        screen.blit(overlay, (int(self.x - r), int(self.y - r)))

    def bounce(self, left, right, top, bottom):
        if self.x - self.radius <= left:
            self.x = left + self.radius
            self.vx *= -self.restitution
        elif self.x + self.radius >= right:
            self.x = right - self.radius
            self.vx *= -self.restitution

        if self.y - self.radius <= top:
            self.y = top + self.radius
            self.vy *= -self.restitution
        elif self.y + self.radius >= bottom:
            self.y = bottom - self.radius
            self.vy *= -self.restitution
