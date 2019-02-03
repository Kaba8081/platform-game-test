import pygame
from os import path
import sys

pygame.init()
screen = pygame.display.set_mode((640,448))

# Textures

imgDir = path.join(path.join(path.dirname(__file__),'..'),'textures')

textures_ground = []
textures_player = []

textures_ground.append(pygame.transform.scale(pygame.image.load(path.join(path.dirname(__file__),'../textures/ground/dirt1.png')).convert_alpha(),(64,64)))
textures_ground.append(pygame.transform.scale(pygame.image.load(path.join(path.dirname(__file__),'../textures/ground/dirt2.png')).convert_alpha(),(64,64)))

# player_idle
for i in range(2):
    textures_player.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'player/player_idle{0}.png'.format(i+1))).convert_alpha(),(64,64)))
for i in range(1):  
    textures_player.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'player/player_crouching{0}.png'.format(i+1))).convert_alpha(),(64,64)))

# Other variables

done = False
allSprites = pygame.sprite.Group()
allTiles = pygame.sprite.Group()
clock = pygame.time.Clock()
background_color = (20, 198, 229)

class Tile(pygame.sprite.Sprite):
    def __init__(self,texture,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = texture
        self.rect = pygame.Rect(x,y,64,64)

class Player(pygame.sprite.Sprite):
    def __init__(self,textures,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = textures
        self.index_idle = 0
        self.tick_idle = 0
        self.facing = 'left'
        #self.image = self.images[self.index_idle]
        self.image_shown = self.images[self.index_idle]
        self.rect = pygame.Rect(x,y,64,64)
        self.crouching = 0
        self.speedx = 0
        self.speedy = 0    
    def update(self):
        # movement

        self.experience_gravity()
        self.gravity()

        keys = pygame.key.get_pressed()
        
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.speedx == 0:
                pass
            elif self.speedx > 0:
                self.speedx -= 0.5
            elif self.speedx < 0:
                self.speedx += 0.5
        else:
            if keys[pygame.K_a]:
                self.speedx = -5
            if keys[pygame.K_d]:
                self.speedx = 5
        if keys[pygame.K_w]:
            if self.speedy == 0:
                self.speedy -= 9
        if keys[pygame.K_s]:
            self.crouching = 1
            self.image_shown = self.images[2]
            self.tick_idle = 60
        else:
            self.crouching = 0

        # animations
        if self.speedx == 0 and self.speedy == 0 and self.crouching != 1:
            if self.tick_idle >= 61:
                self.index_idle += 1
                if self.index_idle >= 2:
                    self.index_idle = 0
                self.image_shown = self.images[self.index_idle] 
                self.tick_idle = 0 
            self.tick_idle += 1
        # image update
        if  keys[pygame.K_d]:
            self.facing = 'right'
        elif keys[pygame.K_a]:
            self.facing = 'left'
        
        if self.facing == 'left':
            self.image = self.image_shown
        elif self.facing == 'right':
            self.image = pygame.transform.flip(self.image_shown,True,False)
        
        # position update
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def gravity(self):
        for colliding_object in pygame.sprite.spritecollide(self, allTiles, False):
            if self.speedy > 0:
                self.rect.bottom = colliding_object.rect.top+1
                self.speedy = 0
            if self.speedy < 0:
                self.rect.top = colliding_object.rect.bottom-1
                self.speedy = 0
    
    def experience_gravity(self, gravity = .35):
        if self.speedy == 0:
            self.speedy = 1
        else:
            self.speedy += gravity
        
# placing sprites
p = Player(textures_player,100,100)
allSprites.add(p)

for i in range(10):
    for j in range(7):
        if j == 5:
            t = Tile(textures_ground[1],i*64,j*64)
            allSprites.add(t)
            allTiles.add(t)
        elif j == 6:
            t = Tile(textures_ground[0],i*64,j*64)
            allSprites.add(t)
            allTiles.add(t)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
            sys.exit()
    screen.fill(background_color)
    allSprites.update()
    allSprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)