# Pygame template

import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

# define several useful colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    # sprite for the palyer
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50)) # Square figure
        self.image.fill(GREEN) # fill the image with green color
        self.rect = self.image.get_rect() # Let the rect part figure out what is the rect of the image
        self.rect.center = (WIDTH / 2, HEIGHT / 2) # Location of the center of the rect when it is initialized

    def update(self):
        self.rect.x += 5
        self.rect.y += 5

        # What if the rect is out of the screen? Let make it this way:
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT

# initialize pygame and create window
pygame.init()
pygame.mixer.init() # sound or music
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# Game Loop
running = True
while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK) # Use RGB
    all_sprites.draw(screen)
    # Double buffering *after* every drawing!
    pygame.display.flip()

pygame.quit()
