import os
import pandas as pd
from turtle import Turtle




# Function to determine the winner
def determine_winner(bsnake_score, psnake_score):
    if bsnake_score > psnake_score:
        return 'Blue'
    elif psnake_score > bsnake_score:
        return 'Pink'
    else:
        return 'Draw'

# Function to save game data to CSV
def save_game_data(game_number, bsnake_score, psnake_score, csv_file_path):
    winner = determine_winner(bsnake_score, psnake_score)
    game_data = {
        'Game Number': [game_number],
        'Blue Snake Score': [bsnake_score],
        'Pink Snake Score': [psnake_score], 
        'Winner': [winner]
    }
    df_new = pd.DataFrame(game_data)
    if os.path.exists(csv_file_path):
        df_existing = pd.read_csv(csv_file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_csv(csv_file_path, index=False)
    return df_combined


# Function to display confrontation result
def display_confrontation_result(df_combined):
    blue_wins = len(df_combined[df_combined['Winner'] == 'Blue'])
    violet_wins = len(df_combined[df_combined['Winner'] == 'Pink'])

    result = Turtle("square")
    result.color("green")
    result.penup()
    result.hideturtle()   
    result.goto(0, 60)
    result.clear()
    result_text = f"Blue vs Pink\n{blue_wins} : {violet_wins}"
    result.write(result_text, align="center", font=("Arial", 24, "normal"))