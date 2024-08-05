""" 
=== 100 Days of Code (Python): Pong Game (Day 22) ===

This is a python implementation of the game "Pong" as part of the 100 days of code challenge.
We use the turtle module as basis.

There are several minor differences to the solution shown in the course videos. But the most 
important are these:
1) The game starts with a random angle in the direction of one of the players instead of always
the same direction to the same player.
2) In turn, the bouncing is sensitive to the impact angle. In the solution shown in the course 
video, the angle is always 45 degrees. Also, whereas the course solution manipulates the x and y
coordinates directly, this implementation here works with the direction information instead.
3) There is a small countdown after each point and everything is being reseted.
4) Finally, the speed increase is done by increasing the step size, not decreasing the update
intervall. I suspect the latter to affect the controlling behaviour and thus provide an 
inconsistent feeling.


"""

### Design:
## Classes:
## - the ball
## - the paddles
## - the scorebord (including middle line)
## - the walls of the field, maybe even just an if-statement in main

### Steps according to the course:
## 1) Create the screen
## 2) Create and move the paddle
## 3) Create another paddle
## 4) Create the ball and make it move
## 5) Detect collision with wall and bounce
## 6) Detect collision with paddle
## 7) Detect when paddle misses
## 8) Keep score

from time import sleep
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard


### Parameters
SCREENWIDTH = 800
SCREENHEIGHT = 600
WALLPOSITION = SCREENHEIGHT/2 - 10 # last number is buffer
PADDLE_X_COR = 350 # x-coordinate of the paddles (+ and -)
IS_GAME_ON = True

def set_quit():
    global IS_GAME_ON
    IS_GAME_ON = False

### Screen initiation
SCREEN = Screen()
SCREEN.setup(SCREENWIDTH, SCREENHEIGHT)
SCREEN.bgcolor("black")
SCREEN.title("Pong")

### Paddle initiation
right_paddle = Paddle("r", PADDLE_X_COR)
left_paddle = Paddle("l", PADDLE_X_COR)

### Make Screen sensitive to key input
SCREEN.listen()
SCREEN.onkey(right_paddle.move_up, "Up")
SCREEN.onkey(right_paddle.move_down, "Down")
SCREEN.onkey(left_paddle.move_up, "w")
SCREEN.onkey(left_paddle.move_down, "s")
SCREEN.onkey(set_quit, "q")
SCREEN.tracer(0)

### Scoreboard initiation
scoreboard = Scoreboard()
scoreboard.set_init_position(SCREEN)
scoreboard.write_score()
intermediate = Scoreboard()

### Ball initiation
ball = Ball()


### Main Game loop
while IS_GAME_ON:
    ## Move Ball forward, update, wait
    ball.move()
    SCREEN.update()
    sleep(0.01)

    ## Check for wall collision
    if ball.ycor() < -WALLPOSITION or ball.ycor() > WALLPOSITION:
        ball.bounce_wall()

    ## Check for Paddle collision
    #only if the x-coord of ball and paddle are similar check for y-coords:
    if abs(abs(ball.xcor()) - PADDLE_X_COR) < 10:
        # if so, distinct between left and right and check y-coords to be similar
        # up half to paddle length (up and down makes 2 half paddle lengths)
        if ((ball.xcor() < 0 and abs(ball.ycor() - left_paddle.ycor()) < 55) or
            (ball.xcor() > 0 and abs(ball.ycor() - right_paddle.ycor()) < 55)):
            ball.bounce_paddle()

    ## Ball out
    if ball.xcor() < -SCREENWIDTH/2 or ball.xcor() > SCREENWIDTH/2:
        #ball.bounce_paddle() #test (instead of "Ball out", bounce ball)

        if ball.xcor() < 0:
            pointfor = "r"
        else:
            pointfor = "l"
        scoreboard.increase_score(pointfor)
        scoreboard.write_score()
        intermediate.point(SCREEN)
        left_paddle.reset_paddle("l", PADDLE_X_COR)
        right_paddle.reset_paddle("r", PADDLE_X_COR)
        ball.reset_ball(pointfor) # start again with ball flying towards the other player

SCREEN.exitonclick()
