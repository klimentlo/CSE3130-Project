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
        # Window
        self.__WINDOW = Window("Brick Breaker", 800, 600, 60)

        # Player

        self.__PLAYER = Player(10)
        self.__PLAYER.setPOS(self.__WINDOW.getWidth()//2 - self.__PLAYER.getWidth()//2, self.__WINDOW.getHeight()*0.9)

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

        # Score & Text
        self.__SCORE = 0
        self.__SCORE_TEXT = Text(f"SCORE: {self.__SCORE}")
        self.__SCORE_TEXT.setPOS(self.__WINDOW.getWidth() - self.__SCORE_TEXT.getWidth() - 10, 5)


        # Lives Text
        self.__LIVES_TEXT = Text(f"LIVES: {self.__PLAYER.getLives()}")
        self.__LIVES_TEXT.setPOS(10, 5)

        # Round & Text
        self.__ROUND = 1
        self.__ROUND_TEXT = Text(f"Round {self.__ROUND}")
        self.__ROUND_TEXT.setPOS(-100,-100)

        self.__roundConsuctor()
        self.__START_LEVEL = False
        self.__GAME_OVER = False
        self.__additionalBallTimer = time.time()







# basically everything is encapsulated (self.__bonusBallTimer())
                                        #    ^^
                                        # Encapsulation

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            self.__startLevel() # Game will only start if space bar is pressed
            if self.__GAME_OVER != True: # if its not game over
                if self.__START_LEVEL == True: # if they want to start the game
                    self.__bonusBallTimer(15) # begin timer for bonus ball (15 seconds)

                    KEYS_PRESSED = pygame.key.get_pressed() # gets key pressed
                    self.__PLAYER.ADmove(KEYS_PRESSED) # if desired key is pressed, move side to side
                    self.__PLAYER.checkBoundaries(self.__WINDOW.getWidth(), self.__WINDOW.getHeight()) # keeps the player bar in boundaries

                    for i in range(len(self.__BALLS) - 1, -1, -1): # runs backwards because inside the function, there are objects that get popped off.
                        self.__playerBallCollisions(i) # < AGGREGATION # Tracks collision between player and ball
                        self.__ballBrickCollisions(i)# < AGGREGATION # Tracks collision between ball and brick

                    self.__checkDeadBalls()  # checks if any balls have died at the bottom, and if the main one did die, we lose a life and all balls reset.

                    if self.__TOTAL_BRICKS <= 0: # if all bricks are dead
                        self.__ROUND += 1 # proceed to next round
                        self.__resetLevel() # resets ball POS and player POS, and also allows user to play when they hit space (and not instantly allow the ball to move again)
                        self.__roundConsuctor() # constructs another map, makes sure its not the same one

                    if self.__PLAYER.getLives() <= 0: # if they lose all lives
                        self.__GAME_OVER = True # make it game over :(
            else:
                if self.__gameOver() == "break": # asks if the user wants to play again, if they do, self.__gameOver retuns "break", which will allow the game to run again
                    time.sleep(0.5) # so the ball doesn't immediately fly out
                    break



            self.__updateWindowFrame() # updates, blits, and clears everything on the screen







    # - - - COLLISIONS
    # Processing
    def __playerBallCollisions(self, i): # is in a for i loop
        if self.__PLAYER.isCollision(self.__BALLS[i].getWidth(), self.__BALLS[i].getHeight(), self.__BALLS[i].getPOS()): # if it collides
            self.__BALLS[i].changeDirY(-1) # reverse the y direction ( makes it go updwards)
            dirRandom = random.choice([0.01, -0.01])  # this is to reduce the chances of an infinite loop of missing a brick
            self.__BALLS[i].changeDirForce(dirRandom) # applies those changes via adding to dir value
            self.__BALLS[i].setPOS(self.__BALLS[i].getX(), self.__BALLS[i].getY() - 5)  # makes it so if you collide with it from the side, it won't glitch like crazy



    def __ballBrickCollisions(self, i):
        for BRICK in self.__BRICKS: # for amoutn of bricks
            collision = BRICK.isBrickCollision(self.__BALLS[i].getWidth(), self.__BALLS[i].getHeight(), self.__BALLS[i].getPOS(), self.__BALLS[i].getDirX(), self.__BALLS[i].getDirY()) # check if it collided
            if collision[0]:  # collisions = [bool, float, float]      example:   [True, -1, 1]  # if it did
                self.__BALLS[i].setDirX(collision[1]) # make ball go in desired direction
                self.__BALLS[i].setDirY(collision[2]) # make ball go in desired  direction
                self.__TOTAL_BRICKS -= 1 # minus one brick
                BRICK.setBrickPOS(-100, -100) # takes collision boxes of the screen
                BRICK.setPOS(-100, -100) # takes actual brick off screen
                # updates score
                self.__SCORE += 10 # adds score
                self.__SCORE_TEXT.setText(f"Score: {self.__SCORE}") # updates score text
                self.__SCORE_TEXT.setX(self.__WINDOW.getWidth() - self.__SCORE_TEXT.getWidth() - 10) # Makes sure score is in frame



    # - - - Level Related

    def __roundConsuctor(self):
        # Bricks
        self.__BRICKS = []
        self.__PREVIOUS_LEVEL = (6, 5, 24, 1, "v1")
        LEVEL_CONFIG = random.choice([(6, 5, 24, 1, "v1"), (4, 5, 32, 0.8, "v2"), (8, 5, 56, 0.7, "v3")])  # (10, 5, 100, 0.4, "v4")
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
                yBrickPlacement += (BRICK.getHeight() + self.__BRICK_SPACING) # moves it down by a brick and a bit
                xBrickPlacement = (self.__WINDOW.getWidth() - ((self.__BRICKS[0].getWidth() + self.__BRICK_SPACING) * self.__BRICKS_PER_ROW)) / 2 + self.__BRICK_SPACING // 2 # all bricks are evenly spready out and in the middle of the screen
                BRICK.setBrickPOS(xBrickPlacement, yBrickPlacement)
                BRICK.setPOS(xBrickPlacement, yBrickPlacement)
                bricksPlaced = 0

            xBrickPlacement += BRICK.getWidth() + self.__BRICK_SPACING  # how far the brick is placed one another
            bricksPlaced += 1


    def __startLevel(self):
        KEYS_PRESSED = pygame.key.get_pressed()
        if KEYS_PRESSED[pygame.K_SPACE] == 1:
            self.__BALLS[0].setSpeed(4) # makes the ball move
            self.__additionalBallTimer = time.time() # starts timer
            self.__START_LEVEL = True # allows game to run
            self.__INTRO_TEXT.setPOS(-50, -50) # take intro text away



    def __resetLevel(self):
        self.__START_LEVEL = False # stops level
        self.__BALLS = [Ball()] # only main ball
        self.__BALLS[0].setPOS(self.__WINDOW.getWidth() // 2 - self.__BALLS[0].getWidth() // 2, # center it
                               self.__WINDOW.getHeight() * 0.85)
        self.__PLAYER.setPOS(self.__WINDOW.getWidth() // 2 - self.__PLAYER.getWidth() // 2, # center it
                             self.__WINDOW.getHeight() * 0.9)

    def __gameOver(self):

        for BRICK in self.__BRICKS: # reomves all brick form screen
            BRICK.setBrickPOS(-100, -100)
            BRICK.setPOS(-100, -100)


        self.__GAME_OVER_TEXT.setPOS(self.__WINDOW.getWidth()//2-self.__GAME_OVER_TEXT.getWidth()//2, self.__WINDOW.getHeight()//2-self.__GAME_OVER_TEXT.getHeight()//2) # center over text
        self.__INTRO_TEXT = Text("Press SPACE to play again!")
        self.__INTRO_TEXT.setPOS(self.__WINDOW.getWidth() // 2 - self.__INTRO_TEXT.getWidth() // 2, self.__WINDOW.getHeight() * 0.75)
        self.__PLAYER.setPOS(-100, -100)
        self.__BALLS[0].setPOS(-100, -100)
        REPLAY = pygame.key.get_pressed()
        if REPLAY[pygame.K_SPACE] == 1:
            return "break" # reruns game




# - - - Balls
    def __checkDeadBalls(self):
        for i in range(len(self.__BALLS) - 1, -1,-1):  # scans backwards so when a ball gets popped, doesnt affect anything
            self.__BALLS[i].bounceX(self.__WINDOW.getWidth())
            self.__BALLS[i].bounceY(self.__WINDOW.getHeight(), self.__TITLE_BAR.getX()+self.__TITLE_BAR.getHeight())
            if self.__BALLS[i].isLost(self.__WINDOW.getWidth(), self.__WINDOW.getHeight()):
                self.__BALLS.pop(i) # removes ball from pygame
                if i == 0:  # if it was our first original ball
                    self.__PLAYER.loseLife() # if it was main ball, player lsoes a life
                    self.__resetLevel() # balls are all removed, with the main one returning to center, and so does the palyer
                    self.__LIVES_TEXT.setText(f"LIVES: {self.__PLAYER.getLives()}")


    def __bonusBallTimer(self, DURATION):
        if time.time() > self.__additionalBallTimer + DURATION: # when desired amoutn of time has passed
            self.__BALLS.append(Ball("BonusBall", 4))
            self.__additionalBallTimer = time.time() # resetcs timer




    def __updateWindowFrame(self): # blits everyhting on to screen
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

