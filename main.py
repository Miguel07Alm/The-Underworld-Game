import pygame 
from pygame import *
import random
import os
import time
import neat
import pickle
from pygame.locals import  *
import visualize
import graphviz

pygame.font.init() 
pygame.mixer.pre_init(16500, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

win_height = 800
win_width = 600
suelo = 625
tamaño = 25
menu_setting = True
GEN_LINES = False
score = 0 

tiempo = pygame.time.get_ticks()

DIR = os.path.dirname(os.path.realpath(__file__))
IMGS_DIR = os.path.join(DIR, "imgs")

WIN = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('The UnderWorld')
icono = pygame.image.load(os.path.join(IMGS_DIR, 'icono.ico'))
pygame.display.set_icon(icono)



dangling = pygame.sprite.Sprite()
god = pygame.sprite.Sprite()
enemigo = pygame.sprite.Sprite()
ultimate_god = pygame.sprite.Sprite()
ultimate_dang = pygame.sprite.Sprite()

#The png images of the game 
dangling.dang_img = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "dangling" + str(x) + ".png")).convert_alpha(), (80,80)) for x in range(1,3)]
god.god_imgs = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR,"god" + str(x) + ".png" )).convert_alpha(), (80,80)) for x in range(1,10)]
bg_img = pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "bg.png")).convert(), (600,800))
menu_bg = pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "menu_bg.png")).convert(), (600,800))
instructions_bg = pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "instructions_bg.png")).convert(), (600,800))
surface_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"base.png")).convert_alpha())
surface1_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR, 'nubes.png')).convert_alpha())
ultimate_god.ultimates_imgs = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "ulti" + str(x) + ".png")).convert_alpha(),(25,25)) for x in range(1,4)]
enemigo.enem_img = pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR, "enemigo.png")).convert_alpha())
ultimate_dang.ultimate_img = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "ulti_dang.png")).convert_alpha(),(25,25))]

ultimate_god.ultimates_foto = [pygame.transform.scale(pygame.image.load(os.path.join(IMGS_DIR, "ulti" + str(x) + ".png")).convert_alpha(),(50,50)) for x in range(1,4)]

gen = 0
instructions = True



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
def draw_window(win,dios, danglings, ulti_dang,ulti_foto,ulti_lista,enemies_top,enemies_bottom,ulti_god,score,fps, surface1,surface2,evento):
    win.blit(bg_img, (0,0))
    score_label = pygame.font.SysFont("arial", 50).render("Score: " + str(score),1,(255,255,255))
    fps_label = pygame.font.SysFont("arial", 40).render("FPS: "+ str(fps), 1, (255,255,255))
    ulti_label = pygame.font.SysFont("arial", 40).render(" :" + str(ulti_lista),1,(0,0,0 ))
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
        ulti.draw(win)     
    for ulti in ulti_foto:
        ulti.draw(win)
    for god in dios:        
        god.draw(win,evento)
    win.blit(score_label, (win_width - score_label.get_width() - 15, 10))
    win.blit(fps_label,(0 , 10))
    win.blit(ulti_label,(235,10))
    pygame.display.flip()

