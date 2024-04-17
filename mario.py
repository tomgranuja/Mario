#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import csv
import sys
import pygame
import numpy as np

pygame.init()
clock = pygame.time.Clock()
#Width and height of the game
size = w,h = 612, 530
#Screen, background and player surfaces
screen = pygame.display.set_mode(size)
screen.fill((255,)*3)
background = pygame.image.load('bground.png').convert()

class Soul():
    def __init__(self, surface, pos):
        self.surface = surface
        self.pos = pos
        
    #Transform self.pos in a property in order to
    #use float precition in the x and y coordinates.
    @property
    def pos(self):
        x,y,w,h = self._pos
        #Return rounded x and y coordinates Rect.
        return pygame.Rect(round(x), round(y), w, h)
    
    @pos.setter
    def pos(self,o):
        x,y,w,h = o
        #Store as a float list.
        self._pos = [x,y,w,h]

class Mario(Soul):
    OFFSET = h-477
    def __init__(self, x, jump_data=[[0,0]]):
        surface = pygame.image.load('mario.png').convert_alpha()
        r = surface.get_rect()
        pos = [x, h-self.OFFSET-r.h, r.w, r.h]
        super().__init__(surface, pos)
        self.x = x
        self.y = h-self.OFFSET-r.h
        self.jump_data = np.array(jump_data)
        self.jump_idx = 0
        self.mvector = np.array((0,0))
        self.speed = np.array((3,3))
        self.jumping = False
    
    def is_outside(self):
        r = self.pos
        h_out = r.right < 0 or r.left > w
        # v_out = r.bottom < 0 or r.top > h
        return h_out #or v_out
    
    def move(self,keys):
        if self.jumping:
            self._pos[:2] = self.jump_data[self.jump_idx]*(1,-1) + (self.x,self.y)
            self.jump_idx += 1
            if self.jump_idx == len(self.jump_data):
                self.x, self.y = self._pos[:2]
                self.jumping = False
                self.jump_idx = 0
        else:
            #2-dimensional vectors
            u = np.ones(2)
            i = u*(1,0)
            j = u*(0,-1)
            vector = sum([  i*keys[self.k['r']],
                        -i*keys[self.k['l']],
                            j*keys[self.k['u']],
                        -j*keys[self.k['d']],
                        ])
            self.mvector = vector*self.speed
            #Move with float precition
            self._pos[:2] += self.mvector
            self.x, self.y = self._pos[:2]
        
        
        if self.is_outside():
            r = self.pos
            if r.left > w:
                self.pos = r.move(-w-r.w,0)
            elif r.right < 0:
                self.pos = r.move(w+r.w,0)
            #self.pos = self.surface.get_rect().move(0,h/2)
            
    def set_kbd_dic(self, **kwargs):
        k = { 'r': pygame.K_RIGHT,
              'l': pygame.K_LEFT,
              'u': pygame.K_UP,
              'd': pygame.K_DOWN,
            }
        k.update(kwargs)
        self.k = { key: k[key] for key in 'rlud' }

objects = []
with open('jdata.csv', newline='') as f:
    reader = csv.DictReader(f)
    jdata = [ (float(row['x']), float(row['y']))
             for row in reader ]

mario = Mario(40, jdata)
mario.set_kbd_dic(r = pygame.K_d,
                  l = pygame.K_a,
                  u = pygame.K_w,
                  d = pygame.K_s)
objects.append(mario)
screen.blit(background,(0,0))

while True:
    #Catch quit event and exit
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE: sys.exit()
    keys = pygame.key.get_pressed()
    for o in objects:
        #Erase objects using the background
        screen.blit(background, o.pos, o.pos)
    for o in objects:
        #Calc new objects position
        if keys[pygame.K_SPACE]:
            o.jumping = True
        o.move(keys)
        #Paint objects
        screen.blit(o.surface, o.pos)
    pygame.display.update()
    #Overall game frames per second
    clock.tick(20)

#if __name__ == '__main__':
#    pass
