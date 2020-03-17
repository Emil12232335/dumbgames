import pygame
import random
from os import path
# 600 x 800
WIDTH = 1920
HEIGHT = 1080
FPS = 60
SPEED = 15
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# initialize PyGame and create window
pygame.init()
pygame.mixer.init(22050, -16, 2, 4096)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Spacy - By: Emil Qvarnström")
pygame.mouse.set_visible(False)
pos = pygame.mouse.get_pos()
clock = pygame.time.Clock()
# Fonts
fontTitle = pygame.font.SysFont("Arial", 150, True)
fontLarge = pygame.font.SysFont("Arial", 70, True)
fontMedium = pygame.font.SysFont("Arial", 40, True)
fontSmall = pygame.font.SysFont("Arial", 30, True)
# Load images
player_image = pygame.image.load("chara2.png")
enemy_image = pygame.image.load("ratayz.png")
metro_image = pygame.image.load("metro.png")
highscores = []
highscores.append(1087)
explosion_amin = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75,75))
    explosion_amin.append(img_lg)
player_image = pygame.transform.scale(player_image, (100,100))
enemy_image = pygame.transform.scale(enemy_image, (100,100))
metro_image = pygame.transform.scale(metro_image, (30,30))
musicchoice=random.randint(1,2)
if musicchoice == 1:
    pygame.mixer.music.load("gametrack1.ogg")
if musicchoice == 2:
    pygame.mixer.music.load("gametrack2.ogg")
pygame.mixer.music.play(-1)
hitSound = pygame.mixer.Sound( "hit.ogg")
oneUp = pygame.mixer.Sound("oneup.ogg")
gameOverSound = pygame.mixer.Sound("gameoversound.ogg")
shot = pygame.mixer.Sound("shoot.wav")
menusound = pygame.mixer.Sound("menu.wav")
# Score
kills = 0
totalscore = 0
kills_c = 10
diffcounter = 0
diffcounter2 = 0
level = 1
now = 0
# Settings
bulletPenetration = 0
trippleBullet = 0
running = True
gameOver = False
# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
            self.rect.center = pos

    def shoot(self):
        bullet = Bullets(self.rect.center, self.rect.center)
        all_sprites.add(bullet)
        bullets.add(bullet)
        if trippleBullet == 1:
            bullet = BulletRight(self.rect.center, self.rect.center)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullet = BulletLeft(self.rect.center, self.rect.center)
            all_sprites.add(bullet)
            bullets.add(bullet)
        if bulletPenetration > 0:
            if trippleBullet == 1:
                for i in range(bulletPenetration):
                    bullet = Bullets(self.rect.center, self.rect.center)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    bullet = BulletRight(self.rect.center, self.rect.center)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    bullet = BulletLeft(self.rect.center, self.rect.center)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
            else:
                for i in range(bulletPenetration):
                    bullet = Bullets(self.rect.center, self.rect.center)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4,8)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 30 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,8)
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speedy = -30

    def update(self):
        self.rect.y += self.speedy
        # Kill if no longer visible
        if self.rect.bottom < 0:
            self.kill()
class BulletRight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speedy = -30
        self.speedx = 5
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Kill if no longer visible
        if self.rect.bottom < 0:
            self.kill()
class BulletLeft(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speedy = -30
        self.speedx = -5
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Kill if no longer visible
        if self.rect.bottom < 0:
            self.kill()
class Metro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = metro_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0 ,WIDTH)
        self.rect.y = random.randrange(0, HEIGHT)
        self.speedy = random.randint(8,15)
    def update(self):
        self.rect.y += self.speedy

        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(0, WIDTH)
