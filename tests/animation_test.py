from os import path

def animations(mob,state,speed):
    import pygame
    
    pygame.init()
    screen = pygame.display.set_mode((200,200))
    allSprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    done = False
    textures = []
    for i in range(2):
        textures.append(pygame.transform.scale(pygame.image.load(path.join(imgDir,'{0}_{1}{2}.png'.format(mob,state,i+1))).convert_alpha(),(64,64)))

    class sprite(pygame.sprite.Sprite):
        def __init__(self,textures):
            pygame.sprite.Sprite.__init__(self)
            self.images = textures

            self.index = 0
            self.tick = 0
            self.image = self.images[self.index]
            self.rect = pygame.Rect(5,5,64,64)    
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
        screen.fill((0,0,0))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

while True:
    print("Czego animację mam wyświetlić?")
    mob = input()
    print("Jaki stan tej postaci mam wyświetlić?")
    state = input()

    imgDir = path.join(path.dirname(__file__),'../textures/mobs')

    animations(mob,state,1)
