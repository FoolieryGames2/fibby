import pygame as py
import pickle
import time
import os.path
import numpy
import random
from grid import *
#initilize pygame
py.init()




class GAME:
    def __init__(self):


        #make a font for text
        py.font.init()
        self.font = py.font.Font(None,30)
        #first lets set some vals
        #grabing the pickled color list
        with open('Colors.pickle', 'rb') as f:
                    self.colors = pickle.load(f)
                    f.close()

        #we will need a bool (True or False) val to tell the game when to close
        self.running = True
        #now call a window from pygame.display , pygame only supports one main window
        self.screen = py.display.set_mode((500,700))
        #sinse this is for a cell phone we will be needing the actualy generated
        #size of the window
        self.screenxy = self.screen.get_size()
        #we can also give this window a title
        py.display.set_caption('Fibby')

        self.LOADUP()



        self.grid = GRID(self)



        self.buttonimgs = self.SPRITESHEETLOADER('buttons.png' , 4 , (50,50) , (15,15) , (0,0,0))

        self.b1 = 0
        self.b1p  = 1
        self.b2 = 0
        self.b2p  = 1
        self.b3 = 3
        self.b3p = 2



        self.menu1 = ['care' , 'stats' , 'say goodbye']
        self.menu2 = ['feed' , 'love' , 'scoop', 'back']
        self.menu3 = ['back']

        self.menupos = 0
        self.onmenu = 0
        self.gamestate = 0

        self.fibbyimgs = self.SPRITESHEETLOADER('fibby.png' , 21 , (32,32) , (10,10) , (255,255,255))
        self.fibbyhappy = [self.fibbyimgs[0],self.fibbyimgs[1]]
        self.fibbyhappyleft = [self.fibbyimgs[6],self.fibbyimgs[7]]
        self.fibbyhappyright = [py.transform.flip(self.fibbyimgs[6],True,False),py.transform.flip(self.fibbyimgs[7],True,False)]
        self.fibbyhearts = [self.fibbyimgs[11],self.fibbyimgs[12]]
        self.fibbyfed = [self.fibbyimgs[18],self.fibbyimgs[19],self.fibbyimgs[20]]
        self.poopimgs = [self.fibbyimgs[13],self.fibbyimgs[14],self.fibbyimgs[15]]
        self.fibbyangry = [self.fibbyimgs[4], self.fibbyimgs[5]]


        self.fibbystate = 'happy idle'
        self.fibbycounter = 0
        self.fibbycounterp = 0
        self.fibbyx = 50
        self.timer_runones = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.timer_holder = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.buttons_holder = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]




        self.background = self.grid.IMG_RESIZE(py.image.load('gui_backing.png'), 100, 100)

        self.clicked = [False,False]


    def TIMER(self,runone,length,repeat = True):
            if self.timer_runones[runone]:
                self.timer_holder[runone] = time.time()
                self.timer_runones[runone] = False

            if self.timer_holder[runone] + length <= time.time():
                if repeat:
                    self.timer_holder[runone] = time.time()
                else:
                    self.timer_holder[runone] = time.time() * 2
                return True
            else:
                return False

    def RESETALLTIMERS(self):
        self.timer_runones = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.timer_holder = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def SPRITESHEETLOADER(self,img,numberof,sizexy,newgridsizexy,colorkey):
        image = pygame.image.load(img)
        spacer = 0
        l = []
        for i in range(numberof):
            s = pygame.Surface(sizexy)
            s.blit(image,(-0 - spacer,0))
            spacer += sizexy[0]
            l.append(s)

        for i in range(0,len(l) ):
            l[i] = self.grid.IMG_RESIZE(l[i], newgridsizexy[0], newgridsizexy[1])
            l[i].set_colorkey(colorkey)

        return l

    def BUTTON(self,img,placement,but = 'L'):
        r = img.get_rect(topleft = placement)
        self.screen.blit(img,r.topleft)
        if but == 'L':

            if r.collidepoint(self.mpos) and self.clicked[0]:

                return True
            else:
                return False

        if but == 'R':

            if r.collidepoint(self.mpos) and self.clicked[1]:
                return True
            else:
                return False

        self.clicked[0] = False
        self.clicked[2] = False
        self.clicked[1] = False

    def BUILDMENU(self):

        spacer = 0
        if self.onmenu == 0:
            for i in self.menu1:
                if self.menu1[self.menupos] == i:
                    f = self.font.render(i,1,(self.colors['black']) ,self.colors['xkcd:bluish'])
                    r = f.get_rect()
                else:
                    f = self.font.render(i,1,(self.colors['black']) )
                    r = f.get_rect()


                py.draw.rect(f,self.colors['xkcd:booger'],(0,0,r.width,r.height),1)
                self.screen.blit(f,self.grid.PLACEMENT(15 + spacer,52))
                spacer += 20

        if self.onmenu == 1:
            for i in self.menu2:
                if self.menu2[self.menupos] == i:
                    f = self.font.render(i,1,(self.colors['black']),self.colors['xkcd:bluish'])
                    r = f.get_rect()
                else:
                    f = self.font.render(i,1,(self.colors['black']))
                    r = f.get_rect()

                py.draw.rect(f,self.colors['xkcd:booger'],(0,0,r.width,r.height),2)
                self.screen.blit(f,self.grid.PLACEMENT(15 + spacer,52))
                spacer += 20

        if self.onmenu == 2:


            f = self.font.render('back',1,(self.colors['black']),self.colors['xkcd:bluish'])
            r = f.get_rect()


            py.draw.rect(f,self.colors['xkcd:booger'],(0,0,r.width,r.height),2)
            self.screen.blit(f,self.grid.PLACEMENT(15 + spacer,52))
            spacer += 20

    def BUTTONHANDLER(self):
        if self.BUTTON(self.buttonimgs[self.b1],self.grid.PLACEMENT(30, 70)):
            print('hit button right')
            self.menupos += 1
            if self.onmenu == 0:
                if self.menupos > 2:
                    self.menupos = 0
            if self.onmenu == 1:
                if self.menupos > 3:
                    self.menupos = 0
            self.b1 = self.b1p
            self.clicked[0] = False
        else:
            self.b1 = 0

        if self.BUTTON(pygame.transform.flip(self.buttonimgs[self.b2],True,False),self.grid.PLACEMENT(10, 70)):
            print('hit button left')

            self.menupos -= 1
            if self.onmenu == 0:
                if self.menupos < 0:
                    self.menupos = 2
            if self.onmenu == 1:
                if self.menupos < 0:
                    self.menupos = 3
            if self.onmenu == 2:
                self.menupos = 0
            self.b2 = self.b2p
            self.clicked[0] = False

        else:
            self.b2 = 0

        if self.BUTTON(pygame.transform.flip(self.buttonimgs[self.b3],True,False),self.grid.PLACEMENT(70, 70)):
            print('hit button select')
            if self.onmenu == 0:
                if self.menupos == 0:
                    self.onmenu = 1
                elif self.menupos == 1:
                    self.gamestate = 1


                if self.menupos == 2:
                    py.quit()

            elif self.onmenu == 1:
                if self.menupos == 3:
                    self.onmenu = 0
                    self.menupos = 0
                elif self.menupos == 0:
                    self.fibbyLevels['hunger'] = 100
                    print('feed')
                    self.SAVE()
                    self.fibbystate = 'fed'

                elif self.menupos == 2:
                    if len(self.fibbyLevels['poopxys']) > 0:
                        self.fibbyLevels['poopxys'] = self.fibbyLevels['poopxys'][:-1]
                        self.fibbystate = 'hearts'
            elif self.onmenu == 2:
                if self.menupos == 0:
                    self.onmenu = 0
                    self.gamestate = 0


            self.b3 = self.b3p
            self.clicked[0] = False

        else:
            self.b3 = 3

    def LOADUP(self):
        if os.path.isfile('saves.pickle'):
            with open('saves.pickle' , 'rb') as f:
                self.fibbyLevels = pickle.load(f)
                f.close()
        else:
            with open('saves.pickle' , 'wb') as f:
                self.fibbyLevels = {
                                    'happiness' : 70 ,
                                     'poop maddness' : 0 ,
                                      'hunger' : 100 ,
                                      'lifetimer' : 0,
                                      'endingepoch' : time.time(),
                                      'poopxys' : [],
                                      'pooptimers' : [] ,
                                      'health' : 100

                                      }
            with open('saves.pickle', 'wb') as f:
                pickle.dump(self.fibbyLevels, f, protocol=pickle.HIGHEST_PROTOCOL)
                f.close()
            self.timepassed = round(time.time()) - self.fibbyLevels['endingepoch']
            self.fibbyLevels['hunger'] -= (self.timepassed//5)
            self.fibbyLevels['lifetimer'] += self.timepassed

    def SAVE(self):
        with open('saves.pickle', 'wb') as f:
            pickle.dump(self.fibbyLevels, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()

    def FIBBYAI(self):

        if self.gamestate == 0:
            if self.fibbystate == 'happy idle':
                if self.fibbycounter > 1:
                    self.fibbycounter = 0
                self.screen.blit(self.fibbyhappy[self.fibbycounter],self.grid.PLACEMENT(self.fibbyx,20))
                if self.TIMER(2,0.5):
                    self.fibbycounter += 1
                if self.fibbycounter > 1:
                    self.fibbycounter = 0

            elif self.fibbystate == 'happy left':
                if self.fibbycounter > 1:
                    self.fibbycounter = 0
                self.screen.blit(self.fibbyhappyleft[self.fibbycounter],self.grid.PLACEMENT(self.fibbyx,20))
                if self.TIMER(2,0.5):
                    self.fibbycounter += 1

                self.fibbyx -= 1
                if self.fibbyx < 20:
                    self.fibbystate = random.choice(['happy idle','happy right'])
                if self.fibbycounter > 1:
                    self.fibbycounter = 0

            elif self.fibbystate == 'happy right':
                if self.fibbycounter > 1:
                    self.fibbycounter = 0
                self.screen.blit(self.fibbyhappyright[self.fibbycounter],self.grid.PLACEMENT(self.fibbyx,20))
                if self.TIMER(2,0.5):
                    self.fibbycounter += 1

                self.fibbyx +=1
                if self.fibbyx > 60:
                    self.fibbystate = random.choice(['happy idle','happy left'])

                if self.fibbycounter > 1:
                    self.fibbycounter = 0

            elif self.fibbystate == 'fed':
                self.screen.blit(self.fibbyfed[self.fibbycounter],self.grid.PLACEMENT(self.fibbyx,20))
                if self.TIMER(2,0.5):
                    self.fibbycounter += 1
                if self.fibbycounter > 2:
                    self.fibbycounter = 0
                if self.TIMER(9,5):
                    self.fibbycounter = 0
                    self.fibbystate == 'hearts'


            elif self.fibbystate == 'hearts':
                self.screen.blit(self.fibbyhearts[self.fibbycounter],self.grid.PLACEMENT(self.fibbyx,20))
                if self.TIMER(2,0.5):
                    self.fibbycounter += 1
                if self.fibbycounter > 1:
                    self.fibbycounter = 0
                if self.TIMER(8,5):
                    self.fibbystate == ['happy idle']

            elif self.fibbystate == 'poop':
                print('entered the elif poop')
                self.screen.blit(self.fibbyangry[1],self.grid.PLACEMENT(self.fibbyx,20))


                if self.TIMER(18,5):
                    print('timer whent off to finish poop anti')
                    self.fibbystate = random.choice(['happy idle','happy left','happy right'])
                    self.fibbyLevels['health'] += 5
                    self.fibbyLevels['happiness'] -= 15
                    self.fibbyLevels['poopxys'].append(self.grid.PLACEMENT(self.fibbyx,20))
                    self.fibbyLevels['pooptimers'].append(time.time())
            if self.TIMER(3,5):
                self.SAVE()
                #self.fibbystate = random.choice(['happy idle','happy left','happy right'])

            if len(self.fibbyLevels['poopxys']) > 0:
                counter = 0
                for i in range(len(self.fibbyLevels['poopxys'])):
                    self.screen.blit(self.poopimgs[self.fibbycounterp],self.fibbyLevels['poopxys'][i])
                if self.TIMER(14,0.3):
                    self.fibbycounterp += 1
                if self.fibbycounterp > 2:
                    self.fibbycounterp = 0
        elif self.gamestate == 1:
            self.onmenu = 2
            self.menupos = 0
            spacer2 = 0
            counter2 = 0
            for i in self.fibbyLevels.values():
                if counter2 < 4:
                    f = self.font.render(str(i) ,1 , (self.colors['black']))
                    # py.draw.rect(f,self.colors['xkcd:booger'],(0,0,r.width,r.height),1)
                    self.screen.blit(f,self.grid.PLACEMENT(15 + spacer2,20))
                    spacer2 += 20
                counter2 += 1
            counter2 = 0

    def GAMETIME(self):
        if self.TIMER(6,1):
            self.fibbyLevels['lifetimer'] += 1
            self.fibbyLevels['endingepoch'] = time.time()

        if self.TIMER(5,5):
            self.fibbyLevels['hunger'] -= 1
            if self.fibbyLevels['hunger'] < 0:
                self.fibbyLevels['hunger'] = 0

        if self.TIMER(10,3):
            self.fibbyLevels['happiness'] -= 1
            if self.fibbyLevels['hunger'] < 40:
                self.fibbyLevels['health'] -= 1
            xcounter = 0
            for i in self.fibbyLevels['pooptimers']:
                if time.time() - i > 100:
                    self.fibbyLevels['health'] -=1
                    self.fibbyLevels['happiness'] -= 1
        if self.TIMER(11,10):
            print('timer wnts off for poop')
            self.fibbystate = 'poop'

        if self.fibbyLevels['health'] <= 0:
            print('fibby is dead')
    def UPDATE(self):
        if self.clicked[0]:
            print('left click')


        if self.clicked[1]:
            print('right click')

        self.GAMETIME()

    def EVENTS(self):
        self.mpos = py.mouse.get_pos()
        for e in py.event.get():
            if e.type == py.QUIT:
                py.quit()

            if e.type == py.MOUSEBUTTONDOWN:
                if py.mouse.get_pressed()[0]:
                    self.clicked[0] = True
                if py.mouse.get_pressed()[2]:
                    self.clicked[1] = True

            if e.type == py.MOUSEBUTTONUP:

                self.clicked[0] = False

                self.clicked[1] = False

    def DRAW(self):
        self.screen.blit(self.background , self.grid.PLACEMENT(0,0))

        self.BUTTONHANDLER()

        self.BUILDMENU()

        self.FIBBYAI()

        py.display.flip()

    def RUN(self):
        while self.running:
            self.EVENTS()
            self.UPDATE()
            self.DRAW()

g = GAME()

g.RUN()
