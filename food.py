import time
from turtle import Turtle
import random

up_limit_x = 300
up_limit_y = 300
down_limit_x = -300
down_limit_y = -300

# INITIAL_POINT = 15

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color("green")
        self.direction = random.randint(1,12)
        self.speed("fastest") # slow speed means the turtle is created in the center of the screen and then move to the position
        self.refresh()
    
    def move(self):
        self.setheading(30*self.direction)
        self.forward(random.randint(-5,15))

        # Screen boundary limits
        # Wrap the head around the screen boundaries
        if self.xcor() > up_limit_x:
            self.setx(down_limit_x)
        elif self.xcor() < down_limit_x:
            self.setx(up_limit_x)
        
        if self.ycor() > up_limit_y:
            self.sety(down_limit_y)
        elif self.ycor() < down_limit_y:
            self.sety(up_limit_y)

    def refresh(self):
        random_x = random.randint(-280,280)
        random_y = random.randint(-280,280)
        self.goto(random_x, random_y)
        self.baseRandom = random.randint(5,25)
        self.point = self.baseRandom
        self.direction = random.randint(1,12)
        self.start_time = time.time()

    def calculatePoint(self):
        basePoint = int(time.time() - self.start_time)
        if basePoint < self.baseRandom:
            self.point = self.baseRandom - basePoint
        else:
            self.point = 2

    def pointVisualize(self):
        if self.point > 0.1:
            scale = self.point/10
        else:
            scale = 0.01
        self.shapesize(stretch_len = scale, stretch_wid = scale)

