import pygame 
from pygame import *
import random
import os
import time
import neat
import pickle
from pygame.locals import  *
pygame.font.init() 
pygame.mixer.init()
pygame.init()
win_height = 800
win_width = 600
suelo = 625
tamaño = 25

tiempo = pygame.time.get_ticks()
DIR = os.path.dirname(os.path.realpath(__file__))
IMGS_DIR = os.path.join(DIR, "imgs")
WIN = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('The God')
icono = pygame.image.load(os.path.join(IMGS_DIR, 'icono.ico'))
pygame.display.set_icon(icono)

dang_img = pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "dangling.png")).convert_alpha(), (80,80))
god_imgs = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR,"god" + str(x) + ".png" )).convert_alpha(), (80,80)) for x in range(1,4)]
bg_img = pygame.transform.scale(pygame.image.load(os  .path.join(IMGS_DIR, "bg.png")).convert(), (600,800))
surface_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"base.png")).convert_alpha())
surface1_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR, 'nubes.png')).convert_alpha())
ultimates_imgs = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "ulti" + str(x) + ".png")).convert_alpha(),(40,40)) for x in range(1,3)]
enem_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR, "enemigo.png")).convert_alpha())

def blitRotateCenter(surf, image, topleft, angle):
    """
    Rota una superficie para hacer que se anime como si se estuviera cayendo la imagen
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, dios, danglings, enemies,score,fps, surface1,surface2,evento):
    win.blit(bg_img, (0,0))
    for enemigo in enemies:
        enemigo.draw(win)
    for dang in danglings:
        dang.draw(win)
    score_label = pygame.font.SysFont("arial", 50).render("Puntuacion: " + str(score),1,(255,255,255))
    win.blit(score_label, (win_width - score_label.get_width() - 15, 10))
    fps_label = pygame.font.SysFont("arial", 50).render("FPS: "+ str(fps), True, (255,255,255))
    win.blit(fps_label,(win_width - fps_label.get_width() - 400, 10))
    surface1.draw(win)
    surface2.draw(win)
    dios.draw(win,evento)
    pygame.display.flip()

    
class God():
    """
    La clase God representa al Dios del juego
    
    """
    max_rotation = 25
    imgs = god_imgs
    rot_vel = 15
    ulti_imgs = ultimates_imgs
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.inclinar = 0 #Grados a inclinarse
        self.tick_count = 0
        self.tick_count2 = 0
        self.vel = 0
        self.height = self.y
        self.img = self.imgs[0]
        
    def fly(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self,evento):
        self.tick_count += 1
        #Formula del desplazamiento (fisica)
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
        # Vel. final
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        if displacement < 0:
            displacement -= 2
        self.y = self.y + displacement
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_SPACE:
                pygame.mixer.music.load('ki.wav')
                pygame.mixer.music.play(-1)
                if displacement <  0 or self.y < self.height + 50:
                    if self.inclinar < -90:
                        self.inclinar += self.rot_vel*2
                    if self.inclinar > -90:
                        self.inclinar -= self.rot_vel*2
        if displacement < 0 or self.y < self.height + 50:
                    if self.inclinar < self.max_rotation:
                        self.inclinar = self.max_rotation/4
        else: 
            if self.inclinar > -90:
                self.inclinar -= self.rot_vel
    def draw(self, win,evento):
        global tiempo
        self.elapsed = pygame.time.get_ticks() - tiempo
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if self.elapsed > 6000:
                    self.img = self.imgs[2]
        elif self.elapsed >4000:
            self.img = self.imgs[1]
        else:
            self.img = self.imgs[0]
        #Inclina la imagen
        blitRotateCenter(win, self.img, (self.x,self.y), self.inclinar)
        
    def get_mask(self):
        """
        consigue una mascara para la imagen actual del Dios
        
        
        """
        
        return pygame.mask.from_surface(self.img)

class Dangling():
    max_rotation = 25
    img = dang_img
    rot_vel = 20
    def __init__(self,x):
        self.x = x
        self.inclinar = 0 #Grados a inclinarse
        self.tick_count = 0
        self.vel = 0
        self.cruzar = False
        self.espacio = 600
        self.configuracion()
    def configuracion(self):
        self.height = random.randrange(100,450) 
    def move(self):
        self.vel = 10
        self.x = self.x - self.vel
    def draw(self,win):
        win.blit(self.img, (self.x, self.height))
    def get_mask(self):
        """
        consigue una mascara para la imagen actual del Dangling
        
        
        """
        return pygame.mask.from_surface(self.img)

class Enemies():
    vel = 15
    espacio = 350                      
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        
        # Donde se colocará el enemigo hacia arriba y hacia abajo
        self.top = 0
        self.bottom = 0
        
        self.enemy_top = pygame.transform.flip(enem_img, False, True)
        self.enemy_bottom = enem_img
        
        self.passed = False

        self.configurar_altura()
    def configurar_altura(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.enemy_top.get_height()
        self.bottom = self.height + self.espacio
    
    def move(self):
        self.x -= self.vel
        
    def draw(self,win):
        win.blit(self.enemy_top, (self.x, self.top))
        win.blit(self.enemy_bottom, (self.x, self.bottom))
    
    def colision(self, god, win):
        """
        Hace que devuelva el punto por el cual el god y dangling se chocaron con el enemigo
        
        """
        
        
        god_mask = god.get_mask()
        top_mask = pygame.mask.from_surface(self.enemy_top)
        bottom_mask = pygame.mask.from_surface(self.enemy_bottom)
        
        top_offset = (self.x - god.x, self.top - round(god.y))
        bottom_offset = (self.x - god.x, self.bottom - round(god.y))
        
        bottom_point = god_mask.overlap(bottom_mask, bottom_offset)
        top_point = god_mask.overlap(top_mask,top_offset)
        
        if bottom_point or top_point:
            return True

        return False
        
        
        
        
        
class Surface1:
    """
    Representa el movimiento en el suelo
    """
    vel = 5
    width = surface_img.get_width()
    img = surface_img

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

class Surface2:
    """
    Representa el movimiento en el suelo
    """
    vel = 5
    width = surface_img.get_width()
    img = surface1_img

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))
        



dios = God(100,300)
dangs = [Dangling(500)]
superficie = Surface1(suelo)
nubes = Surface2(tamaño)
enemigos = [Enemies(win_width)]     
run = True  
def main():    
    global WIN,run
    win = WIN
    score = 0  
    reloj = pygame.time.Clock()
    while run:
        reloj.tick(30)
        keys = pygame.key.get_pressed() 
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                run = False
        if keys[pygame.K_ESCAPE]:
            run = False
        if keys[pygame.K_SPACE]:
            dios.fly()
        rem1 = []
        rem2 = []
        add_enemigo = False
        add_dang = False
        for enemigo in enemigos:
            enemigo.move()
            # Si el dios choca contra el enemigo hace que se muera
            if enemigo.colision(dios,win):
                run = False
            if enemigo.x + enemigo.enemy_top.get_width() < 0:
                rem1.append(enemigo)
            if not enemigo.passed and enemigo.x < dios.x:
                enemigo.passed = True
                add_enemigo = True
        for dang in dangs:
            dang.move()
            if dang.x < 0:
                rem2.append(dang)
            if not dang.cruzar and dang.x < dios.x:
                dang.cruzar = True
                add_dang = True            
        if add_dang:
            dangs.append(Dangling(win_width))
        for r in rem2:
            dangs.remove(r)
        
        
        if add_enemigo:
            score += 1
            enemigos.append(Enemies(win_width)) 
        for r in rem1:
            enemigos.remove(r)
        if dios.y  >= suelo or dios.y < -50:
            run = False
        dios.move(evento)
        nubes.move()
        superficie.move()
        draw_window(win, dios, dangs,enemigos,score, round(reloj.get_fps()), superficie,nubes,evento)       
                    
if __name__ == '__main__':
    main()