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
from ball import Ball
import random
import time
pygame.init()


class Game:
    def __init__(self):
        # Player
        self.__WINDOW = Window("Brick Breaker", 800, 600, 60)
        self.__PLAYER = Player(10)
        self.__PLAYER.setPOS(self.__WINDOW.getWidth()//2 - self.__PLAYER.getWidth()//2, self.__WINDOW.getHeight()*0.9)

        self.__START_LEVEL = False
        self.__additionalBallTimer = time.time()

        # Ball
        self.__TOTAL_BALLS = 1
        self.__BALLS = []

        for i in range(self.__TOTAL_BALLS):
            self.__BALLS.append(Ball())
            self.__BALLS[i].setPOS(self.__WINDOW.getWidth()//2 - self.__BALLS[0].getWidth()//2, self.__WINDOW.getHeight()*0.7)
            self.__BALLS[i].setSpeed(4)

        # Title Bar & Text
        self.__TITLE_BAR = Box(self.__WINDOW.getWidth(), self.__WINDOW.getHeight() // 10)
        self.__TITLE_BAR.setColor(Color.BLACK)
        self.__TITLE_TEXT = Text("!Brick Breaker!")
        self.__TITLE_TEXT.setPOS(self.__WINDOW.getWidth() // 2 - self.__TITLE_TEXT.getWidth() // 2, 5)

        # Score
        self.__SCORE = 0
        self.__SCORE_TEXT = Text(f"SCORE: {self.__SCORE}")
        self.__SCORE_TEXT.setPOS(self.__WINDOW.getWidth() - self.__SCORE_TEXT.getWidth() - 5, 5)

        # LIVES Text
        self.__LIVES_TEXT = Text("LIVES: ")
        self.__LIVES_TEXT.setY(5)

        # LIVES Bar
        self.__LIVES_BAR = Box(self.__PLAYER.getLives(), self.__WINDOW.getHeight() // 20)
        self.__LIVES_BAR.setColor(Color.GREEN)
        self.__LIVES_BAR.setPOS(self.__LIVES_TEXT.getX() + self.__LIVES_TEXT.getWidth() + 4, 15)

        # LEVEL
        self.__LEVEL = 1

        self.__levelConsuctor()










    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            self.__startLevel()
            if self.__START_LEVEL == True:
                self.__bonusBallTimer()

                KEYS_PRESSED = pygame.key.get_pressed()
                self.__PLAYER.ADmove(KEYS_PRESSED)
                self.__PLAYER.checkBoundaries(self.__WINDOW.getWidth(), self.__WINDOW.getHeight())
                self.__checkDeadBalls()
                for i in range(len(self.__BALLS) - 1, -1, -1):
                    self.__playerBallCollisions(i)
                    self.__ballBrickCollisions(i)

                if self.__TOTAL_BRICKS <= 0:
                    self.__LEVEL += 1
                    self.__resetLevel()
                    self.__levelConsuctor()

                if self.__PLAYER.getLives() <= 0:
                    print("Game Over")



            self.__updateWindowFrame()







    # COLLISIONS

    def __playerBallCollisions(self, i):
        if self.__PLAYER.isCollision(self.__BALLS[i].getWidth(), self.__BALLS[i].getHeight(), self.__BALLS[i].getPOS()):
            self.__BALLS[i].changeDirY(-1)
            dirRandom = random.choice([0.01, -0.01])
            self.__BALLS[i].changeDirForce(dirRandom)
            self.__BALLS[i].setPOS(self.__BALLS[i].getX(), self.__BALLS[
                i].getY() - 5)  # makes it so if you collide with it from the side, it won't glitch like crazy

    def __ballBrickCollisions(self, i):
        for BRICK in self.__BRICKS:
            collision = BRICK.isBrickCollision(self.__BALLS[i].getWidth(), self.__BALLS[i].getHeight(),
                                               self.__BALLS[i].getPOS(), self.__BALLS[i].getDirX(),
                                               self.__BALLS[i].getDirY())
            if collision[0]:  # collisions = [bool, float, float]      example:   [True, -1, 1]
                self.__BALLS[i].changeDirX(collision[1])
                self.__BALLS[i].changeDirY(collision[2])
                self.__TOTAL_BRICKS -= 1
                BRICK.setBrickPOS(-100, -100)
                BRICK.setPOS(-100, -100)

    # LOST BALLS

    def __levelConsuctor(self):
        # Bricks
        self.__BRICKS = []
        try:
            while LEVEL_CONFIG[4] == self.__PREVIOUS_LEVEL: # while the level is the same as the last one, keep rolling
                LEVEL_CONFIG = random.choice([(6, 5, 24, 1, "v1"), (4, 5, 32, 0.8, "v2"), (8, 5, 56, 0.7, "v3"), (10, 5, 100, 0.4, "v4")])
        except UnboundLocalError:
            LEVEL_CONFIG = random.choice([(6, 5, 24, 1, "v1"), (4, 5, 32, 0.8, "v2"), (8, 5, 56, 0.7, "v3"), (10, 5, 100, 0.4, "v4")])


        self.__BRICKS_PER_ROW = LEVEL_CONFIG[0]
        self.__BRICK_SPACING = LEVEL_CONFIG[1]
        self.__TOTAL_BRICKS = LEVEL_CONFIG[2]
        self.__BRICK_RATIO = LEVEL_CONFIG[3]
        for i in range(self.__TOTAL_BRICKS):  # makes this many bricks
            self.__BRICKS.append(Brick(self.__BRICK_RATIO))
        self.__PREVIOUS_LEVEL = LEVEL_CONFIG[4]


        # BRICK ALIGNMENT BABY :D

        xBrickPlacement = (self.__WINDOW.getWidth() - ((self.__BRICKS[0].getWidth() + self.__BRICK_SPACING) * self.__BRICKS_PER_ROW)) / 2 + self.__BRICK_SPACING // 2  # Makes it so the row of bricks will be aligned properly
        yBrickPlacement = self.__BRICKS[0].getHeight() + self.__BRICK_SPACING  # makes it so its a brick and a bit away from the ceiling
        bricksPlaced = 0

        for BRICK in self.__BRICKS:  # for amount of bricks
            if bricksPlaced != self.__BRICKS_PER_ROW:
                BRICK.setBrickPOS(xBrickPlacement, yBrickPlacement)
                BRICK.setPOS(xBrickPlacement, yBrickPlacement)
            else:
                yBrickPlacement += (BRICK.getHeight() + self.__BRICK_SPACING)
                xBrickPlacement = (self.__WINDOW.getWidth() - ((self.__BRICKS[
                                                                    0].getWidth() + self.__BRICK_SPACING) * self.__BRICKS_PER_ROW)) / 2 + self.__BRICK_SPACING // 2
                BRICK.setBrickPOS(xBrickPlacement, yBrickPlacement)
                BRICK.setPOS(xBrickPlacement, yBrickPlacement)
                bricksPlaced = 0

            xBrickPlacement += BRICK.getWidth() + self.__BRICK_SPACING  # how far the brick is placed away from the wall
            bricksPlaced += 1



    def __checkDeadBalls(self):
        for i in range(len(self.__BALLS) - 1, -1,-1):  # scans backwards so when a ball gets popped, doesnt affect anything
            self.__BALLS[i].bounceX(self.__WINDOW.getWidth())
            self.__BALLS[i].bounceY(self.__WINDOW.getHeight())
            if self.__BALLS[i].isLost(self.__WINDOW.getWidth(), self.__WINDOW.getHeight()):
                self.__BALLS.pop(i)
                if i == 0:  # if it was our first original ball
                    self.__PLAYER.loseLife()
                    self.__resetLevel()



    def __startLevel(self):
        KEYS_PRESSED = pygame.key.get_pressed()
        if KEYS_PRESSED[pygame.K_SPACE] == 1:
            print("space hit")
            self.__BALLS[0].setSpeed(4)
            self.__additionalBallTimer = time.time()
            self.__START_LEVEL = True


    def __bonusBallTimer(self):
        if time.time() > self.__additionalBallTimer + 0.1:
            self.__BALLS.append(Ball("BonusBall", 4))

            self.__additionalBallTimer = time.time()


    def __resetLevel(self):
        self.__START_LEVEL = False
        self.__BALLS = [Ball()]
        self.__BALLS[0].setPOS(self.__WINDOW.getWidth()//2 - self.__BALLS[0].getWidth()//2, self.__WINDOW.getHeight()*0.7)
        self.__PLAYER.setPOS(self.__WINDOW.getWidth()//2 - self.__PLAYER.getWidth()//2, self.__WINDOW.getHeight()*0.9)


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

        # Ball
        for BALL in self.__BALLS:
            self.__WINDOW.getSurface().blit(BALL.getSurface(), BALL.getPOS())




        self.__WINDOW.updateFrame()


if __name__ == "__main__":
    GAME = Game()
    GAME.run()

