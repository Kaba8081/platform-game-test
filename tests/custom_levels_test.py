import pygame
from os import path

pygame.init()

def show_level(level):
    HEIGHT, WIDTH = 448, 640
    screen = pygame.display.set_mode((640,448))

    done = False
    allSprites = pygame.sprite.Group()
    allTiles = pygame.sprite.Group()
    clock = pygame.time.Clock()
    background_color = (20, 198, 229)
    draw_debug_bool = False
    imgDir = path.join(path.join(path.dirname(__file__),'..'),'textures')

    textures_ground = []
    textures_player = []

    textures_ground.append(pygame.transform.scale(pygame.image.load(path.join(path.dirname(__file__),'../textures/ground/dirt1.png')).convert_alpha(),(64,64)))
    textures_ground.append(pygame.transform.scale(pygame.image.load(path.join(path.dirname(__file__),'../textures/ground/dirt2.png')).convert_alpha(),(64,64)))

    for i in range(2):
        textures_player.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'player/player_idle{0}.png'.format(i+1))).convert_alpha(),(64,64)))
    for i in range(1):  
        textures_player.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'player/player_crouching{0}.png'.format(i+1))).convert_alpha(),(64,64)))
    for i in range(1):
        textures_player.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'player/player_jumping{0}.png'.format(i+1))).convert_alpha(),(64,64)))
    for i in range(2):
        textures_player.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'player/player_running{0}.png'.format(i+1))).convert_alpha(),(64,64)))

    def draw_debug(p):
        p.draw_undergrid() # hitboxes of tiles under the player

        pygame.draw.line(screen, (0,0,255), (200, 0), (200, 448)) # screen sticking point
        pygame.draw.line(screen, (0,0,255), (440, 0), (440, 448))

        pygame.draw.line(screen, (0,255,0), (p.rect.left, p.rect.top),(p.rect.right, p.rect.top), 2) # player hitbox
        pygame.draw.line(screen, (0,255,0), (p.rect.left, p.rect.top),(p.rect.left, p.rect.bottom), 2)
        pygame.draw.line(screen, (0,255,0), (p.rect.right, p.rect.bottom),(p.rect.right, p.rect.top), 2)
        pygame.draw.line(screen, (0,255,0), (p.rect.right, p.rect.bottom),(p.rect.left, p.rect.bottom), 2)
        pygame.draw.line(screen, (0,255,0), (p.rect.right, p.rect.bottom),(p.rect.left, p.rect.top), 1)
        pygame.draw.line(screen, (0,255,0), (p.rect.left, p.rect.bottom),(p.rect.right, p.rect.top), 1)

    class Tile(pygame.sprite.Sprite):
        def __init__(self,value,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = textures_ground[int(value)]
            self.rect = pygame.Rect(x,y,64,64)

    class Player(pygame.sprite.Sprite):
        def __init__(self,textures,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.images = textures

            # animation configs
            self.index_idle = 0
            self.tick_idle = 0
            self.index_jump = 3
            self.tick_jump = 0
            self.index_run = 4
            self.tick_run = 0
            self.facing = 'left'
            self.image_shown = self.images[self.index_idle]

            self.rect = pygame.Rect(x,y,64,64)
            self.crouching = 0
            self.speedx = 0
            self.speedy = 0 
            self.colliding_x = False  

        def update(self):
            # movement

            self.colliding_x = False
            self.experience_gravity()
            self.gravity()
            self.collidex()

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
                    self.tick_idle = 59
                    self.index_idle = 1
                if keys[pygame.K_d]:
                    self.speedx = 5
                    self.tick_idle = 59
                    self.index_idle = 1

            if keys[pygame.K_w]:
                if self.speedy == 0:
                    if self.jump():
                        self.speedy -= 9
                    #self.gravity()
                self.image = self.images[0]
                self.tick_idle = 59
                self.index_idle = 1
                self.crouching = 0

            if keys[pygame.K_s]:
                self.crouching = 1

            else:
                self.crouching = 0

            # animations

            if self.speedy != 0:
                if self.tick_jump >= 30:
                    self.index_jump += 1
                    if self.index_jump > 3:
                        self.index_jump = 3
                    self.image_shown = self.images[self.index_jump]
                    self.tick_jump = 0
                self.tick_jump += 1
            if self.speedx != 0 and self.speedy == 0:
                if self.tick_run > 10:
                    self.index_run += 1
                    if self.index_run > 5:
                        self.index_run = 4
                    self.image_shown = self.images[self.index_run]
                    self.tick_run = 0
                self.tick_run += 1
            if self.speedx == 0 and self.speedy == 0 and self.crouching != 1:
                if self.tick_idle >= 60:
                    self.index_idle += 1
                    if self.index_idle >= 2:
                        self.index_idle = 0
                    self.image_shown = self.images[self.index_idle] 
                    self.tick_idle = 0 
                self.tick_idle += 1
            if self.crouching == 1 and not keys[pygame.K_w]:
                self.image_shown = self.images[2]
                self.tick_idle = 59
                self.index_idle = 1

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

            self.rect.y += self.speedy
            self.rect.x += self.speedx

        def gravity(self):
            for colliding_object in pygame.sprite.spritecollide(self, allTiles, False):
                if abs(colliding_object.rect.centerx - self.rect.centerx) <= 64: #and abs(colliding_object.rect.centery - self.rect.centery) <= 33:
                    if self.speedy > 0 and self.speedx == 0:
                        self.rect.bottom = colliding_object.rect.top + 1
                        self.speedy = 0
                    elif self.speedy < 0 and self.speedx == 0:
                        self.rect.top = colliding_object.rect.bottom + 1
                        self.speedy = 0
                    else:
                        self.speedy = 0

        def jump(self):
            for tile in allTiles:
                if abs(self.rect.centerx - tile.rect.centerx) <= 64:
                    if abs(self.rect.centery - tile.rect.centery) <= 32:
                        return 0
            return 1
        def experience_gravity(self, gravity = .35):
            if self.speedy == 0:
                self.speedy = 1
            else:
                self.speedy += gravity

        def collidex(self):
            for colliding_object in pygame.sprite.spritecollide(self, allTiles, False):
                self.colliding_x = True
                if abs(colliding_object.rect.centery - self.rect.centery) <= 16: #and abs(colliding_object.rect.centerx - self.rect.centerx) <= 16:
                    if self.speedx > 0:
                        self.rect.right = colliding_object.rect.left - 2
                        self.speedx = 0
                    if self.speedx < 0:
                        self.rect.left = colliding_object.rect.right + 2
                        self.speedx = 0

        def draw_undergrid(self):
            for p in allTiles:
                if abs(p.rect.centerx - self.rect.centerx) <= 64:
                    pygame.draw.line(screen, (255,0,0), (p.rect.left, p.rect.top),(p.rect.right, p.rect.top),3)
                    pygame.draw.line(screen, (255,0,0), (p.rect.left, p.rect.top),(p.rect.left, p.rect.bottom),3)
                    pygame.draw.line(screen, (255,0,0), (p.rect.right, p.rect.bottom),(p.rect.right, p.rect.top),3)
                    pygame.draw.line(screen, (255,0,0), (p.rect.right, p.rect.bottom),(p.rect.left, p.rect.bottom),3)
                if abs(p.rect.centery - self.rect.centery) <= 16:#48 or abs(p.rect.centery - self.rect.centery) >= -48:
                    pygame.draw.line(screen, (255,0,0), (p.rect.left, p.rect.top),(p.rect.right, p.rect.top),3)
                    pygame.draw.line(screen, (255,0,0), (p.rect.left, p.rect.top),(p.rect.left, p.rect.bottom),3)
                    pygame.draw.line(screen, (255,0,0), (p.rect.right, p.rect.bottom),(p.rect.right, p.rect.top),3)
                    pygame.draw.line(screen, (255,0,0), (p.rect.right, p.rect.bottom),(p.rect.left, p.rect.bottom),3)

    for i in range(len(level)):
        for j in range(len(level[0])):
            if level[i][j] == '-':
                pass
            else:
                if int(level[i][j]) == 2:
                    p = Player(textures_player,i*64,j*64)
                    allSprites.add(p)
                elif int(level[i][j]) == 3:
                    pass
                else:
                    t = Tile(level[i][j],i*64,j*64)
                    allSprites.add(t)
                    allTiles.add(t)
    while True:
        if p.rect.centerx > 320:
            for sprite in allSprites:
                sprite.rect.centerx -= 16
        elif p.rect.centerx < 320:
            for sprite in allSprites:
                sprite.rect.centerx += 16
        elif p.rect.centery > 320:
            for sprite in allSprites:
                sprite.rect.centery -= 16
        elif p.rect.centery < 320:
            for sprite in allSprites:
                sprite.rect.centery += 16
        else:
            break

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    draw_debug_bool = not draw_debug_bool

        if not p.colliding_x:
            if p.rect.centerx > 200 and p.rect.centerx < 440:
                for platform in allTiles:
                    platform.rect.x += -int(p.speedx / 1.7)
            else:
                for platform in allTiles:
                    platform.rect.x += -p.speedx
                p.rect.x += -p.speedx   

        for platform in allTiles:
            platform.rect.y += -p.speedy

        if p.rect.centery < 280:
            for tile in allSprites:
                tile.rect.y += 1
        elif p.rect.centery > 280: 
            for tile in allSprites:
                tile.rect.y += -1

        if p.rect.centerx < 200:
            for tile in allSprites:
                tile.rect.x += 5
        elif p.rect.centerx > 440:
            for tile in allSprites:
                tile.rect.x -= 5
        
        screen.fill(background_color)
        allSprites.update()
        allSprites.draw(screen)

        if draw_debug_bool:
            draw_debug(p)

        pygame.display.flip()
        clock.tick(60)

import pickle
level_name = input("Poziom: ")
with open(path.join(path.join(path.dirname(__file__),'custom_levels'),level_name),'rb')as file:
    level = pickle.load(file)
    show_level(level)