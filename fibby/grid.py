import pygame

class GRID:
    def __init__(self,g):
        self.g = g

        self.xy = []
        self.tilesize = (self.g.screenxy[0] // 100 , self.g.screenxy[1] // 100)

        for i in range(0,self.g.screenxy[0],self.tilesize[0]):
            for e in range(0,self.g.screenxy[1],self.tilesize[1]):
                self.xy.append((i,e))


    def XYS(self):
        return self.xy

    def PLACEMENT(self,x,y):
        if (self.tilesize[0] * x ,self.tilesize[1] * y) in self.xy:
            return (self.tilesize[0] * x ,self.tilesize[1] * y)


    def IMG_RESIZE(self,img,gridsx,gridsy):
        return pygame.transform.scale(img,(self.tilesize[0] * gridsx , self.tilesize[1] * gridsy))


    def TILECHECK(self,tile):
        s = pygame.Surface(self.tilesize)
        s.fill(self.g.colors['xkcd:warm purple'])
        self.g.screen.blit(s,tile)



    
