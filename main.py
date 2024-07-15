import time
import os
import webbrowser
from result import *
from turtle import Screen
from snake import Snake
from food import Food

# Check if 'game_data.csv' exists in the working directory
if not os.path.isfile('game_data.csv'):
    # Open 'PlayerGuide.html' in the default web browser
    webbrowser.open('PlayerGuide.html')

screen = Screen()
screen.setup(width=640, height=640)
screen.bgcolor("white")
screen.title("Hebi Hunter")
screen.tracer(0)  # Turn off tracer. Screen will not update until update is called

psnake = Snake("VioletRed1", (0, -290))
bsnake = Snake("blue", (0, 280))
player = [psnake, bsnake]

food = Food()

screen.listen()

screen.onkey(lambda: psnake.up(food), "Up") #When psnake.up is called with food, the actual method being called is the wrapper function created by the decorator. The wrapper function expects self and food as parameters
screen.onkey(lambda: psnake.down(food), "Down")
screen.onkey(lambda: psnake.left(food), "Left")
screen.onkey(lambda: psnake.right(food), "Right")

screen.onkey(lambda: bsnake.up(food), "w")
screen.onkey(lambda: bsnake.down(food), "s")
screen.onkey(lambda: bsnake.left(food), "a")
screen.onkey(lambda: bsnake.right(food), "d")

game_is_paused = False
def toggle_pause():
    global game_is_paused
    game_is_paused = not game_is_paused

screen.onkey(toggle_pause, "space")

game_is_on = True
nplayers = len(player) # number of players

while game_is_on:
    screen.update()
    if not game_is_paused:
        food.move()
        food.calculatePoint()
        # if screen.update() is put here, the game never resumes
        time.sleep(0.1)

        # Detect food for snakes
        for snake in player:
            snake.move(food)

        # Self collision
        for i in range(nplayers):
            for segment in player[i].segments[1:]:
                if player[i].head.distance(segment) < 19: # when there is self collision
                    topPlayer = True
                    for j in range(nplayers):
                        if player[j].point > player[i].point: # if the player's score is not the highest
                            topPlayer = False
                            game_is_on = False
                            screen.update()
                            player[i].gameOver()
                            break
                    
                    if topPlayer: # if the player is the player with highest score, deduct the score by 100
                        player[i].point -= player[i].point//3
                        player[i].score.clear()
                        player[i].update_score()
        food.pointVisualize()

# Path to the CSV file
csv_file_path = 'game_data.csv'

# Initialize the game number
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
    if not df.empty:
        game_number = df['Game Number'].max() + 1
    else:
        game_number = 1
else:
    game_number = 1

# Save the game data to the CSV file and get the updated DataFrame
df_combined = save_game_data(game_number, bsnake.point, psnake.point, csv_file_path)

# Display the confrontation 
display_confrontation_result(df_combined)
screen.exitonclick()