def draw_window_AI(win,gen, dios, danglings, ulti_dang, enemies,ulti_god,score,fps, surface1,surface2, enem_ind, dang_ind):
    if gen== 0:
        gen = 1
    
    if not menu_setting:
        
        win.blit(bg_img, (0,0))
        score_label = pygame.font.SysFont("arial", 50).render("Score: " + str(score),1,(255,255,255))
        fps_label = pygame.font.SysFont("arial", 40).render("FPS: "+ str(fps), 1, (255,255,255))
        surface1.draw(win)
        surface2.draw(win)
        for enemigo in enemies:
            enemigo.draw(win)
        for dang in danglings:
            dang.draw(win)
        for ulti_dang in ulti_dang:
            ulti_dang.draw(win)
        for ulti in ulti_god:
            ulti.draw(win)     
        for god in dios:
            if GEN_LINES:
                try:
                    pygame.draw.line(win, (110,255,51), (god.rect.x+ god.img.get_width()/2, god.rect.y + god.img.get_height()/2), (enemies[enem_ind].x + enemies[enem_ind].enemy_top.get_width()/2, enemies[enem_ind].height), 5)
                    pygame.draw.line(win, (110,255,51), (god.rect.x+ god.img.get_width()/2, god.rect.y + god.img.get_height()/2), (enemies[enem_ind].x + enemies[enem_ind].enemy_bottom.get_width()/2, enemies[enem_ind].bottom), 5)
                    pygame.draw.line(win,(110,255,51), (god.rect.x + god.img.get_width()/2, god.rect.y + god.img.get_height()/2),(dangs[dang_ind].rect.x + dangs[dang_ind].img.get_width()/2, dangs[dang_ind].rect.x), 5)
                except:
                    pass            
            god.draw(win)
            
        gen_label = pygame.font.SysFont("arial",40).render("Gens: " + str(gen),1,(255,255,255))
        win.blit(gen_label, (0, 40))
        alive_label = pygame.font.SysFont("arial",40).render("Alive: " + str(len(dios)),1,(255,255,255))
        win.blit(alive_label, (0, 75))
        
        
        win.blit(score_label, (win_width - score_label.get_width() - 15, 10))
        win.blit(fps_label,(0 , 10))
        
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
        self.elapsed = 0
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
        global tiempo, score
        if score > 0:
            self.elapsed = pygame.time.get_ticks() - tiempo
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if self.elapsed >= 4000 and self.elapsed <8000 and score > 0:
                    self.img = self.imgs[1]
                elif self.elapsed >=8000 and self.elapsed <12000 and score > 0:
                    self.img = self.imgs[2]
                elif self.elapsed >=12000 and self.elapsed < 16000 and score > 0:
                    self.img = self.imgs[3]
                elif self.elapsed >=16000 and self.elapsed < 20000 and score > 0:
                    self.img = self.imgs[4]
                elif score >= 30:
                    self.img = self.imgs[8]
                elif score >= 50:
                    self.img = self.imgs[6]
        elif self.elapsed >=0 and self.elapsed < 2000 and score > 0:
            self.img = self.imgs[0]
        elif self.elapsed >=2000 and self.elapsed <  4000 and score > 0:
            self.img = self.imgs[1]
        elif self.elapsed >=4000 and self.elapsed < 8000 and score > 0:
            self.img = self.imgs[2]
        elif self.elapsed >=8000  and score > 0:
            self.img = self.imgs[3]
        if score >= 30 and self.elapsed >=15000:
            self.img = self.imgs[7]
        if score >=50 and self.elapsed >= 25000:
            self.img = self.imgs[6]
        #Inclina la imagen
        blitRotateCenter(win, self.img, (self.rect.x,self.rect.y), self.inclinar)
        
    def get_mask(self):
        """
        consigue una mascara para la imagen actual del Dios
         
        """
        dios_mask = pygame.mask.from_surface(self.img)
        return dios_mask
