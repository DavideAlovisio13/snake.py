# Importing necessary libraries
import curses  # Library for creating text-based interfaces
from copy import copy  # To create shallow copies of objects
from random import randint  # To generate random numbers
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN  # For detecting arrow key inputs

# Initializing the curses library (this will set up the environment for text-based UI)
curses.initscr()

# Create a new window of 30 rows and 60 columns, starting at (0, 0) position
window = curses.newwin(30, 60, 0, 0, curses.init_pair)

#colors
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # snake 
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # food
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # text/border


# Enable keypad mode for the window (to handle special keys like arrow keys)
window.keypad(True)

# Draw a border around the window
window.border(0)


snake = [[15, 13], [15, 12], [15, 11]]  # Starting position of the snake
food = [5, 35]  # Starting position of the food
lookFor = KEY_DOWN  # Initial direction of the snake
points = 0  # Initial score
window.timeout(max(10, 100 - points * 5))  # Adjust the speed of the game based on the score
window.addch(food[0], food[1], "O", curses.color_pair(2))  # Draw the food on the window

while True:
    window.addstr(0, 14, "Points: " + str(points) + '')  # Display the current score
    key = window.getch()  # Get the key pressed by the user
    if key != -1:
        lookFor = key  # Update the direction of the snake based on the key pressed
    newHead = copy(snake[0])  # Create a copy of the head of the snake
    if lookFor == KEY_DOWN:
        newHead[0] += 1  # Move the snake to the right
    elif lookFor == KEY_UP :
        newHead[0] -= 1  # Move the snake to the left
    elif lookFor == KEY_RIGHT:
        newHead[1] += 1  # Move the snake up
    elif lookFor == KEY_LEFT:
        newHead[1] -= 1  # Move the snake down
    snake.insert(0, newHead)  # Add the new head to the snake
    
    if snake[0][0] == 0 or snake[0][0] == 29 or snake[0][1] == 0 or snake[0][1] == 59:
        break  # If the snake hits the border, end the game
    if snake[0] in snake[1:]:
        break  # If the snake hits itself, end the game
    if snake[0] == food:
        food = [] # Remove the food from the window
        points += 1  # Increase the score
        while food == []:
            food = [randint(1, 28), randint(1, 58)]  # Generate a new random position for the food
            if food in snake:
                food = []  # If the food is at the same position as the snake, generate a new position
        window.addch(food[0], food[1], "O", curses.color_pair(2))  # Draw the food on the window
        
    else:
        lastPiece = snake.pop() # Remove the last piece of the snake
        window.addch(lastPiece[0], lastPiece[1], " ")  # Clear the last piece of the snake from the window
    
    window.addch(snake[0][0], snake[0][1], "x", curses.color_pair(1))  # Draw the snake on the window

curses.endwin() # End the curses mode
print("Game Over! Your final score is: " + str(points))  # Display the final