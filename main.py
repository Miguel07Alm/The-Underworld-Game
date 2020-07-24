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
pygame.display.set_caption('The UnderWorld')
icono = pygame.image.load(os.path.join(IMGS_DIR, 'icono.ico'))
pygame.display.set_icon(icono)
pygame.mixer.music.load('underworld.wav')
pygame.mixer.music.play(-1)

dangling = pygame.sprite.Sprite()
god = pygame.sprite.Sprite()
enemigo = pygame.sprite.Sprite()
ultimate_god = pygame.sprite.Sprite()
ultimate_dang = pygame.sprite.Sprite()


dangling.dang_img = pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "dangling.png")).convert_alpha(), (80,80))
god.god_imgs = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR,"god" + str(x) + ".png" )).convert_alpha(), (80,80)) for x in range(1,6)]
bg_img = pygame.transform.scale(pygame.image.load(os  .path.join(IMGS_DIR, "bg.png")).convert(), (600,800))
surface_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"base.png")).convert_alpha())
surface1_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR, 'nubes.png')).convert_alpha())
ultimate_god.ultimates_imgs = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "ulti" + str(x) + ".png")).convert_alpha(),(25,25)) for x in range(1,4)]
enemigo.enem_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR, "enemigo.png")).convert_alpha())
ultimate_dang.ultimate_img = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "ulti_dang.png")).convert_alpha(),(25,25))]
def blitRotateCenter(surf, image, topleft, angle):
    """
    Rota una superficie para hacer que se anime como si se estuviera cayendo la imagen
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
def blitRotateRight(surf, image, topright, angle):
    """
    Rota una superficie para hacer que se anime como si se estuviera cayendo la imagen
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topright = topright).center)

    surf.blit(rotated_image, new_rect.topright)
def draw_window(win, dios, danglings, ulti_dang,ulti_lista,enemies_top,enemies_bottom,ulti_god,score,fps, surface1,surface2,evento):
    win.blit(bg_img, (0,0))
    score_label = pygame.font.SysFont("arial", 50).render("Puntuacion: " + str(score),1,(255,255,255))
    fps_label = pygame.font.SysFont("arial", 40).render("FPS: "+ str(fps), 1, (255,255,255))
    ulti_label = pygame.font.SysFont("arial", 40).render("Ulti: " + str(ulti_lista),1,(0,0,0  ))
    surface1.draw(win)
    surface2.draw(win)
    for enemigo in enemies_top:
        enemigo.draw(win)
    for enemigo in enemies_bottom:
        enemigo.draw(win)
    for dang in danglings:
        dang.draw(win)
    for ulti_dang in ulti_dang:
        ulti_dang.draw(win)
    for ulti in ulti_god:
        ulti.draw(win, evento)      
    dios.draw(win,evento)
    win.blit(score_label, (win_width - score_label.get_width() - 15, 10))
    win.blit(fps_label,(0 , 10))
    win.blit(ulti_label,(125,10))
    pygame.display.flip()

    
