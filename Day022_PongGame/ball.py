"""This module provides the ball class for the Pong game"""

from turtle import Turtle
from random import randint,choice

STARTING_ANGLE = 90
STEP_SIZE = 5
SPEEDINCREASE = True


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("white")
        self.goto(0,0)
        self.step = STEP_SIZE
        self.speed("slowest")
        self.setheading(self.get_heading())

    def reset_ball(self, direction):
        self.setheading(self.get_heading(direction))
        self.setposition(0,0)
        self.step = STEP_SIZE

    def get_heading(self, direction = None):
        """ To get a random direction/heading of the ball at start.
        Uses STARTING_ANGLE as angle of the cone of possible headings."""

        if not direction:
            direction = choice(["l","r"])

        if direction == "r":
            heading = randint(-15,15)
        elif direction == "l":
            heading = randint(165,195)
        else:
            print("Problem at ball:get_start_heading!")
            exit()
        return heading

    def move(self):
        self.forward(self.step)

    def bounce_wall(self):
        current_heading = self.heading()
        self.setheading(-current_heading)

    def bounce_paddle(self):
        current_heading = self.heading() - 180
        self.setheading(-current_heading)
        if SPEEDINCREASE:
            self.step += 1
