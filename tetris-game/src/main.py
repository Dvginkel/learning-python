import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init()
vec = pygame.math.Vector2 # 2 for two dimensional

HEIGHT = 450
WIDTH = 450
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
        
        self.pos = vec(10, 360)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0
    
    def move(self):
        self.acc = vec(0,0.5)
        
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos
    
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15
    
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
                
    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)   
        if P1.vel.y > 0: 
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    
                
    

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH -100),
                                                random.randint(0, HEIGHT -30)))
        self.speed = random.randint(-1, 1)
        self.moving = True
        self.point = True
    
    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
    

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if(abs(platform.rect.top -entity.rect.bottom) < 50) and (abs(platform.rect.bottom - entity.rect.top) < 50):
                return True
        C = False
        
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50,100)
        C =  True
        while C:
            p = platform()    
            p.rect.center = (random.randrange(0,WIDTH - width), random.randrange(-50, 0))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
            

        
PT1 = platform()
P1 = Player()

PT1.moving = False
PT1.point = False

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT -10))

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

for x in range(random.randint(5,6)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
        
    platforms.add(pl)
    all_sprites.add(pl)
    
while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
        
        if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaySurface.fill((255,0,0))    
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                sys.exit()
                
    if P1.rect.top <= HEIGHT/ 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    
    plat_gen()
    displaySurface.fill((0,0,0))
    
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123,255,0))
    displaySurface.blit(g, (WIDTH/2, 10))
    
    for entity in all_sprites:
        displaySurface.blit(entity.surf, entity.rect)
        entity.move()
        
    
    pygame.display.update()
    FramePerSec.tick(FPS)
    