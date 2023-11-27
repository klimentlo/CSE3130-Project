# main.py

'''
title: Main program
author: kliment lo
date-created: 2023/11/06
'''
from game_engine import Game

class Main:
    def __init__(self):
        while True:
            self.__GAME = Game()
            self.__GAME.run()

if __name__ == "__main__":
    Main()