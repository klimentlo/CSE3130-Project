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
        self.__GAME_OVER = False
        self.__additionalBallTimer = time.time()

        # Ball
        self.__TOTAL_BALLS = 1
        self.__BALLS = []

        for i in range(self.__TOTAL_BALLS):
            self.__BALLS.append(Ball())
            self.__BALLS[i].setPOS(self.__WINDOW.getWidth()//2 - self.__BALLS[0].getWidth()//2, self.__WINDOW.getHeight()*0.85)
            self.__BALLS[i].setSpeed(4)

        # Title Bar & Text
        self.__TITLE_BAR = Box(self.__WINDOW.getWidth(), self.__WINDOW.getHeight() // 15)
        self.__TITLE_BAR.setColor(Color.BLACK)
        self.__TITLE_TEXT = Text("Brick Breaker")
        self.__TITLE_TEXT.setPOS(self.__WINDOW.getWidth() // 2 - self.__TITLE_TEXT.getWidth() // 2, 5)

        # Intro Text
        self.__INTRO_TEXT = Text("Press SPACE to start!")
        self.__INTRO_TEXT.setPOS(self.__WINDOW.getWidth()//2 - self.__INTRO_TEXT.getWidth()//2, self.__WINDOW.getHeight()*0.75)

        # GameOver Text
        self.__GAME_OVER_TEXT = Text("GAME OVER", "Arial", 100)
        self.__GAME_OVER_TEXT.setPOS(-100, -100)

        # Score
        self.__SCORE = 0
        self.__SCORE_TEXT = Text(f"SCORE: {self.__SCORE}")
        self.__SCORE_TEXT.setPOS(self.__WINDOW.getWidth() - self.__SCORE_TEXT.getWidth() - 10, 5)


        # Lives Text
        self.__LIVES_TEXT = Text(f"LIVES: {self.__PLAYER.getLives()}")
        self.__LIVES_TEXT.setPOS(10, 5)

        # Round``
        self.__ROUND = 1

        #
        self.__ROUND_TEXT = Text(f"Round {self.__ROUND}")
        self.__ROUND_TEXT.setPOS(-100,-100)

        self.__roundConsuctor()







# basically everything is encapsulated
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            self.__startLevel()
            if self.__GAME_OVER != True:
                if self.__START_LEVEL == True:
                    self.__bonusBallTimer(15)

                    KEYS_PRESSED = pygame.key.get_pressed()
                    self.__PLAYER.ADmove(KEYS_PRESSED)
                    self.__PLAYER.checkBoundaries(self.__WINDOW.getWidth(), self.__WINDOW.getHeight())

                    for i in range(len(self.__BALLS) - 1, -1, -1):
                        self.__playerBallCollisions(i) # < AGGREGATION
                        self.__ballBrickCollisions(i)# < AGGREGATION

                    self.__checkDeadBalls()  # checks if any have died

                    if self.__TOTAL_BRICKS <= 0:
                        self.__ROUND += 1
                        self.__resetLevel()
                        self.__roundConsuctor()

                    if self.__PLAYER.getLives() <= 0:
                        self.__GAME_OVER = True
            else:
                if self.__gameOver() == "break":
                    time.sleep(0.1)
                    break



            self.__updateWindowFrame()







    # - - - COLLISIONS

    def __playerBallCollisions(self, i):
        if self.__PLAYER.isCollision(self.__BALLS[i].getWidth(), self.__BALLS[i].getHeight(), self.__BALLS[i].getPOS()):
            self.__BALLS[i].changeDirY(-1)
            dirRandom = random.choice([0.01, -0.01])
            self.__BALLS[i].changeDirForce(dirRandom)
            self.__BALLS[i].setPOS(self.__BALLS[i].getX(), self.__BALLS[i].getY() - 5)  # makes it so if you collide with it from the side, it won't glitch like crazy



    def __ballBrickCollisions(self, i):
        for BRICK in self.__BRICKS:
            collision = BRICK.isBrickCollision(self.__BALLS[i].getWidth(), self.__BALLS[i].getHeight(), self.__BALLS[i].getPOS(), self.__BALLS[i].getDirX(), self.__BALLS[i].getDirY())
            if collision[0]:  # collisions = [bool, float, float]      example:   [True, -1, 1]
                self.__BALLS[i].setDirX(collision[1])
                self.__BALLS[i].setDirY(collision[2])
                self.__TOTAL_BRICKS -= 1
                BRICK.setBrickPOS(-100, -100)
                BRICK.setPOS(-100, -100)
                # updates score
                self.__SCORE += 10
                self.__SCORE_TEXT.setText(f"Score: {self.__SCORE}")
                self.__SCORE_TEXT.setX(self.__WINDOW.getWidth() - self.__SCORE_TEXT.getWidth() - 10)



    # - - - Level Related

    def __roundConsuctor(self):
        # Bricks
        self.__BRICKS = []
        try:
            while LEVEL_CONFIG[4] == self.__PREVIOUS_LEVEL: # while the level is the same as the last one, keep rolling
                LEVEL_CONFIG = random.choice([(6, 5, 24, 1, "v1"), (4, 5, 32, 0.8, "v2"), (8, 5, 56, 0.7, "v3"), (10, 5, 100, 0.4, "v4")])
                if LEVEL_CONFIG[4] == self.__PREVIOUS_LEVEL:
                    LEVEL_CONFIG = random.choice([(6, 5, 24, 1, "v1"), (4, 5, 32, 0.8, "v2"), (8, 5, 56, 0.7, "v3"), (10, 5, 100, 0.4, "v4")])

        except UnboundLocalError:
            LEVEL_CONFIG = random.choice([(6, 5, 24, 1, "v1"), (8, 20, 24, 0.8, "v2"), (8, 5, 56, 0.7, "v3"), (10, 10, 100, 0.4, "v4")])
        self.__PREVIOUS_LEVEL = LEVEL_CONFIG[4]


        self.__BRICKS_PER_ROW = LEVEL_CONFIG[0]
        self.__BRICK_SPACING = LEVEL_CONFIG[1]
        self.__TOTAL_BRICKS = LEVEL_CONFIG[2]
        self.__BRICK_RATIO = LEVEL_CONFIG[3]
        for i in range(self.__TOTAL_BRICKS):  # makes this many bricks
            self.__BRICKS.append(Brick(self.__BRICK_RATIO))


        # BRICK ALIGNMENT BABY :D

        xBrickPlacement = (self.__WINDOW.getWidth() - ((self.__BRICKS[0].getWidth() + self.__BRICK_SPACING) * self.__BRICKS_PER_ROW)) / 2 + self.__BRICK_SPACING // 2  # Makes it so the row of bricks will be aligned properly
        yBrickPlacement = self.__BRICKS[0].getHeight() + self.__BRICK_SPACING + self.__TITLE_BAR.getHeight() # makes it so its a brick and a bit away from the ceiling
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


    def __startLevel(self):
        KEYS_PRESSED = pygame.key.get_pressed()
        if KEYS_PRESSED[pygame.K_SPACE] == 1:
            self.__BALLS[0].setSpeed(4)
            self.__additionalBallTimer = time.time()
            self.__START_LEVEL = True
            self.__INTRO_TEXT.setPOS(-50, -50)



    def __resetLevel(self):
        self.__START_LEVEL = False
        self.__BALLS = [Ball()]
        self.__BALLS[0].setPOS(self.__WINDOW.getWidth() // 2 - self.__BALLS[0].getWidth() // 2,
                               self.__WINDOW.getHeight() * 0.85)
        self.__PLAYER.setPOS(self.__WINDOW.getWidth() // 2 - self.__PLAYER.getWidth() // 2,
                             self.__WINDOW.getHeight() * 0.9)

    def __gameOver(self):
        self.__GAME_OVER_TEXT.setPOS(self.__WINDOW.getWidth()//2-self.__GAME_OVER_TEXT.getWidth()//2, self.__WINDOW.getHeight()//2-self.__GAME_OVER_TEXT.getHeight()//2)
        self.__INTRO_TEXT = Text("Press SPACE to play again!")
        self.__INTRO_TEXT.setPOS(self.__WINDOW.getWidth() // 2 - self.__INTRO_TEXT.getWidth() // 2, self.__WINDOW.getHeight() * 0.75)
        REPLAY = pygame.key.get_pressed()
        if REPLAY[pygame.K_SPACE] == 1:
            return "break"

        for BRICK in self.__BRICKS:
            BRICK.setBrickPOS(-100, -100)
            BRICK.setPOS(-100, -100)


# - - - Balls
    def __checkDeadBalls(self):
        for i in range(len(self.__BALLS) - 1, -1,-1):  # scans backwards so when a ball gets popped, doesnt affect anything
            self.__BALLS[i].bounceX(self.__WINDOW.getWidth())
            self.__BALLS[i].bounceY(self.__WINDOW.getHeight(), self.__TITLE_BAR.getX()+self.__TITLE_BAR.getHeight())
            if self.__BALLS[i].isLost(self.__WINDOW.getWidth(), self.__WINDOW.getHeight()):
                self.__BALLS.pop(i)
                if i == 0:  # if it was our first original ball
                    self.__PLAYER.loseLife()
                    self.__resetLevel()
                    self.__LIVES_TEXT.setText(f"LIVES: {self.__PLAYER.getLives()}")


    def __bonusBallTimer(self, DURATION):
        if time.time() > self.__additionalBallTimer + DURATION:
            self.__BALLS.append(Ball("BonusBall", 4))
            self.__additionalBallTimer = time.time()




    def __updateWindowFrame(self):
        self.__WINDOW.clearScreen()
        self.__WINDOW.getSurface().blit(self.__TITLE_BAR.getSurface(), self.__TITLE_BAR.getPOS())
        self.__WINDOW.getSurface().blit(self.__TITLE_TEXT.getSurface(), self.__TITLE_TEXT.getPOS())
        self.__WINDOW.getSurface().blit(self.__SCORE_TEXT.getSurface(), self.__SCORE_TEXT.getPOS())
        self.__WINDOW.getSurface().blit(self.__LIVES_TEXT.getSurface(), self.__LIVES_TEXT.getPOS())
        self.__WINDOW.getSurface().blit(self.__INTRO_TEXT.getSurface(), self.__INTRO_TEXT.getPOS())
        for BRICK in self.__BRICKS:


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

            # Actual Brick
            self.__WINDOW.getSurface().blit(BRICK.getSurface(), BRICK.getPOS())

        # Player
        self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())

        # Ball
        for BALL in self.__BALLS:
            self.__WINDOW.getSurface().blit(BALL.getSurface(), BALL.getPOS())

        self.__WINDOW.getSurface().blit(self.__GAME_OVER_TEXT.getSurface(), self.__GAME_OVER_TEXT.getPOS())
        self.__WINDOW.getSurface().blit(self.__ROUND_TEXT.getSurface(), self.__ROUND_TEXT.getPOS())

        self.__WINDOW.updateFrame()


if __name__ == "__main__":
    GAME = Game()
    GAME.run()

