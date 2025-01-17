#brick.py
'''
title: brick class
author: kliment lo
date-created: 2023/11/26
'''

from my_sprite import MySprite
from box import Box
import pygame
from color import Color



class Brick(MySprite):
    def __init__(self, SCALE=1):
        MySprite.__init__(self) # < --- Inheritance
        WIDTH = 100
        HEIGHT = 50

        # Made so no matter the size of the brick, the collision boxes will scale proportionally
        # --- Construction of the brick (ATTRIBUTES)
        self.__BRICK_SPRITE = Box(WIDTH, HEIGHT)
        self.__BRICK_SPRITE.setScale(SCALE)
        self._SURFACE = self.__BRICK_SPRITE.getSurface()


        # Top collision box
        self.__BRICK_TOP = Box(WIDTH*0.9, HEIGHT*0.1)
        self.__BRICK_TOP.setColor(Color.RED)
        self.__BRICK_TOP.setScale(SCALE)

        # Bottom collision box
        self.__BRICK_BOTTOM = Box(WIDTH*0.9, HEIGHT*0.1)
        self.__BRICK_BOTTOM.setColor(Color.RED)
        self.__BRICK_BOTTOM.setScale(SCALE)

        # Left collision box
        self.__BRICK_LEFT = Box(WIDTH*0.05, HEIGHT*0.8)
        self.__BRICK_LEFT.setColor(Color.BLUE)
        self.__BRICK_LEFT.setScale(SCALE)

        # Right collision box
        self.__BRICK_RIGHT = Box(WIDTH*0.05, HEIGHT*0.8)
        self.__BRICK_RIGHT.setColor(Color.BLUE)
        self.__BRICK_RIGHT.setScale(SCALE)

        # CORNERS :(
        self.__TOP_LEFT_CORNER = Box(WIDTH*0.05, HEIGHT*0.1)
        self.__TOP_LEFT_CORNER.setColor(Color.GREEN)
        self.__TOP_LEFT_CORNER.setScale(SCALE)

        self.__TOP_RIGHT_CORNER = Box(WIDTH*0.05, HEIGHT*0.1)
        self.__TOP_RIGHT_CORNER.setColor(Color.GREEN)
        self.__TOP_RIGHT_CORNER.setScale(SCALE)

        self.__BOTTOM_LEFT_CORNER = Box(WIDTH*0.05, HEIGHT*0.1)
        self.__BOTTOM_LEFT_CORNER.setColor(Color.GREEN)
        self.__BOTTOM_LEFT_CORNER.setScale(SCALE)

        self.__BOTTOM_RIGHT_CORNER = Box(WIDTH*0.05, HEIGHT*0.1)
        self.__BOTTOM_RIGHT_CORNER.setColor(Color.GREEN)
        self.__BOTTOM_RIGHT_CORNER.setScale(SCALE)


    # --- SETTER METHODS



    def setBrickPOS(self, X, Y):
        '''
        sets all collision boxes and surfaces to the set location :D
        :param X:
        :param Y:
        :return:
        '''

        self.__BRICK_SPRITE.setPOS(X, Y)

        # Sides
        self.__BRICK_TOP.setPOS(X + self.__BRICK_SPRITE.getWidth() // 2 - self.__BRICK_TOP.getWidth() // 2, Y)
        self.__BRICK_BOTTOM.setPOS(X + self.__BRICK_SPRITE.getWidth() // 2 - self.__BRICK_TOP.getWidth() // 2,
                                   Y + self.__BRICK_SPRITE.getHeight() - self.__BRICK_BOTTOM.getHeight())
        self.__BRICK_LEFT.setPOS(X, Y + self.__BRICK_SPRITE.getHeight() // 2 - self.__BRICK_LEFT.getHeight() // 2)
        self.__BRICK_RIGHT.setPOS(X + self.__BRICK_SPRITE.getWidth() - self.__BRICK_RIGHT.getWidth(),
                                  Y + self.__BRICK_SPRITE.getHeight() // 2 - self.__BRICK_RIGHT.getHeight() // 2)

        # Corners
        self.__TOP_LEFT_CORNER.setPOS(X, Y)
        self.__TOP_RIGHT_CORNER.setPOS(X + self.__BRICK_SPRITE.getWidth() - self.__TOP_RIGHT_CORNER.getWidth(), Y)
        self.__BOTTOM_LEFT_CORNER.setPOS(X, Y + self.__BRICK_SPRITE.getHeight() - self.__BOTTOM_LEFT_CORNER.getHeight())
        self.__BOTTOM_RIGHT_CORNER.setPOS(X + self.__BRICK_SPRITE.getWidth() - self.__BOTTOM_RIGHT_CORNER.getWidth(),
                                          Y + self.__BRICK_SPRITE.getHeight() - self.__BOTTOM_RIGHT_CORNER.getHeight())




    # --- GETTER METHODS

    # --- SIDES
    # Top
    def getTopSurface(self):
        return self.__BRICK_TOP.getSurface()

    def getTopPOS(self):
        return self.__BRICK_TOP.getPOS()

    # Bottom
    def getBottomSurface(self):
        return self.__BRICK_BOTTOM.getSurface()

    def getBottomPOS(self):
        return self.__BRICK_BOTTOM.getPOS()

    # Left
    def getLeftSurface(self):
        return self.__BRICK_LEFT.getSurface()

    def getLeftPOS(self):
        return self.__BRICK_LEFT.getPOS()

    # Right
    def getRightSurface(self):
        return self.__BRICK_RIGHT.getSurface()

    def getRightPOS(self):
        return self.__BRICK_RIGHT.getPOS()

    # --- CORNERS
    # Top Left
    def getTopLeftSurface(self):
        return self.__TOP_LEFT_CORNER.getSurface()

    def getTopLeftPOS(self):
        return self.__TOP_LEFT_CORNER.getPOS()

    # Top Right
    def getTopRightSurface(self):
        return self.__TOP_RIGHT_CORNER.getSurface()

    def getTopRightPOS(self):
        return self.__TOP_RIGHT_CORNER.getPOS()

    # Bottom Right
    def getBottomLeftSurface(self):
        return self.__BOTTOM_LEFT_CORNER.getSurface()

    def getBottomLeftPOS(self):
        return self.__BOTTOM_LEFT_CORNER.getPOS()

    # Bottom Right
    def getBottomRightSurface(self):
        return self.__BOTTOM_RIGHT_CORNER.getSurface()

    def getBottomRightPOS(self):
        return self.__BOTTOM_RIGHT_CORNER.getPOS()


    # Processing
    def isBrickCollision(self, WIDTH, HEIGHT, POS, DIRX, DIRY):
        '''
        use width, height, and POS of the ball, and see if it collides with the corresoponding brick
        return: DIRECTION OF BALL MOVEMENT
        '''
        # Whenever there is a -1, it is switching the direction it
        #\/tells them it did collide
        # [True, 1, -1]
        #        /\   \ DIRY changes direction
        #       DIRX remains the same
        # --- SIDES

        # Top
        if self.__BRICK_TOP.isCollision(WIDTH, HEIGHT, POS):
            return (True, DIRX , -1)

        # Bottom
        if self.__BRICK_BOTTOM.isCollision(WIDTH, HEIGHT, POS):
            return (True, DIRX , 1)
        # Left
        if self.__BRICK_LEFT.isCollision(WIDTH, HEIGHT, POS):
            return (True, -1 , DIRY)
        # Right
        if self.__BRICK_RIGHT.isCollision(WIDTH, HEIGHT, POS):
            return (True, 1, DIRY)


        # --- CORNERS
        # Top Left
        if self.__TOP_LEFT_CORNER.isCollision(WIDTH, HEIGHT, POS):
            if DIRX < 0 and DIRY > 0:
                return (True, DIRX , -1)

            elif DIRX > 0 and DIRY < 0:
                return (True, -1, DIRY)
            else:
                return (True, -1, -1)

        # Top Right
        if self.__TOP_RIGHT_CORNER.isCollision(WIDTH, HEIGHT, POS):

            if DIRX < 0 and DIRY < 0:
                return (True, 1, DIRY)

            elif DIRX > 0 and DIRY > 0:
                return (True, DIRX, -1)

            else:
                return (True, 1, -1)

        # Bottom Left
        if self.__BOTTOM_LEFT_CORNER.isCollision(WIDTH, HEIGHT, POS):
            if DIRX < 0 and DIRY < 0:
                return (True, DIRX, -1)

            elif DIRX > 0 and DIRY > 0:
                return (True, -1, DIRY)

            else:
                return (True, -1, 1)



        # Bottom Right
        if self.__BOTTOM_RIGHT_CORNER.isCollision(WIDTH, HEIGHT, POS):
            if DIRX < 0 and DIRY > 0:
                return (True, 1, DIRY)

            elif DIRX > 0 and DIRY < 0:
                return (True, DIRX, 1)

            else:
                return (True, 1, 1)



        return (False, False, False)








# For corners: if the block hits top right corner when the DIRY is negative and DIRX is positive, just make it posititive
if __name__ == "__main__":
    from window import Window
    pygame.init()
    WINDOW = Window("Asteroid Test", 800, 600, 30)
    BRICKS = []
    ball = Box(5, 5)

    for i in range(25):
        BRICKS.append(Brick(1.5))
    X = 0
    Y = 10
    START_X = 40
    BRICK_GAP = 40
    LAYERING = 5
    for BRICK in BRICKS:
        if X <= WINDOW.getWidth() - BRICK.getWidth():
            BRICK.setBrickPOS(X+START_X, Y)
            X += BRICK.getWidth() + BRICK_GAP

        else:
            X = 0
            Y += BRICK.getHeight() + BRICK_GAP
            LAYERING *= -1
            BRICK.setBrickPOS(X+START_X + LAYERING, Y)
            X += BRICK.getWidth() + BRICK_GAP

        BRICK.blitBrick()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        WINDOW.clearScreen()
        ball.bounceX(WINDOW.getWidth())
        ball.bounceY(WINDOW.getHeight())
        ball.checkBoundaries(WINDOW.getWidth(),WINDOW.getHeight())
        for BRICK in BRICKS:
            collision = BRICK.isBrickCollision(ball.getWidth(), ball.getHeight(), ball.getPOS())
            if collision[0]:
                ball.changeDirX(collision[1])
                ball.changeDirY(collision[2])


            BRICKS[i].blitBrick()
        WINDOW.getSurface().blit(ball.getSurface(), ball.getPOS())
        WINDOW.updateFrame()

        #

        