class Explsion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_amin[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_amin):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_amin[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
# Functions
def splash():
    paused = True
    musicchoice=random.randint(1,2)
    if musicchoice == 1:
        pygame.mixer.music.load("gametrack1.ogg")
    if musicchoice == 2:
        pygame.mixer.music.load("gametrack2.ogg")
    pygame.mixer.music.play(-1)
    while paused:
        clock.tick(FPS)
        screen.fill((133,133,133))
        all_sprites.draw(screen)
        paused_text = fontTitle.render("Spacy", True, pygame.Color('white'))
        screen.blit(paused_text, paused_text.get_rect(center=(WIDTH/2, HEIGHT/2-120)))
        totalscore_text = fontSmall.render("Press any mouse button to start", True, pygame.Color('white'))
        screen.blit(totalscore_text, totalscore_text.get_rect(center=(WIDTH/2, HEIGHT/2)))
        shop_text = fontMedium.render("Shop (S)", True, pygame.Color('white'))
        screen.blit(shop_text, shop_text.get_rect(center=(WIDTH/2, HEIGHT/2+90)))
        paused_text2 = fontMedium.render("Exit (Q)", True, pygame.Color('white'))
        screen.blit(paused_text2, paused_text2.get_rect(center=(WIDTH/2, HEIGHT/2+140)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menusound.play()
                running = False
                paused = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menusound.play()
                    shop()
                if event.key == pygame.K_q:
                    menusound.play()
                    running = False
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                menusound.play()
                paused = False
        pygame.display.flip()
def pause():
    paused = True
    while paused:
        clock.tick(FPS)
        screen.fill((133,133,133))
        all_sprites.draw(screen)
        paused_text = fontTitle.render("Paused", True, pygame.Color('white'))
        screen.blit(paused_text, paused_text.get_rect(center=(WIDTH/2, HEIGHT/2-90)))
        totalscore_text = fontMedium.render("Total score: "+ str(totalscore), True, pygame.Color('white'))
        screen.blit(totalscore_text, totalscore_text.get_rect(center=(WIDTH/2, HEIGHT/2)))
        shop_text = fontMedium.render("Shop (S)", True, pygame.Color('white'))
        screen.blit(shop_text, shop_text.get_rect(center=(WIDTH/2, HEIGHT/2+90)))
        paused_text2 = fontMedium.render("Exit (Q)", True, pygame.Color('white'))
        screen.blit(paused_text2, paused_text2.get_rect(center=(WIDTH/2, HEIGHT/2+140)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menusound.play()
                running = False
                paused = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menusound.play()
                    shop()
                if event.key == pygame.K_q:
                    menusound.play()
                    running = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_ESCAPE:
                    menusound.play()
                    paused = False
        pygame.display.flip()
def shop():
    paused = True
    while paused:
        screen.fill((133,133,133))
        all_sprites.draw(screen)
        clock.tick(FPS)
        paused_text = fontTitle.render("Shop", True, pygame.Color('white'))
        screen.blit(paused_text, paused_text.get_rect(center=(WIDTH/2, 100)))
        totalscore_text = fontMedium.render("Total score: "+ str(totalscore), True, pygame.Color('white'))
        screen.blit(totalscore_text, totalscore_text.get_rect(center=(WIDTH/2, 200)))
        shop_text = fontMedium.render("Go Back (ESC)", True, pygame.Color('white'))
        screen.blit(shop_text, (WIDTH/2-100, HEIGHT-120))
        paused_text2 = fontMedium.render("Exit (Q)", True, pygame.Color('white'))
        screen.blit(paused_text2, (WIDTH/2-80, HEIGHT-70))
        # Items
        bulletPenetration_text = fontSmall.render(("1. Bullet penetration - Price: 1000 - Current level: "+str(bulletPenetration)), True, pygame.Color('white'))
        screen.blit(bulletPenetration_text, bulletPenetration_text.get_rect(center=(WIDTH/2, 300)))
        trippleBullet_text = fontSmall.render(("2. Tripple shoot - Price: 1000 - Current level: "+str(trippleBullet)), True, pygame.Color('white'))
        screen.blit(trippleBullet_text, trippleBullet_text.get_rect(center=(WIDTH/2, 350)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menusound.play()
                running = False
                paused = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menusound.play()
                if event.key == pygame.K_2:
                    menusound.play()
                if event.key == pygame.K_q:
                    menusound.play()
                    running = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_ESCAPE:
                    menusound.play()
                    paused = False
        pygame.display.flip()
def restart():
    waiting = True
    pygame.mixer_music.stop()
    gameOverSound.play()
    highscores.append(kills)
    if len(highscores) > 10:
        highscores.sort(reverse = True)
        highscores.pop()
    else:
        highscores.sort(reverse = True)
    while waiting:
        clock.tick(FPS)
        paused_text = fontLarge.render("You died!", True, pygame.Color('red'))
        screen.blit(paused_text, paused_text.get_rect(center=(WIDTH/2, 100)))
        paused_text2 = fontMedium.render("Restart (R)", True, pygame.Color('white'))
        screen.blit(paused_text2, paused_text2.get_rect(center=(WIDTH/2, 200)))
        paused_text3 = fontMedium.render("Exit (Q)", True, pygame.Color('white'))
        screen.blit(paused_text3, paused_text3.get_rect(center=(WIDTH/2, 250)))
        paused_text4 = fontMedium.render("Highscores", True, pygame.Color('white'))
        screen.blit(paused_text4, paused_text4.get_rect(center=(WIDTH/2, 350)))
        add = 0
        numbering = 1
        for stuff in highscores:
            highscore_text = fontSmall.render(str(numbering)+"# - "+str(stuff), True, pygame.Color('white'))
            screen.blit(highscore_text, highscore_text.get_rect(center=(WIDTH/2, 390+add)))
            add += 25
            numbering += 1
        all_sprites.empty()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menusound.play()
                waiting = False
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menusound.play()
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    menusound.play()
                    waiting = False
                    all_sprites.add(player)
                    for i in range(4):
                        m = Mob()
                        all_sprites.add(m)
                        mobs.add(m)
                pygame.mixer.stop()
                musicchoice=random.randint(1,2)
                if musicchoice == 1:
                    #pygame.mixer.music.load(path.join(snd_dir, "gametrack1.ogg"))
                    pygame.mixer.music.load("gametrack1.ogg")
                if musicchoice == 2:
                    #pygame.mixer.music.load(path.join(snd_dir, "gametrack2.ogg"))
                    pygame.mixer.music.load("gametrack2.ogg")
                pygame.mixer.music.play(-1)
        all_sprites.update()
        pygame.display.flip()
# Spawn stuff
all_sprites = pygame.sprite.Group()
metro = pygame.sprite.Group()
for i in range(0):
    me = Metro()
    all_sprites.add(me)
    metro.add(me)
mobs = pygame.sprite.Group()
for i in range(4):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# Game loop
gameOver = False
running = True
p = Player()
splash()
while running:
    if gameOver:
        restart()
        gameOver = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        metro = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        level = 1
        totalscore += kills
        kills = 0
        kills_c = 10
        diffcounter = 0
        for i in range(0):
            me = Metro()
            all_sprites.add(me)
            metro.add(me)
        for i in range(4):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

    clock.tick(FPS)
    pos = pygame.mouse.get_pos()

    # input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shot.play()
            player.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menusound.play()
                pause()
    if kills > kills_c:
        diffcounter +=1
        if diffcounter >= 10:
            diffcounter = 0
            for i in range(2):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
            level += 1
            oneUp.play()
            kills_c += 10
    # Update
    all_sprites.update()
    # Mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_mask)
    hits2 = pygame.sprite.spritecollide(player, metro, False, pygame.sprite.collide_mask)
    if hits or hits2:
        for hit in hits or hits2:
            expl = Explsion(hit.rect.center)
            all_sprites.add(expl)
            gameOver = True

    # Bullet hit mob
    hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits:
        expl = Explsion(hit.rect.center)
        all_sprites.add(expl)
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        hitSound.play()
        kills += 1
    font = pygame.font.Font(None, 40)
    fps = font.render("FPS: " + (str(int(clock.get_fps()))), True, pygame.Color('white'))
    kills_text = font.render("Score: " + (str(int(kills))), True, pygame.Color('white'))
    level_text = font.render("Level: " + (str(int(level))), True, pygame.Color('white'))
    esc_text = font.render("Pause (ESC)", True, pygame.Color('white'))

    # Draw
    screen.fill((133,133,133))
    all_sprites.draw(screen)
    screen.blit(fps, (WIDTH-130, 30))
    screen.blit(kills_text, kills_text.get_rect(center=(WIDTH-100, 70)))
    screen.blit(level_text, (WIDTH/2 - 48, 30))
    screen.blit(esc_text, (10, 10))

    # after drawing everything flip the display
    pygame.display.flip()

pygame.quit()