class God(pygame.sprite.Sprite):
    """
    La clase God representa al Dios del juego
    
    """
    max_rotation = 25
    imgs = god.god_imgs
    rot_vel = 15
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.inclinar = 0 #Grados a inclinarse
        self.tick_count = 0
        self.vel = 0
        self.img = self.imgs[0]
        self.rect = self.img.get_rect()
        self.height = self.rect.y
        self.rect.x = x
        self.rect.y = y
    def fly(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.rect.y
    def move(self,evento):
        self.tick_count += 1
        #Formula del desplazamiento (fisica)
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
        # Vel. final
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        if displacement < 0:
            displacement -= 2
        self.rect.y = self.rect.y + displacement
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_SPACE:
                if displacement <  0 or self.rect.y < self.height + 50:
                    if self.inclinar < -90:
                        self.inclinar += self.rot_vel*2
                    if self.inclinar > -90:
                        self.inclinar -= self.rot_vel*2
        if displacement < 0 or self.rect.y < self.height + 50:
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
                if self.elapsed >= 6000 and self.elapsed <10000:
                    self.img = self.imgs[2]
                elif self.elapsed >=10000 and self.elapsed <15000:
                    self.img = self.imgs[3]
                elif self.elapsed >=15000:
                    self.img = self.imgs[4]
        elif self.elapsed >=4000 and self.elapsed <10000:
            self.img = self.imgs[1]
        elif self.elapsed >=10000 and self.elapsed <15000:
            self.img = self.imgs[2]
        elif self.elapsed >=15000:
            self.img = self.imgs[3]
        else:
            self.img = self.imgs[0]
        #Inclina la imagen
        blitRotateCenter(win, self.img, (self.rect.x,self.rect.y), self.inclinar)
        
    def get_mask(self):
        """
        consigue una mascara para la imagen actual del Dios
         
        """
        dios_mask = pygame.mask.from_surface(self.img)
        return dios_mask
class UltimateGod(pygame.sprite.Sprite):
    ulti_img = ultimate_god.ultimates_imgs
    rot_vel = 20
    max_rotation = 50
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.vel = 15
        self.inclinar = 0
        self.ulti_imgs = self.ulti_img[0]
        self.pasado = False
        self.tick_count = 0
        self.rect = self.ulti_imgs.get_rect()
        self.rect.x = dios.rect.x
        self.rect.y = dios.rect.y
    def move(self):
        self.tick_count += 1
        displacement = self.vel*(self.tick_count)+0.5*(3)*(self.tick_count)**2
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        if displacement < 0:
            displacement -= 2
        
        self.rect.x = self.rect.x + displacement
        if displacement < 0:  
            if self.inclinar < self.max_rotation:
                self.inclinar += self.max_rotation*5 
        else:  
            if self.inclinar > -90:
                self.inclinar += self.rot_vel
    def draw(self,win, evento):
        global tiempo 
        self.elapsed = pygame.time.get_ticks() - tiempo
        
        if self.elapsed >= 5000 and self.elapsed < 10000 :
            self.ulti_imgs = self.ulti_img[1] 
        elif self.elapsed >=10000:  
            self.ulti_imgs = self.ulti_img[2]
        else:
            self.ulti_imgs = self.ulti_img[0]
        #Inclina la imagen
        blitRotateRight(win, self.ulti_imgs, (self.rect.x,self.rect.y), self.inclinar)   
    def get_mask(self):
        """
        Extrae los bits de la imagen de la ulti
        """
        return pygame.mask.from_surface(self.ulti_imgs)
    def colision_dang(self, dang, win):
        """
        Hace que devuelva el punto por el cual el god y dangling se chocaron con el enemigo
        
        """
        dang_mask = dang.get_mask()
        ulti_mask = self.get_mask()
        ulti_offset = (self.rect.x - round(dang.rect.x), self.rect.y - dang.rect.height)
        
        c_point = dang_mask.overlap(ulti_mask, ulti_offset)
        
        
        
        if c_point:
            return True

        return False
class Dangling(pygame.sprite.Sprite):
    max_rotation = 25
    img = dangling.dang_img
    rot_vel = 20
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.inclinar = 0 #Grados a inclinarse
        self.tick_count = 0
        self.vel = 0
        self.cruzar = False
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.configuracion()
    def configuracion(self):
        self.rect.height = random.randrange(100,450) 
    def move(self):
        self.vel = 10
        self.rect.x = self.rect.x - self.vel
    def draw(self,win):
        win.blit(self.img, (self.rect.x, self.rect.height))
    def get_mask(self):
        """
        consigue una mascara para la imagen actual del Dangling
        
        
        """
        return pygame.mask.from_surface(self.img)
    def colision(self, god, win):
        """
        Hace que devuelva el punto por el cual el god y dangling se chocaron con el enemigo
        
        """
        god_mask = god.get_mask()
        dang_mask = self.get_mask()
        dang_offset = (self.rect.x - god.rect.x, self.rect.height - round(god.rect.y))
        
        c_point = god_mask.overlap(dang_mask, dang_offset)
        
        
        
        if c_point:
            return True

        return False
    
class UltimateDang(pygame.sprite.Sprite):
    ulti_img = ultimate_dang.ultimate_img
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ulti_imgs = self.ulti_img[0]
        self.vel = 20
        self.inclinar = 0
        self.pasado = False
        self.tick_count = 0
        self.rect = self.ulti_imgs.get_rect()
        for dang in dangs:
            self.rect.x = dang.rect.x
            self.rect.y = dang.rect.height
            
    def move(self):
        self.rect.x = self.rect.x - self.vel
    def draw(self,win):
        #Inclina la imagen
        win.blit(self.ulti_imgs, (self.rect.x,self.rect.y))   
    def get_mask(self):
        """
        Extrae los bits de la imagen de la ulti
        """ 
        return pygame.mask.from_surface(self.ulti_imgs)
    def colision_god(self, god, win):
        """
        Hace que devuelva el punto por el cual el god y dangling se chocaron con el enemigo
        
        """
        god_mask = god.get_mask()
        ulti_mask = self.get_mask()
        ulti_offset = (self.rect.x - god.rect.x, self.rect.y - round(god.rect.y))
        
        c_point = god_mask.overlap(ulti_mask, ulti_offset)
        
        
        
        if c_point:
            return True

        return False
class Enemies_Top(pygame.sprite.Sprite):
    vel = 15                      
    
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.height = 0
        
        # Donde se colocará el enemigo hacia arriba y hacia abajo
        self.top = 0
        self.enemy_top = pygame.transform.flip(enemigo.enem_img, False, True)
        self.rect = self.enemy_top.get_rect()
        self.passed = False

        self.configurar_altura()
    def configurar_altura(self):
        self.height = random.randrange(100,300)
        self.top = self.height - self.enemy_top.get_height()
    
    def move(self):
        self.x -= self.vel
        
    def draw(self,win):
        win.blit(self.enemy_top, (self.x, self.top))
    def colision_god(self, god, win):
        """
        Hace que devuelva el punto por el cual el god y dangling se chocaron con el enemigo
        
        """
        god_mask = god.get_mask()
        top_mask = pygame.mask.from_surface(self.enemy_top)
        top_offset = (self.x - god.rect.x, self.top - round(god.rect.y))
        
        top_point = god_mask.overlap(top_mask, top_offset)
        
        
        
        if top_point:
            return True

        return False
    def colision_ulti_top(self,ulti ,win):
        ulti_mask = ulti.get_mask()
        top_mask = pygame.mask.from_surface(self.enemy_top)
        
        
        top_offset = (self.x - round(ulti.rect.x), self.top - round(ulti.rect.y))
        
        top_point = ulti_mask.overlap(top_mask, top_offset)
        
        if top_point:
            return True

        return False
class Enemies_Bottom(pygame.sprite.Sprite):
    vel = 15
    espacio = 400
    
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.height = 0
        
        # Donde se colocará el enemigo hacia arriba y hacia abajo
        self.bottom = 0
        self.enemy_bottom = enemigo.enem_img
        self.rect = self.enemy_bottom.get_rect()
        self.passed = False

        self.configurar_altura()
    def configurar_altura(self):
        self.height = random.randrange(10,200)
        self.bottom = self.height + self.espacio
    
    def move(self):
        self.x -= self.vel
        
    def draw(self,win):
        win.blit(self.enemy_bottom, (self.x, self.bottom))
    def colision_god(self, god, win):
        """
        Hace que devuelva el punto por el cual el god y dangling se chocaron con el enemigo
        
        """
        god_mask = god.get_mask()
        bottom_mask = pygame.mask.from_surface(self.enemy_bottom)
        bottom_offset = (self.x - god.rect.x, self.bottom - round(god.rect.y))
        
        bottom_point = god_mask.overlap(bottom_mask, bottom_offset)
        
        
        
        if bottom_point:
            return True

        return False
    def colision_ulti_bottom(self,ulti,win):
        ulti_mask = ulti.get_mask()
        bottom_mask = pygame.mask.from_surface(self.enemy_bottom)
        
        
        bottom_offset = (self.x - round(ulti.rect.x), self.bottom - round(ulti.rect.y))
        
        bottom_point = ulti_mask.overlap(bottom_mask, bottom_offset)
        
        if bottom_point:
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
dangs = [Dangling(win_width)]
ulti_dang = [UltimateDang()]
superficie = Surface1(suelo)
nubes = Surface2(tamaño)
enemigos_top = [Enemies_Top(win_width)]
enemigos_bottom = [Enemies_Bottom(win_width)]     
ulti_god = [UltimateGod()]
run = True  

def main():    
    global WIN,run
    win = WIN
    score = 0  
    ulti_lista = ""
    opcion1 = "Press 1"
    opcion2 = "Activated"
    reloj = pygame.time.Clock()
    ulti_activada= False
    while run:
        reloj.tick(30)
        keys = pygame.key.get_pressed()
        eventos = pygame.event.get()
        for evento in eventos: 
            if evento.type == pygame.QUIT:
                run = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    ulti_activada= True
                if evento.key == pygame.K_SPACE:
                    dios.fly()
        if not(ulti_activada):
            ulti_lista = opcion1
        else:
            ulti_lista = opcion2
        if keys[pygame.K_ESCAPE]:
            run = False
        rem_top = []
        rem_bot = []
        rem2 = []
        rem3 = []
        rem4 = []
        add_ulti = False
        add_enemigo_top = False
        add_enemigo_bottom = False
        add_dang = False
        add_ulti_dang = False
        colision = False
        pasado_width = False
        colision_dang = False
        for ulti in ulti_god:              
            if ulti_activada:
                ulti.move() 
            else:
                ulti.rect.midleft = dios.rect.midright
            for dang in dangs:
                if ulti.colision_dang(dang,win):
                    dangs.clear()
                    ulti_dang.clear()
                    colision_dang = True
                    score += 1
            if ulti.rect.x > win_width:
                rem3.append(ulti)
            if not ulti.pasado and ulti.rect.x > win_width:
                ulti.pasado = True
                add_ulti = True
        if add_ulti:
            ulti_activada = False
            ulti_god.append(UltimateGod())
            
        for r in rem3:
            ulti_god.remove(r)
        superficie.move()                      
        for enemigo_top in enemigos_top:
            enemigo_top.move()
            for ulti in ulti_god:
                if enemigo_top.colision_ulti_top(ulti,win):
                    enemigos_top.clear()
                    colision = True
            # Si el dios choca contra el enemigo hace que se muera
            if enemigo_top.colision_god(dios,win):
                run = False
            if enemigo_top.x + enemigo_top.enemy_top.get_width() < 0:
                rem_top.append(enemigo_top)
                pasado_width = True
            if not enemigo_top.passed and enemigo_top.x < dios.rect.x:
                enemigo_top.passed = True
                add_enemigo_top = True
            if colision:
                add_enemigo_top= True
                
        for enemigo in enemigos_bottom:
            enemigo.move()
            for ulti in ulti_god:
                if enemigo.colision_ulti_bottom(ulti,win):
                    enemigos_bottom.clear()
                    colision = True
            # Si el dios choca contra el enemigo hace que se muera
            if enemigo.colision_god(dios,win):
                run = False
            if enemigo.x  + enemigo.enemy_bottom.get_height() < 0:
                rem_bot.append(enemigo)
                pasado_width = True
            if not enemigo.passed and enemigo.x < dios.rect.x:
                enemigo.passed = True
                add_enemigo_bottom = True 
            if colision:
                add_enemigo_bottom= True
        
        for dang in dangs:
            dang.move()
            if dang.colision(dios, win):
                run = False
            if dang.rect.x + dang.img.get_width() < 0:
                rem2.append(dang)
                add_dang = True
            if not dang.cruzar and dang.rect.x < 0:
                dang.cruzar = True     
        
        for ulti in ulti_dang:
            ulti.move()
            if ulti.colision_god(dios,win):
                score -= 1
            if ulti.rect.x > win_width:
                rem4.append(ulti)
            if not ulti.pasado and ulti.rect.x < 0:
                ulti.pasado = True
                add_ulti_dang = True
        
        if add_dang:
            dangs.append(Dangling(win_width)) 
            ulti_dang.append(UltimateDang())
        if colision_dang:
            dangs.append(Dangling(win_width)) 
            ulti_dang.append(UltimateDang())
        
        for r in rem4:
            ulti_dang.remove(r)
        
        for r in rem2:
            dangs.remove(r)
            
        if add_enemigo_top or add_enemigo_bottom:
            score += 1
        
        if pasado_width:
            enemigos_top.append(Enemies_Top(win_width))
            enemigos_bottom.append(Enemies_Bottom(win_width))
        
        if not pasado_width and len(enemigos_top) == 0 and len(enemigos_bottom) == 0:
            enemigos_bottom.append(Enemies_Bottom(win_width))
            enemigos_top.append(Enemies_Top(win_width))
        
        for r in rem_bot:
            enemigos_bottom.remove(r)  
        for i in rem_top:
            enemigos_top.remove(i)        
        
        if dios.rect.y + dios.img.get_height() - 10  >= suelo or dios.rect.y < -50:
            run = False
        dios.move(evento)
        nubes.move()
        draw_window(win, dios, dangs,ulti_dang,ulti_lista,enemigos_top,enemigos_bottom,ulti_god, score, round(reloj.get_fps()), superficie,nubes,evento)       
                    
if __name__ == '__main__':
    main()