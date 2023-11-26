# box.py in d_inheritance(folder)
'''
title: box class
author: kliment lo
date-created: 2023/10/30
'''

from my_sprite import MySprite
import pygame

class Box(MySprite):

    def __init__(self, WIDTH=1, HEIGHT=1):
        MySprite.__init__(self, WIDTH, HEIGHT) # < --- Inheritance
        self._SURFACE = pygame.Surface(self._DIMENSIONS, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._COLOR)

    # MODIFIER METHOD
    def setColor(self, COLOR):
        '''
        update the color of the box
        :param COLOR: tuple
        :return: none
        '''
        self.__COLOR = COLOR
        self._SURFACE.fill(self.__COLOR)


if __name__ == "__main__":
    from window import Window
    from random import randrange
    pygame.init()
    WINDOW = Window("Box", 800, 600, 60)
    #BOX = Box(100, 100)
    BOX = Box(175, 15)
    BOX2 = Box(15, 15)
    BOX.setX(WINDOW.getWidth()//2 - BOX.getWidth()//2)
    BOX.setY(WINDOW.getHeight()*0.9)
    BOX.setSpeed(7)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        KEYPRESSES = pygame.key.get_pressed()
        BOX.ADmove(KEYPRESSES)
        BOX2.bounceX(WINDOW.getWidth())
        BOX2.bounceY(WINDOW.getHeight())
        BOX.checkBoundaries(WINDOW.getWidth(),WINDOW.getHeight())

        WINDOW.clearScreen()
        WINDOW.getSurface().blit(BOX.getSurface(), BOX.getPOS())
        WINDOW.getSurface().blit(BOX2.getSurface(), BOX2.getPOS())

        #WINDOW.getSurface().blit(BOX.getSurface(), BOX.getPOS())
        WINDOW.updateFrame()