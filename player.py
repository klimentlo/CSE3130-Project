# player.py in g_asteroids (folder)

'''
title: player class
author: kliment lo
date-created: 2023/11/06
'''

import pygame
from my_sprite import MySprite
from box import Box
from brick import Brick

class Player(MySprite):

    def __init__(self, SPEED=15): #  WIDTH, HEIGHT, X, Y, SPEED=5, COLOR=(255,255,255)

        MySprite.__init__(self, 1, 1, 0, 0, SPEED, (255, 255, 255))
        self.__PLAYER_SPRITE = Box(175, 15)
        self._SURFACE = self.__PLAYER_SPRITE.getSurface()
        self.__LIVES = 10
        self.__GAME_OVER = False


    # SETTER METHOD
    def isDead(self):
        if self.__LIVES <= 0:
            self.__GAME_OVER = True
    def loseLife(self):
        self.__LIVES -= 1

    # GETTER METHODS
    def getLives(self):
        return self.__LIVES

if __name__ == "__main__":
    from window import Window
    pygame.init()
    WINDOW = Window("Player test", 800, 600, 30)
    PLAYER = Player()

    PLAYER.setPOS(WINDOW.getWidth()//2 - PLAYER.getWidth()//2, WINDOW.getHeight()* 0.9)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        PRESSED_KEYS = pygame.key.get_pressed()

        PLAYER.ADmove(PRESSED_KEYS)
        PLAYER.checkBoundaries(WINDOW.getWidth(), WINDOW.getHeight())

        WINDOW.clearScreen()
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        WINDOW.updateFrame()

