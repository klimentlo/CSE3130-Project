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
pygame.init()


class Game:
    def __init__(self):
        # Player
        self.__WINDOW = Window("Brick Breaker", 800, 600, 60)
        self.__PLAYER = Player()
        self.__PLAYER.setPOS(self.__WINDOW.getWidth()//2 - self.__PLAYER.getWidth()//2, self.__WINDOW.getHeight()*0.9)

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

        # Bricks
        self.__BRICKS = []
        for i in range (50):
            self.__BRICKS.append(Brick())
        xDistance = 0
        yDistance = self.__BRICKS[0].getHeight() + 5
        blocksPerRow = 0
        rowNum = 1
        for BRICK in self.__BRICKS:
            blocksPerRow += 1
            if rowNum > 0:
                initialPlacement = 0
            else:
                intialPlacement = BRICK.getWidth()//2

            xDistance += BRICK.getWidth() + 5 + initialPlacement
            BRICK.setPOS(xDistance, yDistance)
            if blocksPerRow == 6:
                blocksPerRow = 0
                xDistance = 0
                yDistance += self.__BRICKS[0].getHeight() + 5
                rowNum *= -1


    def blitBrick(self):
        # Brick
        # Sides
        self.__WINDOW.getSurface().blit(self.__BRICK.getLeftSurface(), self.__BRICK.getLeftPOS())
        self.__WINDOW.getSurface().blit(self.__BRICK.getRightSurface(), self.__BRICK.getRightPOS())
        self.__WINDOW.getSurface().blit(self.__BRICK.getTopSurface(), self.__BRICK.getTopPOS())
        self.__WINDOW.getSurface().blit(self.__BRICK.getBottomSurface(), self.__BRICK.getBottomPOS())

        # Corners
        self.__WINDOW.getSurface().blit(self.__BRICK.getTopLeftSurface(), self.__BRICK.getTopLeftPOS())
        self.__WINDOW.getSurface().blit(self.__BRICK.getTopRightSurface(), self.__BRICK.getTopRightPOS())
        self.__WINDOW.getSurface().blit(self.__BRICK.getBottomLeftSurface(), self.__BRICK.getBottomLeftPOS())
        self.__WINDOW.getSurface().blit(self.__BRICK.getBottomRightSurface(), self.__BRICK.getBottomRightPOS())
        self.__WINDOW.getSurface().blit(self.__BRICK.getSurface(), self.__BRICK.getPOS())

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #        WINDOW.clearScreen()
            #        ball.bounceX(WINDOW.getWidth())
            #        ball.bounceY(WINDOW.getHeight())
            #        ball.checkBoundaries(WINDOW.getWidth(), WINDOW.getHeight())
            #        for BRICK in BRICKS:
            #            collision = BRICK.isBrickCollision(ball.getWidth(), ball.getHeight(), ball.getPOS())
            #            if collision[0]:
            #                ball.changeDirX(collision[1])
            #                ball.changeDirY(collision[2])

            #            BRICKS[i].blitBrick()
            #        WINDOW.getSurface().blit(ball.getSurface(), ball.getPOS())
            #        WINDOW.updateFrame()


            self.__WINDOW.clearScreen()
            for BRICK in self.__BRICKS:
                BRICK.blitBrick()
            self.WINDOW.updateFrame()

if __name__ == "__main__":
    GAME = Game()
    GAME.run()

