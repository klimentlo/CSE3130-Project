# window.py in f_ghostly (folder)
'''
title: Window class for pygame
author: kliment lo
date-created: 2023-10-30
'''

import pygame
from color import Color
class Window:
    '''
    creates the window that will load pygame
    '''

    def __init__(self, TITLE, WIDTH, HEIGHT, FPS):
        self.__TITLE = TITLE
        self.__FPS = FPS
        self.__WIDTH = WIDTH
        self.__HEIGHT = HEIGHT
        self.__SCREEN_DIMENSIONS = (self.__WIDTH, self.__HEIGHT)
        self.__CLOCK = pygame.time.Clock()
        self.__SURFACE = pygame.display.set_mode(self.__SCREEN_DIMENSIONS)
        self.__SURFACE.fill(Color.GREY) # pulls the color from color class
        pygame.display.set_caption(self.__TITLE)

    def clearScreen(self):
        self.__SURFACE.fill(Color.GREY)

    def updateFrame(self):
        self.__CLOCK.tick(self.__FPS)
        pygame.display.flip()

    def getSurface(self):
        return self.__SURFACE

    def getWidth(self):
        return self.__WIDTH

    def getHeight(self):
        return self.__HEIGHT

    def getFPS(self):
        return self.__FPS