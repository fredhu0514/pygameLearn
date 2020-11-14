# Pygame template
# Art from Kenney.nl and JROB774
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

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

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, percentage):
    if percentage < 0:
        percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = int((percentage / 100) * BAR_LENGTH)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

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
        self.shield = 100
        self.shoot_dalay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
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

        if keystate[pygame.K_j]:
            self.continuous_shoot()

        # Super Machine Gun LOL Add by Fred Hu
        if keystate[pygame.K_q]:
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
            super_machine_gun_snd.play()

        # Check if unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom =  HEIGHT - 10

    def continuous_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_dalay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                machine_gun_snd.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                machine_gun_snd.play()
                self

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

    def hide(self):
        # hide the player for temp
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 400)

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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, metoer_radius=0):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
        self.metoer_width = 0
        if self.size == 'lg':
            self.metoer_width = metoer_radius * 2

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                if self.size == 'lg':
                    self.image = pygame.transform.scale(self.image, (int(self.metoer_width * 1.8), int(self.metoer_width * 1.8)))
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speedy
        # kill it if moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "blue.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_small2.png", "meteorBrown_tiny1.png", "meteorBrown_tiny2.png", "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png", "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(2, 14):
    filename = "exp" + str(i) + ".png"
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
for i in range(1, 7):
    filename = "expl" + str(i) + ".png"
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (130, 130))
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot.wav"))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, "Shield.wav"))
power_sound = pygame.mixer.Sound(path.join(snd_dir, "Powerup.wav"))
super_machine_gun_snd = pygame.mixer.Sound(path.join(snd_dir, "Machinegun.wav"))
player_die_snd = pygame.mixer.Sound(path.join(snd_dir, "lose_one_live.wav"))
machine_gun_snd = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot_m.wav"))
expl_sound = []
for snd in ["Explosion.wav", "Explosion2.wav"]:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'bgm_Fred.wav'))
pygame.mixer.music.set_volume(0.5)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()

# Score counting
score = 0

pygame.mixer.music.play(loops=-1) # continuously loop when it is finished
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
        random.choice(expl_sound).play()
        expl = Explosion(hit.rect.center, 'lg', hit.radius)
        all_sprites.add(expl)
        # 10% chance of dropping powerups
        if random.random() > 0.97:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # Check see if a mob hit the Player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # Any mob that hit the player
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        random.choice(expl_sound).play()
        newmob()
        if player.shield <= 0:
            player_die_snd.play()
            death_explosion = Explosion(player.rect.center, 'player', 0)
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check if the splayer hit the powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()

    # if the player died and the explosion has finished playing
    if player.lives <= 0 and not death_explosion.alive():
        running = False

    # Draw / render
    screen.fill(BLACK) # Use RGB
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # Double buffering *after* every drawing!
    pygame.display.flip()

pygame.quit()