class God_AI(pygame.sprite.Sprite):
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
        self.img_count = 0
        self.vel = 0
        self.elapsed = 0
        self.__num_random = random.randint(0,8)
        self.img = self.imgs[0]
        self.rect = self.img.get_rect()
        self.height = self.rect.y
        self.rect.x = x
        self.rect.y = y
    def fly(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.rect.y
    def move(self):
        self.tick_count += 1
        #Formula del desplazamiento (fisica)
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
        # Vel. final
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        if displacement < 0:
            displacement -= 2
        self.rect.y = self.rect.y + displacement
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
    def draw(self, win):
        global tiempo, score
        if score >0:
            self.elapsed = pygame.time.get_ticks() - tiempo
        if self.__num_random == 0 or self.__num_random == 1 or self.__num_random == 2 or self.__num_random == 3 or self.__num_random == 4 :
            if self.elapsed >= 4000 and self.elapsed < 8000 and score > 0:
                self.img = self.imgs[1]
            elif self.elapsed >= 8000 and self.elapsed < 12000 and score > 0:
                self.img = self.imgs[2]
            elif self.elapsed >= 12000 and self.elapsed < 16000 and score > 0:
                self.img = self.imgs[3]
            elif self.elapsed >= 16000 and score > 0:
                self.img = self.imgs[4]
                
            else:
                self.img = self.imgs[0]
        elif self.__num_random == 5:
            self.img = self.imgs[5]
        elif self.__num_random == 6:
            self.img = self.imgs[6]
        elif self.__num_random == 7:
            self.img = self.imgs[7]
            if score >10 and self.elapsed >= 25000:
                self.img = self.imgs[8]
        
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
        self.elapsed = 0
        self.rect = self.ulti_imgs.get_rect()
        for god in dios:    
            self.rect.x = god.rect.x
            self.rect.y = god.rect.y
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
    def draw(self,win):
        global tiempo, score
        if score > 0:
            self.elapsed = pygame.time.get_ticks() - tiempo
        if self.elapsed >= 0 and self.elapsed < 5000 and score >0 :
            self.ulti_imgs = self.ulti_img[0]
        elif score >5:
            self.ulti_imgs = self.ulti_img[1] 
        elif score >= 15 and self.elapsed >= 10000:  
            self.ulti_imgs = self.ulti_img[2]
        
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
    
class UltimateGod_AI(pygame.sprite.Sprite):
    ulti_img = ultimate_god.ultimates_imgs
    rot_vel = 20
    max_rotation = 50
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.vel = 15
        self.inclinar = 0
        self.ulti_imgs = self.ulti_img[0]
        self.pasado = False
        self.elapsed = 0
        self.tick_count = 0
        self.rect = self.ulti_imgs.get_rect()
        for god in GODS:    
            self.rect.x = god.rect.x
            self.rect.y = god.rect.y
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
    def draw(self,win):
        global tiempo, score 
        if score > 0:
            self.elapsed = pygame.time.get_ticks() - tiempo
        if self.elapsed >= 0 and self.elapsed < 5000 and score >0 :
            self.ulti_imgs = self.ulti_img[0]
        elif score >=5 and score <15:
            self.ulti_imgs = self.ulti_img[1] 
        elif score >= 15 and self.elapsed >= 10000:  
            self.ulti_imgs = self.ulti_img[2]
        
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
    
class Ultimate_foto(pygame.sprite.Sprite):
    ulti_img = ultimate_god.ultimates_foto
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ulti_imgs = self.ulti_img[0]
        self.rect = self.ulti_imgs.get_rect()
        self.rect.x = 200
        self.rect.y = 10
        self.elapsed = 0
    def draw(self,win):
        global tiempo, score        
        if score > 0:
            self.elapsed = pygame.time.get_ticks() - tiempo
        if self.elapsed >= 0 and self.elapsed < 5000 and score >0 :
            self.ulti_imgs = self.ulti_img[0]
        elif score >5:
            self.ulti_imgs = self.ulti_img[1] 
        elif score >= 15 and self.elapsed >= 10000:  
            self.ulti_imgs = self.ulti_img[2]
        
        #Inclina la imagen
        win.blit(self.ulti_imgs, (self.rect.x,self.rect.y))   
class Dangling(pygame.sprite.Sprite):
    max_rotation = 25
    imgs = dangling.dang_img
    rot_vel = 20
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.inclinar = 0 #Grados a inclinarse
        self.tick_count = 0
        self.vel = 0
        self.cruzar = False
        self.img = self.imgs[0]
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.configuracion()
    def configuracion(self):
        self.rect.height = random.randrange(100,450) 
    def move(self):
        self.vel = 10
        self.rect.x = self.rect.x - self.vel
    def draw(self,win):
        global score, tiempo
        self.elapsed = pygame.time.get_ticks() - tiempo
        if score >= 20 and self.elapsed > 10000:
            self.img = self.imgs[1]
        else:
            self.img = self.imgs[0]
        
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

class Enemies_AI(pygame.sprite.Sprite):
    vel = 15
    espacio = 250
    
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.height = 0
        
        # Donde se colocará el enemigo hacia arriba y hacia abajo
        self.bottom = 0
        self.top = 0
        self.enemy_bottom = enemigo.enem_img
        self.enemy_top = pygame.transform.flip(enemigo.enem_img, False, True)
        self.rect = self.enemy_bottom.get_rect()
        self.passed = False

        self.height_setting()
    def height_setting(self):
        self.height = random.randrange(75,450)
        self.bottom = self.height + self.espacio
        self.top = self.height - self.enemy_top.get_height()
    
    def move(self):
        self.x -= self.vel
        
    def draw(self,win):
        win.blit(self.enemy_bottom, (self.x, self.bottom))
        win.blit(self.enemy_top, (self.x, self.top))
    def colision_god(self, god, win):
        """
        Hace que devuelva el punto por el cual el god y dangling se chocaron con el enemigo
        
        """
        god_mask = god.get_mask()
        top_mask = pygame.mask.from_surface(self.enemy_top)
        top_offset = (self.x - god.rect.x, self.top - round(god.rect.y))
            
        top_point = god_mask.overlap(top_mask, top_offset)
        bottom_mask = pygame.mask.from_surface(self.enemy_bottom)
        bottom_offset = (self.x - god.rect.x, self.bottom - round(god.rect.y))
            
        bottom_point = god_mask.overlap(bottom_mask, bottom_offset)
            
        if bottom_point or top_point:
            return True

        return False
    def colision_ulti(self,ulti,win):
        ulti_mask = ulti.get_mask()
        bottom_mask = pygame.mask.from_surface(self.enemy_bottom)
        top_mask = pygame.mask.from_surface(self.enemy_top)
        
        
        top_offset = (self.x - round(ulti.rect.x), self.top - round(ulti.rect.y))
        
        top_point = ulti_mask.overlap(top_mask, top_offset)
        
        bottom_offset = (self.x - round(ulti.rect.x), self.bottom - round(ulti.rect.y))
        
        bottom_point = ulti_mask.overlap(bottom_mask, bottom_offset)
        
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
                       
dios = [God(100,300)]
GODS = []

dangs = [Dangling(win_width)]
ulti_dang = [UltimateDang()]
superficie = Surface1(suelo)
nubes = Surface2(tamaño)
enemigos_top = [Enemies_Top(win_width)]
enemigos_bottom = [Enemies_Bottom(win_width)]     
ulti_god = [UltimateGod()]
ulti_foto = [Ultimate_foto()]
run = True  

run_AI = False
def eval_genomes(genomes, config):
    global WIN, run, menu_setting, run_AI, gen, GODS,score
    win = WIN
    # Creation of a list when it contains the nets of the neural network and the genome for holding itself
    gen += 1
    nets = []
    ge = []
    
    # Creation of the gods object that can manage the neural network
    GODS = GODS
    ULTI_GOD = []
    for genome_id, genome in genomes:
        genome.fitness = 0 # Level of fitness
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        GODS.append(God_AI(100,300))
        ge.append(genome)
    

    enemies_AI = [Enemies_AI(win_width)]
    ULTI_GOD = [UltimateGod_AI()]
    enem_killed = 0
    activated_ulti = False
    clock = pygame.time.Clock()
    score = 0
    while run_AI and len(GODS) > 0:
        clock.tick(30)
        events = pygame.event.get()
        for evento in events:
            if evento.type == pygame.QUIT:
                run_AI = False
                pygame.quit()
                break
        enem_ind = 0
        dang_ind = 0
        
        add_ulti = False
        add_enemy = False
        add_dang = False
        add_ulti_dang = False
        colision = False
        pasado_width = False
        colision_dang = False
        special_attack = False
        rem_ulti_god = []
        if len(GODS) > 0:
            if len(enemies_AI) > 1 and GODS[0].x > enemies_AI[0].x + enemies_AI[0].enemy_top.get_width():# If use the first or second
                enem_ind = 1
                    
            if len(dangs) > 1 and GODS[0].rect.x > dangs[0].x + dangs[0].img.get_width():
                dang_ind = 1
              
         
        for x, god in enumerate(GODS):
            ge[x].fitness += 0.1
            god.move()
            output1 = nets[GODS.index(god)].activate((god.rect.y, abs(god.rect.y - enemies_AI[enem_ind].height), abs(god.rect.y - enemies_AI[enem_ind].bottom)))

            if output1[0] > 0.5:
                god.fly()
            output2 = nets[GODS.index(god)].activate((god.rect.y, abs(god.rect.y - dangs[dang_ind].rect.height), abs(god.rect.y - dangs[dang_ind].rect.x)))
            if output2[0] > 0.5:
                god.fly()
        for ulti in ULTI_GOD:     
            if output2[0] > -0.5 or output1[0] > 0.5:
                activated_ulti = True
            if activated_ulti:
                ulti.move()
            else:
                for god in GODS:
                    ulti.rect.midleft = god.rect.midright
        superficie.move()
        nubes.move()
        
        rem_enem = []
        rem_dangs = []
        rem_ulti_dang = []
        for ulti in ULTI_GOD:              
            for dang in dangs:
                if ulti.colision_dang(dang,win):
                    dangs.clear()
                    ulti_dang.clear()
                    colision_dang = True
            if ulti.rect.x > win_width:
                rem_ulti_god.append(ulti)
            if not ulti.pasado and ulti.rect.x > win_width:
                ulti.pasado = True
                add_ulti = True
        if add_ulti:
            ULTI_GOD.append(UltimateGod_AI())  
            
        for ulti in ulti_dang:
            ulti.move()
            for god in GODS:    
                if ulti.colision_god(god,win):
                    for genome in ge:
                        genome.fitness -= 1
            
            if ulti.rect.x > win_width:
                rem_ulti_dang.append(ulti)
            if not ulti.pasado and ulti.rect.x < 0:
                ulti.pasado = True
                add_ulti_dang = True   
        if add_dang:
            dangs.append(Dangling(win_width)) 
            ulti_dang.append(UltimateDang())
        if colision_dang:
            score += 1
            for genome in ge:
                genome.fitness += 5
            enem_killed += 1
            
        for enemy in enemies_AI:
            enemy.move()
            for god in GODS:
                if enemy.colision_god(god, win):
                    ge[GODS.index(god)].fitness -= 1
                    nets.pop(GODS.index(god))
                    ge.pop(GODS.index(god))
                    GODS.pop(GODS.index(god))
            
            
            for ulti in ULTI_GOD:
                if enemy.colision_ulti(ulti,win):
                    enemies_AI.clear()
                    colision = True
            # Si el dios choca contra el enemigo hace que se muera
            for god in GODS:    
                if enemy.colision_god(god,win):
                    ge[GODS.index(god)].fitness -= 1
                    nets.pop(GODS.index(god))
                    ge.pop(GODS.index(god))
                    GODS.pop(GODS.index(god))
            if enemy.x + enemy.enemy_top.get_width() < 0:
                rem_enem.append(enemy)
                pasado_width = True
            for god in GODS:    
                if not enemy.passed and enemy.x < god.rect.x:
                    enemy.passed = True
                    add_enemy= True
            if colision:
                add_enemy = True          
        
        for dang in dangs:
            dang.move()
            for god in GODS:    
                if dang.colision(god, win):
                    ge[GODS.index(god)].fitness -= 1
                    nets.pop(GODS.index(god))
                    ge.pop(GODS.index(god))
                    GODS.pop(GODS.index(god))
            if dang.rect.x + dang.img.get_width() < 0:
                rem_dangs.append(dang)
                add_dang = True
            if not dang.cruzar and dang.rect.x < 0:
                dang.cruzar = True     
        
        if add_enemy:
            score += 1
            for genome in ge:
                genome.fitness += 5
        if pasado_width:
            enemies_AI.append(Enemies_AI(win_width))
        if add_dang:
            dangs.append(Dangling(win_width)) 
            ulti_dang.append(UltimateDang())
        if colision_dang:
            score += 1
            enem_killed += 1
            dangs.append(Dangling(win_width)) 
            ulti_dang.append(UltimateDang())
        
        if enem_killed == 5 :
            enemigos_bottom.clear()
            enemigos_top.clear()
            special_attack = True
            enem_killed = 0
        if special_attack:
            enemies_AI.append(Enemies_AI(win_eidth))
            
            
        for r in rem_enem:
            enemies_AI.remove(r)
        for j in rem_dangs:
            dangs.remove(j)
        for a in rem_ulti_god:
            ULTI_GOD.remove(a)
        for b in rem_ulti_dang:
            ulti_dang.remove(b)
        
        
        if not pasado_width and len(enemies_AI) == 0:
            enemies_AI.append(Enemies_AI(win_width))
            
        if not add_dang and len(dangs) == 0 and len(ulti_dang) == 0:
            dangs.append(Dangling(win_width)) 
            ulti_dang.append(UltimateDang())
        
        for god in GODS:   
            if god.rect.y + god.img.get_height() - 10  >= suelo or god.rect.y < -50:
                nets.pop(GODS.index(god))
                ge.pop(GODS.index(god))
                GODS.pop(GODS.index(god))

        draw_window_AI(win, gen, GODS, dangs, ulti_dang, enemies_AI, ULTI_GOD, score, round(clock.get_fps()), superficie, nubes, enem_ind, dang_ind)

def main():    
    global WIN, run, menu_setting, run_AI, gen, score, instructions
    win = WIN
    # ALGORITHM FOR PLAYING 4 TYPES OF MUSIC
    random_music = random.randint(0,3)
    songs = [pygame.mixer.Sound(os.path.join(DIR,"base" + str(x) + ".wav")) for x in range(1,5)]
    if random_music == 0:
        
        pygame.mixer.Channel(0).play(songs[0],-1)
        
    elif random_music == 1:
        pygame.mixer.Channel(1).play(songs[1],-1)
        
    elif random_music == 2:
        pygame.mixer.Channel(2).play(songs[2],-1)
    elif random_music == 3:
        pygame.mixer.Channel(3).play(songs[3],-1)

    ulti_lista = ""
    opcion1 = "Press 1"
    opcion2 = "Activated"
    enem_killed = 0
    reloj = pygame.time.Clock()
    activated_ulti= False
    instructions_button = 1
    while instructions:
        win.blit(instructions_bg, (0,0))
        for evento in pygame.event.get():    
            if evento.type == pygame.QUIT:
                run = False
                menu_setting = False
                instructions = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                instructions_button += 1
                if instructions_button == 3:
                    instructions = False
        
        pygame.display.flip()
    while menu_setting:
        win.blit(menu_bg, (0,0))
        player_label = pygame.font.SysFont("arial", 50).render("Press P to play without AI ",1,(0,0,0))
        ai_label = pygame.font.SysFont("arial", 50).render("Press A to play with AI", 1, (0,0,0))
        
        win.blit(player_label, (100 ,500))
        win.blit(ai_label,(100 ,550 ))
        
        
        for evento in pygame.event.get():    
            if evento.type == pygame.QUIT:
                run = False
                menu_setting = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    menu_setting = False 
                if evento.key == pygame.K_a:
                    menu_setting = False
                    run = False
                    run_AI = True
                if evento.key == pygame.K_ESCAPE:
                    run = False
                    menu_setting = False
        pygame.display.flip()
    while run and not menu_setting:
        reloj.tick(30)
        keys = pygame.key.get_pressed()
        eventos = pygame.event.get()
        for evento in eventos: 
            if evento.type == pygame.QUIT:
                run = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    activated_ulti= True
                if evento.key == pygame.K_SPACE:
                    for god in dios:   
                        god.fly()               
        
        if not(activated_ulti):
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
        special_attack = False
        for ulti in ulti_god:              
            if activated_ulti:
                ulti.move() 
            else:
                for god in dios:    
                    ulti.rect.midleft = god.rect.midright
            for dang in dangs:
                if ulti.colision_dang(dang,win):
                    dangs.clear()
                    ulti_dang.clear()
                    colision_dang = True
            if ulti.rect.x > win_width:
                rem3.append(ulti)
            if not ulti.pasado and ulti.rect.x > win_width:
                ulti.pasado = True
                add_ulti = True
        if add_ulti:
            activated_ulti = False
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
            for god in dios:    
                if enemigo_top.colision_god(god,win):
                    run = False
            if enemigo_top.x + enemigo_top.enemy_top.get_width() < 0:
                rem_top.append(enemigo_top)
                pasado_width = True
            
            for god in dios:    
                if not enemigo_top.passed and enemigo_top.x < god.rect.x:
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
            for god in dios:    
                if enemigo.colision_god(god,win):
                    run = False
            if enemigo.x  + enemigo.enemy_bottom.get_height() < 0:
                rem_bot.append(enemigo)
                pasado_width = True
            
            for god in dios:    
                if not enemigo.passed and enemigo.x < god.rect.x:
                    enemigo.passed = True
                    add_enemigo_bottom = True 
            if colision:
                add_enemigo_bottom= True
        
        for dang in dangs:
            dang.move()
            for god in dios:    
                if dang.colision(god, win):
                    run = False
            if dang.rect.x + dang.img.get_width() < 0:
                rem2.append(dang)
                add_dang = True
            if not dang.cruzar and dang.rect.x < 0:
                dang.cruzar = True     
        
        for ulti in ulti_dang:
            ulti.move()
            for god in dios:    
                if ulti.colision_god(god,win):
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
            score += 1
            enem_killed += 1
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
        if enem_killed == 5 :
            enemigos_bottom.clear()
            enemigos_top.clear()
            special_attack = True
            enem_killed = 0
            score = score + 5
        if special_attack:
            enemigos_bottom.append(Enemies_Bottom(win_width))
            enemigos_top.append(Enemies_Top(win_width))
            
        for god in dios:   
            if god.rect.y + god.img.get_height() - 10  >= suelo or god.rect.y < -50:
                run = False
            god.move(evento)
        nubes.move()
        draw_window(win, dios, dangs,ulti_dang,ulti_foto,ulti_lista,enemigos_top,enemigos_bottom,ulti_god, score, round(reloj.get_fps()), superficie,nubes,evento)       
    
    # AQUI IRIA LO DE SI LA RUN_AI IS TRUE SE PONE LA FUNCION Y CORRE LA IA
    while run_AI and not menu_setting:
        RUN(config_path)
def RUN(config_file):
        
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)    
    p = neat.Population(config)
        
        
    # Print the stats and the progress of the neural network in terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
        
        
    # Run the main function and gives 50 generations
    winner = p.run(eval_genomes, 50)
        
    # The final result of the stats
    print('\nThe Best Genome is\n{!s}'.format(winner))
    
if __name__ == '__main__':
    config_path = os.path.join(DIR, 'config-feedforward.txt')
    main() 