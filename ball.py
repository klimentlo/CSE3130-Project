# player.py in g_asteroids (folder)

'''
title: player class
author: kliment lo
date-created: 2023/11/06
'''

from my_sprite import MySprite
from box import Box
from color import Color
import random


class Ball(MySprite):
    def __init__(self, isBonus="Regular"):
        MySprite.__init__(self)
        self.__BALL_SPRITE = Box(10, 10)
        if isBonus == "BonusBall":
            self.__BALL_SPRITE.setColor(Color.NEON)
            X = random.randrange(200,600)
            self.setPOS(random.randrange(200,600), 480)
            self.changeDirY(-1)
            self.changeDirX(random.choice([-1, 1]))


        self._SURFACE = self.__BALL_SPRITE.getSurface()






    def isLost(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0):
        MySprite.checkBoundaries(self, MAX_X, MAX_Y)
        if self.getY() == MAX_Y - self.getHeight():
            return True




