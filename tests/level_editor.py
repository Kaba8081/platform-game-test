import pygame
from os import path

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640,448))
pygame.display.set_caption("Level editor")

clock = pygame.time.Clock()
allTiles = pygame.sprite.Group()
Font=pygame.font.SysFont("Arial", 12,bold=False,italic=False)

done = False
imgDir = path.join(path.join(path.join(path.dirname(__file__),'..'),'textures'),'ground')
textures = []
materials = ['dirt1','dirt2','player_spawn','enemy_spawner']
current_material = 'dirt1'
current_material_index = 0
coordinates_fix_x = 0
coordinates_fix_y = 0

for i in range(2):
    textures.append(pygame.image.load(path.join(imgDir,'dirt{0}.png'.format(i+1))))

terrain = []

for i in range(100):
    lista = []
    for j in range(100):
        lista.append('-')
    terrain.append(lista)

TILESIZE = 16

#   COLORS
BLACK = (0,0,0)
WHITE = (250,250,250)
RED = (250,0,0)
GREEN = (0,250,0)
BLUE = (0,0,250)
GRAY = (185,185,185)
LIGHTGREY = (100, 100, 100)

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,value,texture):
        pygame.sprite.Sprite.__init__(self)
        self.image  = pygame.Surface((16,16))
        if value == 'tile':
            self.image = texture
        elif value == 'spawner':
            self.image.fill(texture)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,direction,direction2):
        if direction == 'L':
            self.rect.left -= 16
        elif direction == 'R':
            self.rect.right += 16
        
        if direction2 == 'U':
            self.rect.bottom -= 16
        elif direction2 == 'D':
            self.rect.bottom += 16

def draw_grid():
    for x in range(0, 640, TILESIZE):
            pygame.draw.line(screen, LIGHTGREY, (x, 0), (x, 448))
    for y in range(0, 448, TILESIZE):
            pygame.draw.line(screen, LIGHTGREY, (0, y), (640, y))

while not done:
    directions = ['None','None']
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if coordinates_fix_x < 60:
                    directions[0] = "L"
                    coordinates_fix_x += 1
            elif event.key == pygame.K_RIGHT:
                if coordinates_fix_x > 0: 
                    directions[0] = "R"
                    coordinates_fix_x -= 1
            else:
                directions.append('None')
            if event.key == pygame.K_UP:
                if coordinates_fix_y < 72:
                    directions[1] = "U"
                    coordinates_fix_y += 1
            elif event.key == pygame.K_DOWN:
                if coordinates_fix_y > 0:
                    directions[1] = "D"
                    coordinates_fix_y -= 1
            else:
                directions.append('None')
            
            
            if event.key == pygame.K_o:
                if not current_material_index == 0:
                    current_material_index -= 1
                    current_material = materials[current_material_index]
            elif event.key == pygame.K_p:
                if not current_material_index == len(materials)-1:
                    current_material_index += 1
                    current_material = materials[current_material_index]
            
            if event.key == pygame.K_s:
                from tkinter import *
                from tkinter import ttk
                import pickle

                def save():
                    print(terrain)
                    file = open(path.join(path.join(path.dirname(__file__),'custom_levels'),nameVar.get()),'wb')
                    pickle.dump(terrain,file)

                root = Tk()
                root.title("Feet to Meters")

                mainframe = ttk.Frame(root, padding="3 3 12 12")
                mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
                mainframe.columnconfigure(0, weight=1)
                mainframe.rowconfigure(0, weight=1)

                nameVar = StringVar()
                nameEntry = ttk.Entry(mainframe, width=15, textvariable=nameVar)
                nameEntry.grid(column=0, row=1, sticky=(W, E))

                ttk.Button(mainframe, text="Zapisz", command=save).grid(column=0, row=2, sticky=W)

                ttk.Label(mainframe, text="Nazwa pliku:").grid(column=0, row=0, sticky=W)

                for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

                nameEntry.focus()
                root.bind('return', save)

                root.mainloop() 
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed, mouse_pos  = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
            if mouse_pressed[0]: # LPM
                if current_material_index != 2 and current_material_index != 3:
                    t = Tile(int(mouse_pos[0]/16)*16,int(mouse_pos[1]/16)*16,'tile',textures[current_material_index])
                    allTiles.add(t)
                    terrain[int(mouse_pos[0]/16)+coordinates_fix_x][int(mouse_pos[1]/16)+coordinates_fix_y] = current_material_index 
                else:
                    if current_material_index == 2 :
                        t = Tile(int(mouse_pos[0]/16)*16,int(mouse_pos[1]/16)*16,'spawner',GREEN)
                        allTiles.add(t)
                        terrain[int(mouse_pos[0]/16)+coordinates_fix_x][int(mouse_pos[1]/16)+coordinates_fix_y] = current_material_index
                    if current_material_index == 3:
                        t = Tile(int(mouse_pos[0]/16)*16,int(mouse_pos[1]/16)*16,'spawner',RED)
                        allTiles.add(t)
                        terrain[int(mouse_pos[0]/16)+coordinates_fix_x][int(mouse_pos[1]/16)+coordinates_fix_y] = current_material_index
            elif mouse_pressed[2]: # PPM
                terrain[int(mouse_pos[0]/16)+coordinates_fix_x][int(mouse_pos[1]/16)+coordinates_fix_y] = '-'
                for sprite in allTiles:
                    if sprite.rect.x == int(mouse_pos[0]/16)*16 and sprite.rect.y == int(mouse_pos[1]/16)*16:
                        sprite.kill()
    screen.fill(BLACK)
    draw_grid()
    allTiles.update(directions[0],directions[1])
    allTiles.draw(screen)
    label=Font.render('Building material: '+str(current_material),1,(168,168,168),(0,0,0))
    screen.blit(label,(10,10))
    #label=Font.render('Tile properties: ID - '+str(terrain[a][b])+'| '+str(structures[a][b]),1,(168,168,168),(0,0,0))
    #screen.blit(label,(470,22))
    pygame.display.flip()
    clock.tick(60)