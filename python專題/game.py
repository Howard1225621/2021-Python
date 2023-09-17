import pygame
import random
import os

FPS = 60

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

WIDTH = 700
HEIGHT = 490

#初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('')
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("python專題","picture","Ocean.jpg")).convert()
Player_img = pygame.image.load(os.path.join("python專題","picture","Fish.jpg")).convert()
Shark_img = pygame.image.load(os.path.join("python專題","picture","Sharkk.jpg")).convert()

def new_shark():
    shark = Shark()
    all_sprites.add(shark)
    sharks.add(shark)

def draw_health(surf, hp, x, y):
    if hp<0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect,2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Player_img,(50,40))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect() #把這個image框起來(定位)
        self.rect.centery = HEIGHT/2
        self.rect.left = 50
        self.speedx = 8
        self.health = 100

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedx
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        
class Shark(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Shark_img,(100,40))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect() #把這個image框起來(定位)
        self.rect.x = random.randrange(700,800)
        self.rect.y = random.randrange(0,HEIGHT-self.rect.height)  
        self.speedx = random.randrange(-10,-2)
        self.speedy = random.randrange(-3,3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(700,800)
            self.rect.y = random.randrange(0,HEIGHT-self.rect.height)  
            self.speedx = random.randrange(-10,-2)
            self.speedy = random.randrange(-3,3)

all_sprites = pygame.sprite.Group()
sharks = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_shark()

running = True

while running:
    clock.tick(FPS) #在一秒之內最多被執行60次
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    hits = pygame.sprite.spritecollide(player,sharks,True)
    for hit in hits:
        new_shark()
        player.health -= 10
        if player.health <= 0:
            running = False

    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_health(screen, player.health, 5, 10)
    pygame.display.update()
pygame.quit()
