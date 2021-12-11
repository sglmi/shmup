# classes for shmup game.

import pygame
import random
import os



def init():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
    pygame.display.set_caption('Shmup') # title of screen
    clock = pygame.time.Clock()
    return screen, clock

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(Window.FONT_NAME, size)
    text_surface = font.render(text, True, Color.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
# create a new mob
def new_mob(sprites, mobs):
    m = Mob()
    sprites.add(m)
    mobs.add(m)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        
def draw_shield_bar(surface, x, y, persent):
    if persent < 0:
        persent = 0
        
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (persent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, Color.GREEN, fill_rect)
    pygame.draw.rect(surface, Color.WHITE, outline_rect, 2)

# pygame window attribute
class Window:
    WIDTH = 480
    HEIGHT = 600
    FPS = 60
    FONT_NAME = pygame.font.match_font('DejaVuSans')


# Some predefined colors
class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


# All Images used in Game
class Image:
    init()
    IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'img')
    # Load all images
    BACKGROUND = pygame.image.load(os.path.join(IMAGE_DIR, 'starfield.png')).convert()

    BACKGROUND2 = pygame.image.load(os.path.join(IMAGE_DIR, 'purple.jpg')).convert()


    BACKGROUND_RECT = BACKGROUND.get_rect()
    BACKGROUND2_RECT = BACKGROUND2.get_rect()
    PLAYER = {
        "red": pygame.image.load(os.path.join(IMAGE_DIR, 'playerShip1_red.png')).convert(),
        "blue": pygame.image.load(os.path.join(IMAGE_DIR, 'playerShip1_blue.png')).convert(),
    }
    METEOR = pygame.image.load(os.path.join(IMAGE_DIR, 'meteorBrown_big1.png')).convert()
    BULLET = {
        "red": pygame.image.load(os.path.join(IMAGE_DIR, 'laserRed16.png')).convert(),
        "blue": pygame.image.load(os.path.join(IMAGE_DIR, 'laserBlue16.png')).convert(),
    }
    PLAYER_MINI = pygame.transform.scale(PLAYER.get("red"), (25, 19))
    PLAYER_MINI.set_colorkey(Color.BLACK)
    powerup = {
            'shield':pygame.image.load(os.path.join(IMAGE_DIR,'shield_gold.png')).convert(),
            'gun':pygame.image.load(os.path.join(IMAGE_DIR,'bolt_gold.png')).convert()
        }
    METEOR_LIST = ('meteorBrown_big1.png', 'meteorBrown_big2.png', 
                   'meteorBrown_med1.png','meteorBrown_med2.png', 
                   'meteorBrown_small1.png', 'meteorBrown_big2.png',
                   'meteorBrown_tiny1.png')
    meteor_images = []

    @staticmethod
    def meteors():
        Image.meteor_images = []
        for img in Image.METEOR_LIST:
            Image.meteor_images.append(
                    pygame.image.load(os.path.join(Image.IMAGE_DIR, img)).convert())

    explosion_anim = {'lg': [], 'sm': []}
    
    @staticmethod
    def explosions():
        Image.explosion_anim = {'lg': [], 'sm': [], 'player': []}
        for i in range(2):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(os.path.join(Image.IMAGE_DIR, filename)).convert()
            img.set_colorkey(Color.BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            Image.explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            Image.explosion_anim['sm'].append(img_sm)
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pygame.image.load(os.path.join(Image.IMAGE_DIR, filename)).convert()
            img.set_colorkey(Color.BLACK)
            Image.explosion_anim['player'].append(img)
    
            
        
class Sound:
    init()
    SOUND_DIR = os.path.join(os.path.dirname(__file__), 'snd')
    SHOOT = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'pew.wav'))
    PLAYER_DIE = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'sonic_expl.ogg'))
    pygame.mixer.music.load(os.path.join(SOUND_DIR, 'music.ogg'))
    pygame.mixer.music.set_volume(0.5)  # decrese the background music volume
    explosion_sounds = []
    

    @staticmethod
    def explosions():
        Sound.explosion_sounds = []
        for sound in ['exp1.wav', 'exp2.wav']:
            Sound.explosion_sounds.append(
                    pygame.mixer.Sound(os.path.join(Sound.SOUND_DIR, sound)))
        Sound.explosion_sounds[0].set_volume(.6)
        Sound.explosion_sounds[1].set_volume(.6)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, color="red"):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(Image.PLAYER.get(color), (50, 38))
        self.image.set_colorkey(Color.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20 
       #pygame.draw.circle(self.image, Color.RED, self.rect.center, self.radius)
        self.rect.centerx = Window.WIDTH / 2
        self.rect.bottom = Window.HEIGHT - 2
        self.speedx = 0
        self.speedy = 0
        self.score = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        
    def update(self):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = Window.WIDTH / 2
            self.rect.bottom = Window.HEIGHT - 10
        
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        
        if self.rect.right > Window.WIDTH:
            self.rect.right = Window.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
    def shoot(self, color="red"):
        bullet = Bullet(self.rect.centerx, self.rect.top, color)
        Sound.SHOOT.play()
        return bullet
    
    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (Window.WIDTH / 2, Window.HEIGHT + 200)
    
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

# Enemy
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super(Mob, self).__init__()
        # create path for meteors image path
        Image.meteors()
        self.image_orig = random.choice(Image.meteor_images)
        self.image_orig.set_colorkey(Color.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, Color.RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, Window.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 0:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.top > Window.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > Window.WIDTH + 20:
            self.rect.x = random.randrange(0, Window.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
    

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color="red"):
        super(Bullet, self).__init__()
        self.image = Image.BULLET.get(color)
        self.image.set_colorkey(Color.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy 
        # kill if it moves off the top of screen
        if self.rect.bottom < 0:
            self.kill()


# Power Up
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(['shield', 'gun'])
        self.image = Image.powerup[self.type]
        self.image.set_colorkey(Color.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5
        
    def update(self):
        self.rect.y += self.speedy 
        # kill if it moves off the top of screen
        if self.rect.top > Window.HEIGHT:
            self.kill()

# Explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        Image.explosions()
        self.size = size
        self.image = Image.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(Image.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = Image.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

        
