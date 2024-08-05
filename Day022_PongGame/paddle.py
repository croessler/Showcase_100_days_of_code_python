"""This module provides the paddle class for the Pong game"""

from turtle import Turtle

STEP_LENGTH = 30

class Paddle(Turtle):
    """ Paddle class for Pong"""
    def __init__(self,side,x_cor):
        super().__init__()
        self.penup()
        #self.shape("square")
        self.color("white")
        self.shape("square")
        self.shapesize(1,5)
        self.left(90)   # turn left so that "forward" becomes "up" in effect
        self.reset_paddle(side,x_cor)

    def move_up(self):
        self.forward(STEP_LENGTH)

    def move_down(self):
        self.backward(STEP_LENGTH)

    def reset_paddle(self,side,x_cor):
        if side == "r":
            self.setposition(x_cor,0)
        elif side == "l":
            self.setposition(-x_cor,0)
        else:
            print("reset_paddle: Please enter a valid side for the paddle!")
            exit()
