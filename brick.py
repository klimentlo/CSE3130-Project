#brick.py
from my_sprite import MySprite
from box import Box
import pygame
from color import Color


class Brick(MySprite):
    def __init__(self):
        MySprite.__init__(self)

        self.__BRICK_SPRITE = Box(100, 50)
        self._SURFACE = self.__BRICK_SPRITE.getSurface()


        # Top collision box
        self.__BRICK_TOP = Box(90, 5)
        self.__BRICK_TOP.setColor(Color.RED)

        # Bottom collision box
        self.__BRICK_BOTTOM = Box(90, 5)
        self.__BRICK_BOTTOM.setColor(Color.RED)

        # Left collision box
        self.__BRICK_LEFT = Box(5, 40)
        self.__BRICK_LEFT.setColor(Color.BLUE)

        # Right collision box
        self.__BRICK_RIGHT = Box(5, 40)
        self.__BRICK_RIGHT.setColor(Color.BLUE)

        # CORNERS :(
        self.__TOP_LEFT_CORNER = Box(5, 5)
        self.__TOP_LEFT_CORNER.setColor(Color.GREEN)

        self.__TOP_RIGHT_CORNER = Box(5, 5)
        self.__TOP_RIGHT_CORNER.setColor(Color.GREEN)

        self.__BOTTOM_LEFT_CORNER = Box(5, 5)
        self.__BOTTOM_LEFT_CORNER.setColor(Color.GREEN)

        self.__BOTTOM_RIGHT_CORNER = Box(5, 5)
        self.__BOTTOM_RIGHT_CORNER.setColor(Color.GREEN)



    # SIDES
    def getTopSurface(self):
        return self.__BRICK_TOP.getSurface()

    def getTopPOS(self):
        return self.__BRICK_TOP.getPOS()

    def getBottomSurface(self):
        return self.__BRICK_BOTTOM.getSurface()

    def getBottomPOS(self):
        return self.__BRICK_BOTTOM.getPOS()

    def getLeftSurface(self):
        return self.__BRICK_LEFT.getSurface()

    def getLeftPOS(self):
        return self.__BRICK_LEFT.getPOS()

    def getRightSurface(self):
        return self.__BRICK_RIGHT.getSurface()

    def getRightPOS(self):
        return self.__BRICK_RIGHT.getPOS()

    # CORNERS

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



    def setBrickPOS(self, X=100, Y=100):
        '''
        sets all collision boxes and surfaces to the set location :D
        :param X:
        :param Y:
        :return:
        '''

        BRICK.setPOS(X, Y)
        # Sides         If this\/ doesn't work, change the X to Brick.getX() :D
        self.__BRICK_TOP.setPOS(X + BRICK.getWidth()//2 - self.__BRICK_TOP.getWidth()//2, Y)
        self.__BRICK_BOTTOM.setPOS(X + BRICK.getWidth()//2 - self.__BRICK_TOP.getWidth()//2, Y+self.__BRICK_SPRITE.getHeight()-self.__BRICK_BOTTOM.getHeight())
        self.__BRICK_LEFT.setPOS(X, Y + BRICK.getHeight()//2-self.__BRICK_BOTTOM.getHeight()//2)
        self.__BRICK_RIGHT.setPOS(X + self.__BRICK_SPRITE.getWidth()-self.__BRICK_RIGHT.getWidth(), BRICK.getHeight()//2-self.__BRICK_BOTTOM.getHeight()//2)
        
        # Corners
        self.__TOP_LEFT_CORNER.setPOS(X, Y)
        self.__TOP_RIGHT_CORNER.setPOS(X + BRICK.getWidth()-self.__TOP_RIGHT_CORNER.getWidth(),Y)
        self.__BOTTOM_LEFT_CORNER.setPOS(X, Y + BRICK.getHeight()-self.__BOTTOM_LEFT_CORNER.getHeight())
        self.__BOTTOM_RIGHT_CORNER.setPOS(X + BRICK.getWidth()-self.__BOTTOM_RIGHT_CORNER.getWidth(), Y + BRICK.getHeight()-self.__BOTTOM_RIGHT_CORNER.getHeight())

        
        
    def blitBrick(self):
      
        # Brick
        WINDOW.getSurface().blit(BRICK.getSurface(), BRICK.getPOS())
        
        # Sides
        WINDOW.getSurface().blit(BRICK.getLeftSurface(), BRICK.getLeftPOS())
        WINDOW.getSurface().blit(BRICK.getRightSurface(), BRICK.getRightPOS())
        WINDOW.getSurface().blit(BRICK.getTopSurface(), BRICK.getTopPOS())
        WINDOW.getSurface().blit(BRICK.getBottomSurface(), BRICK.getBottomPOS())
        
        # Corners
        WINDOW.getSurface().blit(BRICK.getTopLeftSurface, BRICK.getTopLeftPOS())
        WINDOW.getSurface().blit(BRICK.getTopRightSurface, BRICK.getTopRightPOS()())
        WINDOW.getSurface().blit(BRICK.getBottomLeftSurface, BRICK.getBottomLeftPOS())
        WINDOW.getSurface().blit(BRICK.getBottomRightSurface, BRICK.getBottomRightPOS())






if __name__ == "__main__":
    from window import Window
    pygame.init()
    WINDOW = Window("Asteroid Test", 800, 600, 30)
    BRICK = Brick()
    BRICK.setBrickPOS(50,50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        WINDOW.clearScreen()
        BRICK.blitBrick()
        WINDOW.updateFrame()

        