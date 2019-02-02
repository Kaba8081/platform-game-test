from os import path

def animations(mob,state,direction,background,speed):
    import pygame
    
    pygame.init()
    screen = pygame.display.set_mode((192,192))
    allSprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    done = False
    textures = []
    if direction == 'L':
        for i in range(2):
            textures.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'{0}_{1}{2}.png'.format(mob,state,i+1))).convert_alpha(),(64,64)))
    elif direction == 'R':
        for i in range(2):
            textures.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(imgDir,'{0}_{1}{2}.png'.format(mob,state,i+1))).convert_alpha(),(64,64)), True, False))
    
    class background_sprite(pygame.sprite.Sprite):
        def __init__(self,texture,x):
            pygame.sprite.Sprite.__init__(self)

            self.image = texture
            self.rect = pygame.Rect(x,136,64,64)

    background_color = (0,0,0)
    if background == '':
        pass
    elif background == 'overworld':
        background_color = (20, 198, 229)
        for i in range(3):
            bs = background_sprite(pygame.transform.scale(pygame.image.load(path.join(path.dirname(__file__),'../textures/ground/dirt2.png')).convert_alpha(),(64,64)),i*64)
            allSprites.add(bs)

    class sprite(pygame.sprite.Sprite):
        def __init__(self,textures):
            pygame.sprite.Sprite.__init__(self)
            self.images = textures

            self.index = 0
            self.tick = 0
            self.image = self.images[self.index]
            self.rect = pygame.Rect(72,72,64,64)    
        def update(self):
            if self.tick >= 61:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index] 
                self.tick = 0 
            self.tick += 1  

    s = sprite(textures)
    allSprites.add(s)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
                return
        screen.fill(background_color)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

while True:
    print("W jakim folderze jest ta animacja?")
    folder = input()

    imgDir = path.join(path.dirname(__file__),'../textures/'+folder)
    print("Czego animację mam wyświetlić?")
    mob = input()
    print("Jaki stan tej postaci mam wyświetlić?")
    state = input()
    print("W którą stronę postać ma się patrzyć? (L lub R)")
    direction = input()
    print("Jakie tło ma mieć symulacja? (dla oryginalnego, zostaw puste)")
    background = input()

    animations(mob,state,direction,background,1)
