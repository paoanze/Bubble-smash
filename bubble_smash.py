from tkinter import *
from random import randint
from math import sqrt
from time import sleep, time

# Constants
WIN_HEIGHT = 500
WIN_WIDTH = 800
SUB_RADIUS = 15
SUB_SPEED = 10
MIN_BUB_RADIUS = 10
MAX_BUB_RADIUS = 30
MAX_BUB_SPEED = 10
BUFFER = 100
BUB_CREATION_CHANCE = 10
GAME_TIME_LIMIT = 30
BONUS_POINTS = 1000

# Initialization
main_window = Tk()
main_window.title('Bubble Smash')
canvas = Canvas(main_window, width=WIN_WIDTH, height=WIN_HEIGHT, bg="black")
canvas.pack()

# Ship creation
ship_id = canvas.create_polygon(5, 5, 5, 25, 30, 15, fill='white')
ship_id2 = canvas.create_oval(0, 0, 30, 30, outline='red')
CENTER_X = WIN_WIDTH / 2
CENTER_Y = WIN_HEIGHT / 2
canvas.move(ship_id, CENTER_X, CENTER_Y)
canvas.move(ship_id2, CENTER_X, CENTER_Y)

# Bubble lists
bubble_ids = []
bubble_radii = []
bubble_speeds = []

# Event handler for moving the ship
def move_submarine(event):
    if event.keysym == "Up":
        canvas.move(ship_id, 0, -SUB_SPEED)
        canvas.move(ship_id2, 0, -SUB_SPEED)
    elif event.keysym == "Down":
        canvas.move(ship_id, 0, SUB_SPEED)
        canvas.move(ship_id2, 0, SUB_SPEED)
    elif event.keysym == "Left":
        canvas.move(ship_id, -SUB_SPEED, 0)
        canvas.move(ship_id2, -SUB_SPEED, 0)
    elif event.keysym == "Right":
        canvas.move(ship_id, SUB_SPEED, 0)
        canvas.move(ship_id2, SUB_SPEED, 0)

canvas.bind_all('<Key>', move_submarine)

# Function to create a bubble
def create_bubble():
    x = WIN_WIDTH + BUFFER
    y = randint(0, WIN_HEIGHT)
    r = randint(MIN_BUB_RADIUS, MAX_BUB_RADIUS)
    bubble_id = canvas.create_oval(x - r, y - r, x + r, y + r, outline="white")
    bubble_ids.append(bubble_id)
    bubble_radii.append(r)
    bubble_speeds.append(randint(1, MAX_BUB_SPEED))

# Function to move all bubbles
def move_bubbles():
    for i in range(len(bubble_ids)):
        canvas.move(bubble_ids[i], -bubble_speeds[i], 0)

# Function to get coordinates of an object
def get_coordinates(id_num):
    pos = canvas.coords(id_num)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y

# Function to delete a bubble
def delete_bubble(i):
    del bubble_radii[i]
    del bubble_speeds[i]
    canvas.delete(bubble_ids[i])
    del bubble_ids[i]

# Function to clean up bubbles that are off the screen
def clean_up_bubbles():
    for i in range(len(bubble_ids) - 1, -1, -1):
        x, y = get_coordinates(bubble_ids[i])
        if x < -BUFFER:
            delete_bubble(i)

# Function to calculate distance between two objects
def calculate_distance(id1, id2):
    x1, y1 = get_coordinates(id1)
    x2, y2 = get_coordinates(id2)
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to handle collisions and update score
def check_collision():
    points = 0
    for i in range(len(bubble_ids) - 1, -1, -1):
        if calculate_distance(ship_id2, bubble_ids[i]) < (SUB_RADIUS + bubble_radii[i]):
            points += (bubble_radii[i] + bubble_speeds[i])
            delete_bubble(i)
    return points

# Function to update score display
def update_score(score):
    canvas.itemconfig(score_display, text=str(score))

# Function to update time display
def update_time(time_left):
    canvas.itemconfig(time_display, text=str(time_left))

# Display for time and score
canvas.create_text(50, 30, text='TIME', fill='white')
canvas.create_text(150, 30, text='SCORE', fill='white')
time_display = canvas.create_text(50, 50, fill='white')
score_display = canvas.create_text(150, 50, fill='white')

# Main game loop
current_score = 0
bonus_time = 0
game_end_time = time() + GAME_TIME_LIMIT

while time() < game_end_time:
    if randint(1, BUB_CREATION_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubbles()
    current_score += check_collision()
    if int(current_score / BONUS_POINTS) > bonus_time:
        bonus_time += 1
        game_end_time += GAME_TIME_LIMIT
    update_score(current_score)
    update_time(int(game_end_time - time()))
    main_window.update()
    sleep(0.01)

# Game over display
canvas.create_text(CENTER_X, CENTER_Y, text='GAME OVER', fill='red', font=('Helvetica', 30))
canvas.create_text(CENTER_X, CENTER_Y + 30, text='Score: ' + str(current_score), fill='white')
canvas.create_text(CENTER_X, CENTER_Y + 45, text='Bonus time: ' + str(bonus_time * GAME_TIME_LIMIT), fill='white')

# Start the Tkinter main loop
main_window.mainloop()
