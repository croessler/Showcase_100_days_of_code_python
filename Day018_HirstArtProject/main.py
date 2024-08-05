""" 
=== 100 Days of Code (Python): Hirst Art Project (Day 18) ===

This module is to generate dot-images like those of Damien Hirst, see "image.jpg".
To do so, the colors he uses are extracted with "colorgram" from an example image
(again, "image.jpg"), stored in a file and then randomly used for the point colors.

1) The function "draw_hirst_points()" draws regular point as a grid of squares as
was the goal of this days challenge. An example is shown in "result.jpg"
2) In the context of this days lessons we also draw a spirograph (a figure composed
of interwoven circles) and since some dot-images of hirst looked somewhat similar,
I provided a way to do dot-spirograph-images, that is spirographs from dotted 
circles, with draw_hist_spirograph(). An example is shown in "result2.jpg".
"""

from random import choice
import colorgram
import turtle as t
from turtle import Turtle, Screen
from extracted_color_palette import ex_colors

t.colormode(255)

def get_colors_from_image(path = './image'):
    colors = colorgram.extract(path, 30)
    colors = colors[1:] # remove the most prominent color which is probably white
    colors_rgb = []
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        color_tuple = (r,g,b)
        colors_rgb.append(color_tuple)
    return colors_rgb

def colortest(param_turtle):
    turtle = param_turtle
    colors = get_colors_from_image()
    for color in colors:
        turtle.color(color)
        turtle.pensize(25)
        turtle.right(360/len(colors))
        turtle.forward(20)

def draw_hirst_points(param_turtle, x_points = 10, y_points = 10, pointsize = 20, pointdistance = 50):
    turtle = param_turtle
    l_screenheight = (pointdistance) * y_points
    l_screenwidth = (pointdistance) * x_points
    x_init_position = -(l_screenwidth/2) + pointsize
    y_init_position = -(l_screenheight/2) + pointsize
    for i in range(0,y_points):
        for j in range(0,x_points):
            turtle.teleport(x_init_position + (j*pointdistance), y_init_position + (i*pointdistance))
            turtle.color(choice(ex_colors))
            turtle.dot(pointsize)
    return l_screenwidth, l_screenheight
            
def draw_dot_circle(param_turtle, radius=100, points=40, pointsize=15):
    turtle = param_turtle
    angle = 360/points
    turtle.color(choice(ex_colors))
    for i in range(points):
        turtle.dot(pointsize)
        turtle.penup()
        turtle.circle(radius,angle)
    

def draw_hirst_spirograph(param_turtle, circles, radius, points, pointsize):
    turtle = param_turtle
    angle = 360/circles
    turtle.speed('fastest')
    for i in range(circles):
        draw_dot_circle(turtle, radius, points, pointsize)
        turtle.left(angle)
    l_screenwidth = 2*radius
    l_screenheight = 2*radius
    return l_screenwidth, l_screenheight


my_turtle = Turtle()
my_turtle.hideturtle()
#colortest(my_turtle) ## see the extracted colors
#print(get_colors_from_image()) ## provide a list of rgb-tuples of the extracted colors
# --> extracted_color_palette.py

###screenwidth, screenheight = draw_hirst_points(my_turtle, 16, 9, 30, 60)
screenwidth, screenheight = draw_hirst_spirograph(param_turtle=my_turtle,
                                                  circles=18,
                                                  radius=150,
                                                  points=30,
                                                  pointsize=10)


SCREEN = Screen()
SCREEN.screensize(screenwidth, screenheight)
SCREEN.delay(0)
SCREEN.exitonclick()
