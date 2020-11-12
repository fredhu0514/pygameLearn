# Pygame template

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define several useful colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init() # sound or music
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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

        # Machine Gun Mode LOL Add by Fred Hu
        if keystate[pygame.K_k]:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

        # Super Machine Gun LOL Add by Fred Hu
        if keystate[pygame.K_x]:
            bullet_1 = Bullet(self.rect.centerx, self.rect.top)
            bullet_2 = Bullet(self.rect.centerx - 40, self.rect.top + 15)
            bullet_3 = Bullet(self.rect.centerx - 80, self.rect.top + 30)
            bullet_4 = Bullet(self.rect.centerx + 40, self.rect.top + 15)
            bullet_5 = Bullet(self.rect.centerx + 80, self.rect.top + 30)
            all_sprites.add(bullet_1)
            all_sprites.add(bullet_2)
            all_sprites.add(bullet_3)
            all_sprites.add(bullet_4)
            all_sprites.add(bullet_5)
            bullets.add(bullet_1)
            bullets.add(bullet_2)
            bullets.add(bullet_3)
            bullets.add(bullet_4)
            bullets.add(bullet_5)


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill it if moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


# Load all game graphics
background = pygame.image.load(path.join(img_dir, "blue.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
# meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_small2.png", "meteorBrown_tiny1.png", "meteorBrown_tiny2.png", "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png", "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Score counting
score = 0

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
        # Shoot event
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check see if a bullet hit the mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # First True deletes the hitten mob; second True deletes the hitten bullet
    # Add a mob whenever we destroyed one
    for hit in hits:
        score += 50 - hit.radius
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    # Check see if a mob hit the Player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle) # Any mob that hit the player
    if hits:
        running = False


    # Draw / render
    screen.fill(BLACK) # Use RGB
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    # Double buffering *after* every drawing!
    pygame.display.flip()

pygame.quit()
