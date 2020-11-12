# Pygame template

import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

# define several useful colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Player(pygame.sprite.Sprite):
    # sprite for the palyer
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "p1_jump.png")).convert()
        self.image.set_colorkey(BLACK) # Originally there will be black fills between the pic and the rect, so set colorkey can make it transparent
        self.rect = self.image.get_rect() # Let the rect part figure out what is the rect of the image
        self.rect.center = (WIDTH / 2, HEIGHT / 2) # Location of the center of the rect when it is initialized
        self.x_speed = 5
        self.y_speed = 5

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # What if the rect is out of the screen? Let make it this way:
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -5

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
    screen.fill(BLUE) # Use RGB
    all_sprites.draw(screen)
    # Double buffering *after* every drawing!
    pygame.display.flip()

pygame.quit()
