#
#   -- Pool Game --
#     Class Table
#   
# Author: Samuel Luggeri
import pygame

class Table:
    def __init__(self, screen):
        self.screen = screen

        self.GREEN = (34, 139, 34)
        self.BROWN = (139, 69, 19)

        self.margin = 20
        self.original_table_img = pygame.image.load("Assets/felt.png").convert()
        self.scaled_table_img = None
        self.update()


    def update_image(self):
        self.scaled_table_img = pygame.transform.scale(
            self.original_table_img,
            (self.width - 2 * self.margin,
            self.height - 2 * self.margin)
        )

    #  aggiorna dimensioni (utile per resize)
    def update(self):
        self.width = int(self.screen.get_width() * 0.8)
        self.height = int(self.width / (2 / 1))

        self.x = (self.screen.get_width() - self.width) // 2
        self.y = (self.screen.get_height() - self.height) // 2
        self.update_image()

    
    # disegno tavolo
    def draw(self):
        pygame.draw.rect(
            self.screen,
            self.BROWN,
            (self.x, self.y, self.width, self.height)
        )

        self.screen.blit(
            self.scaled_table_img,
            (self.x + self.margin, self.y + self.margin)
        )


    # restituisce area utile per collisioni
    def get_bounds(self):
        left = self.x + self.margin
        right = self.x + self.width - self.margin
        top = self.y + self.margin
        bottom = self.y + self.height - self.margin

        return left, right, top, bottom