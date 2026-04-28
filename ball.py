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
        
        # --- CARICAMENTO E PREPARAZIONE TEXTURE ---
        # Carichiamo l'asset (la striscia rettangolare)
        raw_image = pygame.image.load(f"Assets/balls/poolballs{ball_id}.png").convert_alpha()
        
        # Scaliamo la texture in modo che l'altezza corrisponda al diametro della palla
        # La larghezza viene scalata proporzionalmente per permettere il "loop" della rotazione
        aspect_ratio = raw_image.get_width() / raw_image.get_height()
        tex_height = radius * 2
        tex_width = int(tex_height * aspect_ratio)
        self.texture = pygame.transform.smoothscale(raw_image, (tex_width, tex_height))
        
        # Offset per la rotazione (simula il rotolamento sull'asse X)
        self.tex_offset = 0
        
        # --- CREAZIONE MASCHERA CIRCOLARE ---
        # Creiamo una superficie che useremo per "ritagliare" la texture a forma di cerchio
        self.mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.mask, (255, 255, 255, 255), (radius, radius), radius)

        # Costanti fisiche
        self.friction = 0.985
        self.restitution = 0.85

    def move(self, dt=1):
        scale = dt * 60
        self.x += self.vx * scale
        self.y += self.vy * scale

        # Applichiamo attrito
        self.vx *= self.friction
        self.vy *= self.friction

        # Fermiamo la palla se la velocità è minima
        if abs(self.vx) < 0.1: self.vx = 0
        if abs(self.vy) < 0.1: self.vy = 0
        
        # Aggiorniamo l'offset della texture in base alla velocità (effetto rotazione)
        # Dividiamo per il raggio per dare una sensazione di rotolamento realistica
        self.tex_offset = (self.tex_offset + self.vx) % (self.texture.get_width() // 2)

    def draw(self, screen):
        r = self.radius
        
        # 1. Creiamo una superficie temporanea per la palla di questo frame
        ball_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        
        # 2. Disegniamo la texture scorrevole sulla superficie della palla
        # Disegniamo due volte la texture affiancata per gestire il loop continuo
        ball_surface.blit(self.texture, (-self.tex_offset, 0))
        ball_surface.blit(self.texture, (-self.tex_offset + (self.texture.get_width() // 2), 0))
        
        # 3. Applichiamo il ritaglio circolare (Maschera)
        # Il flag BLEND_RGBA_MIN mantiene solo i pixel dove la maschera è bianca
        ball_surface.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        # 4. Disegniamo la palla "finita" sullo schermo principale
        screen.blit(ball_surface, (int(self.x - r), int(self.y - r)))

        # 5. --- EFFETTI DI LUCE (FAKE 3D) ---
        # Creiamo un overlay per luci e ombre
        overlay = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        
        # Luce riflessa (Highlight) in alto a sinistra
        pygame.draw.circle(
            overlay, 
            (255, 255, 255, 100), 
            (int(r * 0.6), int(r * 0.6)), 
            int(r * 0.3)
        )
        
        # Ombra sferica per dare profondità
        # Usiamo un gradiente semplice o un cerchio scuro con alpha basso
        pygame.draw.circle(
            overlay, 
            (0, 0, 0, 40), 
            (r, r), 
            r, 
            width=int(r * 0.2) # Ombra solo sui bordi
        )
        
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
