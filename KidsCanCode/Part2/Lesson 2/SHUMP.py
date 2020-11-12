# Pygame template

import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# define several useful colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init() # sound or music
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 # x location of your ship
        self.rect.bottom = HEIGHT - 10 # y location of your ship
        self.speedx = 0

    def update(self):
        self.speedx = 0
        # Check if the key is down and found which key is down
        keystate = pygame.key.get_pressed() # return a list of all keys pressed down on the keyboard
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
        if (keystate[pygame.K_RIGHT] and (keystate[pygame.K_LEFT] or keystate[pygame.K_a])) or (keystate[pygame.K_LEFT] and (keystate[pygame.K_RIGHT] or keystate[pygame.K_d])) or (keystate[pygame.K_a] and keystate[pygame.K_d]):
            self.speedx = 0
        self.rect.x += self.speedx

        # Set the walls on the two sides
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
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
