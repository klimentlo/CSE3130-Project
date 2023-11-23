# game_engine.py

'''
title: game engine for brick breaker
author: kliment lo
date-created: 2023/11/21
'''
import pygame
from player import Player
from window import Window
from box import Box
from text import Text
from color import Color
from brick import Brick
import random
pygame.init()


class Game:
    def __init__(self):
        # Player
        self.__WINDOW = Window("Brick Breaker", 800, 600, 60)
        self.__PLAYER = Player(10)
        self.__PLAYER.setPOS(self.__WINDOW.getWidth()//2 - self.__PLAYER.getWidth()//2, self.__WINDOW.getHeight()*0.9)

        # Ball
        self.__BALL = Box(10, 10)
        self.__BALL.setPOS(self.__WINDOW.getWidth()//2 - self.__BALL.getWidth()//2, self.__WINDOW.getHeight()*0.8)
        self.__BALL.setSpeed(30)
        # Title Bar & Text
        self.__TITLE_BAR = Box(self.__WINDOW.getWidth(), self.__WINDOW.getHeight() // 10)
        self.__TITLE_BAR.setColor(Color.BLACK)
        self.__TITLE_TEXT = Text("!Brick Breaker!")
        self.__TITLE_TEXT.setPOS(self.__WINDOW.getWidth() // 2 - self.__TITLE_TEXT.getWidth() // 2, 5)

        # Score
        self.__SCORE = 0
        self.__SCORE_TEXT = Text(f"SCORE: {self.__SCORE}")
        self.__SCORE_TEXT.setPOS(self.__WINDOW.getWidth() - self.__SCORE_TEXT.getWidth() - 5, 5)

        # Health Text
        self.__HEALTH_TEXT = Text("HEALTH: ")
        self.__HEALTH_TEXT.setY(5)

        # Health Bar
        self.__HEALTH_BAR = Box(self.__PLAYER.getHealth(), self.__WINDOW.getHeight() // 20)
        self.__HEALTH_BAR.setColor(Color.GREEN)
        self.__HEALTH_BAR.setPOS(self.__HEALTH_TEXT.getX() + self.__HEALTH_TEXT.getWidth() + 4, 15)

        # LEVEL
        self.__LEVEL = 1

        # Bricks
        self.__BRICKS = []
        self.__BRICKS_PER_ROW = 12
        self.__BRICK_SPACING = 10
        self.__TOTAL_BRICKS = 90
        for i in range (self.__TOTAL_BRICKS): #makes this many bricks
            self.__BRICKS.append(Brick(0.5))


        # BRICK ALIGNMENT BABY :D

        xBrickPlacement = (self.__WINDOW.getWidth() - ((self.__BRICKS[0].getWidth() + self.__BRICK_SPACING) * self.__BRICKS_PER_ROW))/2 + self.__BRICK_SPACING//2 # Makes it so the row of bricks will be aligned properly
        yBrickPlacement = self.__BRICKS[0].getHeight() + self.__BRICK_SPACING # makes it so its a brick and a bit away from the ceiling
        bricksPlaced = 0

        for BRICK in self.__BRICKS: # for amount of bricks
            if bricksPlaced != self.__BRICKS_PER_ROW:
                BRICK.setBrickPOS(xBrickPlacement, yBrickPlacement)
                BRICK.setPOS(xBrickPlacement, yBrickPlacement)
            else:
                yBrickPlacement += (BRICK.getHeight() + self.__BRICK_SPACING)
                xBrickPlacement = (self.__WINDOW.getWidth() - ((self.__BRICKS[0].getWidth() + self.__BRICK_SPACING) * self.__BRICKS_PER_ROW)) / 2 + self.__BRICK_SPACING // 2
                BRICK.setBrickPOS(xBrickPlacement, yBrickPlacement)
                BRICK.setPOS(xBrickPlacement, yBrickPlacement)
                bricksPlaced = 0

            xBrickPlacement += BRICK.getWidth() + self.__BRICK_SPACING  # how far the brick is placed away from the wall
            bricksPlaced += 1





    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            KEYS_PRESSED = pygame.key.get_pressed()
            self.__PLAYER.ADmove(KEYS_PRESSED)
            self.__PLAYER.checkBoundaries(self.__WINDOW.getWidth(), self.__WINDOW.getHeight())

            self.__BALL.bounceX(self.__WINDOW.getWidth())
            self.__BALL.bounceY(self.__WINDOW.getHeight())
            self.__BALL.checkBoundaries(self.__WINDOW.getWidth(), self.__WINDOW.getHeight())

            if self.__PLAYER.isCollision(self.__BALL.getWidth(), self.__BALL.getHeight(), self.__BALL.getPOS()):
                self.__BALL.changeDirY(-1)
                dirRandom = random.choice([0.01, -0.01])
                self.__BALL.changeDirForce(dirRandom)

            for BRICK in self.__BRICKS:
                collision = BRICK.isBrickCollision(self.__BALL.getWidth(), self.__BALL.getHeight(), self.__BALL.getPOS(), self.__BALL.getDirX(), self.__BALL.getDirY())
                if collision[0]: # collisions = [bool, float, float]      example:   [True, -1, 1]
                    self.__BALL.changeDirX(collision[1])
                    self.__BALL.changeDirY(collision[2])
                    BRICK.setBrickPOS(-100,-100)
                    BRICK.setPOS(-100, -100)

            self.__updateWindowFrame()




    def __updateWindowFrame(self):
        self.__WINDOW.clearScreen()

        for BRICK in self.__BRICKS:
            # Actual Brick
            self.__WINDOW.getSurface().blit(BRICK.getSurface(), BRICK.getPOS())

            # Side Brick
            self.__WINDOW.getSurface().blit(BRICK.getLeftSurface(), BRICK.getLeftPOS())
            self.__WINDOW.getSurface().blit(BRICK.getRightSurface(), BRICK.getRightPOS())
            self.__WINDOW.getSurface().blit(BRICK.getTopSurface(), BRICK.getTopPOS())
            self.__WINDOW.getSurface().blit(BRICK.getBottomSurface(), BRICK.getBottomPOS())

            # Corners
            self.__WINDOW.getSurface().blit(BRICK.getTopLeftSurface(), BRICK.getTopLeftPOS())
            self.__WINDOW.getSurface().blit(BRICK.getTopRightSurface(), BRICK.getTopRightPOS())
            self.__WINDOW.getSurface().blit(BRICK.getBottomLeftSurface(), BRICK.getBottomLeftPOS())
            self.__WINDOW.getSurface().blit(BRICK.getBottomRightSurface(), BRICK.getBottomRightPOS())

        # Player
        self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())
        self.__WINDOW.getSurface().blit(self.__BALL.getSurface(), self.__BALL.getPOS())




        self.__WINDOW.updateFrame()


if __name__ == "__main__":
    GAME = Game()
    GAME.run()

