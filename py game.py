import pygame
import random
from os import path
import time
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
a = 0
WIDTH = 480
HEIGHT = 600
FPS = 40

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
  
    def shoot(self):   
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 15)
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
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -130 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 6)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y+20
        self.rect.centerx = x
        self.speedy = -12

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Load all game graphics
background = pygame.image.load(path.join(img_dir,"background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "spaceShip.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir,"spaceMissile.png")).convert()

meteor_images = []
meteor_list = ['meteorGrey_big1.png','meteorGrey_big2.png', 'meteorGrey_med1.png', 'meteorGrey_med1.png'
                 , 'meteorGrey_small1.png', 'meteorGrey_small2.png',
               'meteorGrey_tiny1.png','meteorGrey_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    
pygame.mixer.music.load(path.join(snd_dir, 'DST-RailJet-LongSeamlessLoop.mp3'))
pygame.mixer.music.set_volume(10)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(25):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0
start = time.time()


#gets the time
def gettime():
    return (time.time()-start-a)
#orints time
def timee(a):
    sec = int(time.time() - start -a)
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    timer = (f"Time: {int(mins)}:{sec}")   
    draw_text(screen, str(timer), 18, 40, 10)
#draws text
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
pygame.mixer.music.play(loops=-1)


# Game loop
running = True
while running:
    k = (gettime())
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.shoot()

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        random.choice(expl_sounds).play()
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(f"Score :{score}"), 18, WIDTH - 40, 10)
    timee(a)
    pygame.display.flip()
    if (int(gettime()) % 10000) == 0 and int(gettime()) != 0:
        num1 = random.randint(1,20)
        num2 = random.randint(1,20)
        operation = random.randint(1,2)
        if operation == 1 :
            result = num1-num2
            sign = '-'
        elif operation == 2:
            result = num1+num2
            sign = '+'
        draw_text(screen, str(f"Whats {num1} {sign} {num2}?"), int(HEIGHT/2), int(WIDTH/2), 10)
        while True:
            answer = int(input(f"Whats {num1} {sign} {num2}?"))
            if answer == (result) :
                break
            else:
                print('Wrong answer')
        time.sleep(2)
        r = (gettime())
        a = a + (r-k)-1
        
pygame.quit()

 



