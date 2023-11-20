# player.py in g_asteroids (folder)

'''
title: player class
author: kliment lo
date-created: 2023/11/06
'''

import pygame
from my_sprite import MySprite
from box import Box
from lazer import Lazer

class Player(MySprite):

    def __init__(self):
        MySprite.__init__(self)
        self.__PLAYER_SPRITE = Box(30,60)
        self._SURFACE = self.__PLAYER_SPRITE.getSurface()
        self.__HEALTH = 100
        self.__ANGLE = 0
        self.__LAZERS = []
        for i in range(300):
            self.__LAZERS.append(Lazer())

        self.__LAZER_COOLDOWN = False
        self.__LAZER_COOLDOWN_TIMER = 0

    # MODIFIER METHODS
    def ADrotate(self, KEY_PRESSED):
        if KEY_PRESSED[pygame.K_a]:
            self.__ANGLE += self._SPD # will eventually make it rotate anti-clockwise
        if KEY_PRESSED[pygame.K_d]:
            self.__ANGLE -= self._SPD # will eventually make it rotate clockwise
        CENTER = self.getCenter()
        self._SURFACE = pygame.transform.rotate(self.__PLAYER_SPRITE.getSurface(), self.__ANGLE)
        self.setX(CENTER[0] - self.getWidth()//2)
        self.setY(CENTER[1] - self.getHeight()//2)

    def fireLazer(self, KEY_PRESSED):
        if KEY_PRESSED[pygame.K_SPACE] and not self.__LAZER_COOLDOWN:
            for lazer in self.__LAZERS:
                if not lazer.getFired():
                    lazer.setFired(True)
                    lazer.setAngle(-self.__ANGLE)
                    self.__LAZER_COOLDOWN = True
                    break

    def setX(self, X):
        MySprite.setX(self, X)
        for Lazer in self.__LAZERS:
            if not Lazer.getFired():
                Lazer.setX(X + self.getWidth()//2 - Lazer.getWidth()//2)

    def setY(self, Y):
        MySprite.setY(self, Y)
        for Lazer in self.__LAZERS:
            if not Lazer.getFired():
                Lazer.setY(Y + self.getHeight()//2 - Lazer.getHeight()//2)

    def setPOS(self, X, Y):
        MySprite.setPOS(self, X, Y)
        for Lazer in self.__LAZERS:
            if not Lazer.getFired():
                Lazer.setPOS(X + self.getWidth()//2 - Lazer.getWidth()//2, Y + self.getHeight()//2 - Lazer.getHeight()//2)

    # processing
    def moveLazers(self):
        for lazer in self.__LAZERS:
            lazer.move()

    def resetLazers(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0):
        for lazer in self.__LAZERS:
            if not (MIN_X < lazer.getX() < MAX_X) or \
                    not (MIN_Y < lazer.getY() < MAX_Y):
                lazer.setPOS(self.getX() + self.getWidth()//2 - lazer.getWidth()//2,
                             self.getY() + self.getHeight()//2 - lazer.getHeight()//2)
                lazer.setFired(False)

    def updateLazerCooldown(self, FPS):
        '''
        counts how long the lazer cooldown is based on the FPS
        :param FPS: int
        :return: none
        '''
        if self.__LAZER_COOLDOWN:
            self.__LAZER_COOLDOWN_TIMER += 1
            if self.__LAZER_COOLDOWN_TIMER > FPS//900000000000000000000000000000000000000000000000000000000:
                self.__LAZER_COOLDOWN = False
                self.__LAZER_COOLDOWN_TIMER = 0

    def takeDamage(self, DAMAGE):
        self.__HEALTH -= DAMAGE


    # ACCESSOR METHODS
    def getLazerCount(self):
        return len(self.__LAZERS)

    def getLazerSurface(self, INDEX):
        return self.__LAZERS[INDEX].getSurface()

    def getLazerPOS(self, INDEX):
        return self.__LAZERS[INDEX].getPOS()

    def getHealth(self):
        return self.__HEALTH


if __name__ == "__main__":
    from window import Window
    pygame.init()
    WINDOW = Window("Player test", 800, 600, 30)
    PLAYER = Player()
    PLAYER.setPOS(WINDOW.getWidth()//2 - PLAYER.getWidth()//2, WINDOW.getHeight()//2 - PLAYER.getHeight()//2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        PRESSED_KEYS = pygame.key.get_pressed()

        PLAYER.ADrotate(PRESSED_KEYS)
        PLAYER.fireLazer(PRESSED_KEYS)
        PLAYER.resetLazers(WINDOW.getWidth(), WINDOW.getHeight())

        PLAYER.moveLazers()
        PLAYER.updateLazerCooldown(WINDOW.getFPS())


        WINDOW.clearScreen()
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        for i in range(PLAYER.getLazerCount()):
            WINDOW.getSurface().blit(PLAYER.getLazerSurface(i), PLAYER.getLazerPOS(i))
        WINDOW.updateFrame()

