from turtle import Turtle
from time import sleep
ALIGNMENT = "center"
FONT=('Courier', 24, 'normal')

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.hideturtle()
        self.color("white")
        self.penup()
        self.init_x = 0
        self.init_y = 0
        self.score_l = 0
        self.score_r = 0

    def write_score(self):
        self.clear()
        self.teleport(self.init_x, self.init_y)
        scorestring = f"{self.score_l} : {self.score_r}"
        self.write(scorestring, ALIGNMENT, font=FONT)

    def increase_score(self, player):
        if player == "l":
            self.score_l += 1
        elif player == "r":
            self.score_r += 1
        else:
            print("Problem at scoreboard:increase_score!")
            exit()

    def set_init_position(self,screen):
        self.init_x = -30
        self.init_y = (screen.screensize()[1]) -30
        self.teleport(self.init_x,self.init_y)

    def game_over(self):
        self.teleport(-60, 0)
        self.color("red")
        self.write("GAME OVER", ALIGNMENT, font=FONT)

    def point(self,screen):
        x_offset = -150
        self.teleport(x_offset, 0)
        self.write("Point. Continue in 2", ALIGNMENT, font=FONT)
        screen.update()
        sleep(1)
        self.clear()
        self.teleport(x_offset, 0)
        self.write("Point. Continue in 1", ALIGNMENT, font=FONT)
        screen.update()
        sleep(1)
        self.clear()
        screen.update()
