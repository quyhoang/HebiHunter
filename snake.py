from turtle import Turtle
import threading
import pygame

START_POS  = [(0,0), (-20,0), (-40,0)] #list of tuple
FONT = ("Arial", 24, "normal") # a tuple is required in write()

MOVE_DISTANCE = 20
MICRO_DISTANCE = 1

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

up_limit_x = 300
up_limit_y = 300
down_limit_x = -300
down_limit_y = -300

# Function to play sound in a separate thread
def play_sound(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load and play sound
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Keep the thread alive while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


class Snake:
    def __init__(self, color, scorePosition):
        self.color = color 
        self.segments = []
        self.create_snake(color)
        self.create_score(scorePosition)
        self.head = self.segments[0]
        self.key_pressed = False
        
    def create_score(self, scorePosition):
        self.score = Turtle("square")
        self.point = 0
        self.score.color(self.color)
        self.score.penup()
        self.score.goto(scorePosition)
        self.update_score()
        self.score.hideturtle()

    def update_score(self):
        self.score.write(f"Score: {self.point}", align="center", font=FONT)

    def gameOver(self):
        sound_thread = threading.Thread(target=play_sound, args=('gameOver.mp3',))
        sound_thread.start()

        # Final "さようなら！" message
        self.score.goto(0, 0)
        self.score.write("さようなら！", align="center", font=FONT)

    def increase_score(self, value):
        self.point += value
        self.score.clear()
        self.update_score()

    def create_snake(self, color):   
        for pos in START_POS:
            s = Turtle("circle")
            s.color(color)
            s.penup()
            s.goto(pos) # x,y
            self.segments.append(s)
        # self.segments[0].shape("circle")
        self.segments[0].shapesize(stretch_len=1.2, stretch_wid=1.2)

    def move(self, food, distance = MOVE_DISTANCE):
        for index in range(len(self.segments)-1, 0, -1):
            new_x = self.segments[index - 1].xcor()
            new_y = self.segments[index - 1].ycor()
            self.segments[index].goto(new_x, new_y)

        self.head.forward(distance)
        

        # Screen boundary limits
        # Wrap the head around the screen boundaries
        if self.head.xcor() > up_limit_x:
            self.head.setx(down_limit_x)
        elif self.head.xcor() < down_limit_x:
            self.head.setx(up_limit_x)
        
        if self.head.ycor() > up_limit_y:
            self.head.sety(down_limit_y)
        elif self.head.ycor() < down_limit_y:
            self.head.sety(up_limit_y)

        self.getFood(food)

    def getFood(self, food):
        if self.head.distance(food) <= 17:
            self.increase_score(food.point)
            self.grow()
            food.refresh()


    def grow(self):
        # Create and start a thread for playing the sound
        sound_thread = threading.Thread(target=play_sound, args=('ting.mp3',))
        sound_thread.start()
        s = Turtle("circle")
        s.color(self.color)
        s.penup()
        s.goto(self.segments[-1].position()) # last turtle's position
        self.segments.append(s)

    # def directionDecorator(func):
    #     def wrapper(self, food):
    #         result = func(self)
    #         self.move(food)
    #         return result
    #     return wrapper

    def directionDecorator(func):
        def wrapper(self, food):
            func(self)  # Call the original function without arguments
            self.move(food)  # Move the snake after changing the direction, using the captured food object
        return wrapper

    @directionDecorator
    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    @directionDecorator    
    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN) 
     
    @directionDecorator
    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    @directionDecorator
    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)