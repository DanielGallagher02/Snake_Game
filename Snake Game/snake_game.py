# Snake Game with Power-Ups
# Developed as a personal project to enhance understanding of game development using Pygame

import pygame       # Library for game development
import random       # For random number generation (used in placing food, obstacles, and power-ups)
import os           # For operating system interactions (used in high score file handling)

# Initialize Pygame modules
pygame.init()

# Define color constants (RGB format)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (100, 100, 100)
red = (213, 50, 80)    # Color for food
green = (0, 255, 0)    # Color for the snake
blue = (50, 153, 213)  # Color for obstacles
yellow = (255, 255, 0) # Color for Speed Boost power-up
purple = (128, 0, 128) # Color for Slow Down power-up
orange = (255, 165, 0) # Color for Score Multiplier power-up
cyan = (0, 255, 255)   # Color for Invincibility power-up

# Set up the game window dimensions
width = 600    # Width of the game window
height = 400   # Height of the game window

# Create the game window
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')  # Set the window title

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Snake properties
snake_block = 10  # Size of each block segment of the snake (for grid-based movement)

# Set up font styles for displaying text
font_style = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 25)
menu_font = pygame.font.SysFont(None, 50)
pause_font = pygame.font.SysFont(None, 35)
info_font = pygame.font.SysFont(None, 20)

# File path for storing the high score (ensure the directory exists)
high_score_file = "./Snake Game/high_score.txt"

def load_high_score():
    """Load the high score from a file."""
    # Check if the high score file exists
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as f:
            try:
                # Read and return the high score as an integer
                return int(f.read())
            except:
                # If the file is empty or corrupt, return 0
                return 0
    else:
        # If the file doesn't exist, return 0
        return 0

def save_high_score(score):
    """Save the high score to a file."""
    with open(high_score_file, 'w') as f:
        # Write the new high score to the file
        f.write(str(score))

def display_score(score, high_score):
    """Display the current score and high score on the screen."""
    # Render the score text
    score_text = score_font.render("Score: " + str(score), True, white)
    # Render the high score text
    high_score_text = score_font.render("High Score: " + str(high_score), True, white)
    # Blit the texts onto the game window at specified positions
    game_window.blit(score_text, [10, 10])
    game_window.blit(high_score_text, [10, 30])

def draw_snake(snake_list):
    """Draw the snake on the screen using rectangles."""
    # Iterate through each segment in the snake's body
    for x in snake_list:
        # Draw a rectangle for each segment
        pygame.draw.rect(game_window, green, [x[0], x[1], snake_block, snake_block])

def draw_obstacles(obstacles):
    """Draw obstacles on the screen."""
    # Iterate through the list of obstacles
    for obstacle in obstacles:
        # Draw each obstacle as a rectangle
        pygame.draw.rect(game_window, blue, [obstacle[0], obstacle[1], snake_block, snake_block])

def draw_power_up(power_up):
    """Draw the power-up on the screen."""
    if power_up:
        # Draw the power-up rectangle with its specific color
        pygame.draw.rect(game_window, power_up['color'], [power_up['pos'][0], power_up['pos'][1], snake_block, snake_block])

def message_center(msg, color, y_displace=0, font=font_style):
    """Display a message at the center of the screen."""
    # Render the message text
    mesg = font.render(msg, True, color)
    # Get the rectangle of the text for positioning
    text_rect = mesg.get_rect(center=(width / 2, height / 2 + y_displace))
    # Blit the message onto the game window
    game_window.blit(mesg, text_rect)

def pause(current_score, high_score):
    """Function to pause the game."""
    paused = True  # Flag to keep the game paused

    while paused:
        # Fill the screen with black color
        game_window.fill(black)

        # Display pause menu options
        message_center("Game Paused", white, -100, menu_font)
        message_center(f"Score: {current_score}", white, -50, pause_font)
        message_center(f"High Score: {high_score}", white, -20, pause_font)
        message_center("Press R to Resume", white, 20, pause_font)
        message_center("Press C to Restart", white, 60, pause_font)
        message_center("Press M for Main Menu", white, 100, pause_font)
        message_center("Press Q to Quit", white, 140, pause_font)
        pygame.display.update()

        # Event handling for pause menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game if the window is closed
                paused = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Resume the game
                    paused = False
                elif event.key == pygame.K_c:
                    # Restart the game
                    game_loop()
                elif event.key == pygame.K_m:
                    # Go back to main menu
                    main_menu()
                elif event.key == pygame.K_q:
                    # Quit the game
                    paused = False
                    pygame.quit()
                    quit()

        # Control the frame rate of the pause menu
        clock.tick(15)

def game_loop():
    """Main function to run the game loop."""
    game_over = False  # Flag to check if the game is over
    game_close = False  # Flag to check if the player has lost

    # Load the high score from the file
    high_score = load_high_score()

    # Initial snake speed settings
    base_snake_speed = 15
    snake_speed = base_snake_speed  # Current snake speed

    # Starting position of the snake (center of the screen)
    x1 = width / 2
    y1 = height / 2

    # Variables to track the snake's movement
    x1_change = 0
    y1_change = 0

    # Snake body represented as a list of coordinates
    snake_list = []
    snake_length = 1  # Initial length of the snake

    # Generate obstacles on the screen
    obstacles = []
    num_obstacles = 10  # Number of obstacles to generate

    # Generate random positions for obstacles
    while len(obstacles) < num_obstacles:
        obs_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        obs_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        obstacle_position = [obs_x, obs_y]

        # Ensure obstacles do not spawn on the snake's starting position or overlap with others
        if obstacle_position != [x1, y1] and obstacle_position not in obstacles:
            obstacles.append(obstacle_position)

    # Generate initial food position
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Ensure food does not spawn on an obstacle
    while [foodx, foody] in obstacles:
        foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Variables for power-ups
    power_up = None  # Current power-up on the screen
    power_up_spawn_time = random.randint(5000, 15000)  # Time until the next power-up spawns (in milliseconds)
    power_up_timer = 0  # Timer to track power-up spawning
    active_power_up = None  # Currently active power-up
    power_up_end_time = 0  # Time when the power-up effect ends

    # Define power-up types and their properties
    power_up_types = {
        'speed_boost': {'color': yellow, 'duration': 5000},        # Increases speed for 5 seconds
        'slow_down': {'color': purple, 'duration': 5000},          # Decreases speed for 5 seconds
        'score_multiplier': {'color': orange, 'duration': 5000},   # Doubles score for 5 seconds
        'invincibility': {'color': cyan, 'duration': 5000},        # Invincibility for 5 seconds
    }

    while not game_over:

        while game_close:
            # Fill the screen with black color
            game_window.fill(black)
            # Display game over messages
            message_center("You Lost!", red, -50, menu_font)
            message_center("Press C-Play Again, M-Main Menu, or Q-Quit", white, 10)
            # Display the current score and high score
            display_score(snake_length - 1, high_score)
            pygame.display.update()

            # Update high score if the current score is higher
            if snake_length - 1 > high_score:
                high_score = snake_length - 1
                save_high_score(high_score)

            # Event handling for game over screen
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # Quit the game
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        # Restart the game
                        game_loop()
                    elif event.key == pygame.K_m:
                        # Go back to main menu
                        main_menu()
                if event.type == pygame.QUIT:
                    # Quit the game
                    game_over = True
                    game_close = False

        # Event handling during gameplay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                # Movement controls
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    # Pause the game
                    pause(snake_length - 1, high_score)

        # Update the snake's position
        x1 += x1_change
        y1 += y1_change

        # Boundary collision detection
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            if active_power_up != 'invincibility':
                # End the game if not invincible
                game_close = True
            else:
                # Wrap around effect when invincible
                x1 = x1 % width
                y1 = y1 % height

        # Fill the game window with black color
        game_window.fill(black)

        # Draw the food
        pygame.draw.rect(game_window, red, [foodx, foody, snake_block, snake_block])

        # Draw the obstacles
        draw_obstacles(obstacles)

        # Draw the power-up if it exists
        draw_power_up(power_up)

        # Update the snake's body segments
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Collision detection with self and obstacles
        if active_power_up != 'invincibility':
            for x in snake_list[:-1]:
                if x == snake_head:
                    # End the game if the snake collides with itself
                    game_close = True

            if snake_head in obstacles:
                # End the game if the snake collides with an obstacle
                game_close = True
        else:
            # No collision detection when invincible
            pass

        # Draw the snake on the screen
        draw_snake(snake_list)
        # Display the current score and high score
        display_score(snake_length - 1, high_score)
        # Update the display
        pygame.display.update()

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # Spawn power-up after a certain time has passed
        if power_up is None and current_time - power_up_timer > power_up_spawn_time:
            # Randomly select a power-up type
            power_up_type = random.choice(list(power_up_types.keys()))
            # Generate random position for the power-up
            power_up_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            power_up_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            # Ensure the power-up does not spawn on the snake, food, or obstacles
            while [power_up_x, power_up_y] in snake_list or [power_up_x, power_up_y] == [foodx, foody] or [power_up_x, power_up_y] in obstacles:
                power_up_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
                power_up_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            # Create the power-up dictionary with its properties
            power_up = {
                'type': power_up_type,
                'pos': [power_up_x, power_up_y],
                'color': power_up_types[power_up_type]['color'],
                'duration': power_up_types[power_up_type]['duration'],
            }

        # Check if the snake has collected the power-up
        if power_up and x1 == power_up['pos'][0] and y1 == power_up['pos'][1]:
            active_power_up = power_up['type']             # Set the active power-up
            power_up_end_time = current_time + power_up['duration']  # Calculate when the effect ends
            power_up = None                                # Remove the power-up from the screen
            power_up_timer = current_time                  # Reset the power-up timer
            power_up_spawn_time = random.randint(10000, 20000)  # Set time for the next power-up

            # Apply the effects of the power-up
            if active_power_up == 'speed_boost':
                snake_speed += 5
            elif active_power_up == 'slow_down':
                snake_speed = max(5, snake_speed - 5)
            elif active_power_up == 'score_multiplier':
                pass  # Handled during scoring
            elif active_power_up == 'invincibility':
                pass  # Handled during collision detection

        # Check if the power-up effect has expired
        if active_power_up and current_time >= power_up_end_time:
            # Reset the effects of the power-up
            if active_power_up == 'speed_boost' or active_power_up == 'slow_down':
                snake_speed = base_snake_speed
            active_power_up = None

        # Check if the snake has eaten the food
        if x1 == foodx and y1 == foody:
            # Generate new food position
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

            # Ensure food does not spawn on the snake, obstacles, or power-up
            while [foodx, foody] in obstacles or [foodx, foody] in snake_list or (power_up and [foodx, foody] == power_up['pos']):
                foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

            # Increase the snake's length (score)
            if active_power_up == 'score_multiplier':
                snake_length += 2  # Double the length increment
            else:
                snake_length += 1

            # Increase the snake's speed every 5 points, unless slowed down
            if (snake_length - 1) % 5 == 0 and snake_speed < 30 and active_power_up != 'slow_down':
                snake_speed += 1

        # Control the frame rate of the game
        clock.tick(snake_speed)

    # Quit the game and close the window
    pygame.quit()
    quit()

def main_menu():
    """Function to display the main menu."""
    menu = True  # Flag to keep the main menu running
    while menu:
        # Fill the game window with black color
        game_window.fill(black)

        # Display the game title and menu options
        message_center("Snake Game", green, -100, menu_font)
        message_center("Press P to Play", white, -60, pause_font)
        message_center("Press H for High Score", white, -20, pause_font)
        message_center("Press I for Game Info", white, 20, pause_font)
        message_center("Press Q to Quit", white, 60, pause_font)
        pygame.display.update()

        # Event handling for the main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                menu = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Start the game
                    menu = False
                    game_loop()
                elif event.key == pygame.K_q:
                    # Quit the game
                    menu = False
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_h:
                    # Show high score
                    show_high_score()
                elif event.key == pygame.K_i:
                    # Show game information
                    show_game_info()

        # Control the frame rate of the main menu
        clock.tick(15)

def show_high_score():
    """Function to display the high score."""
    high_score = load_high_score()  # Load the high score
    showing = True  # Flag to keep the high score screen running
    while showing:
        # Fill the screen with black color
        game_window.fill(black)
        # Display the high score
        message_center("High Score", green, -50, menu_font)
        message_center(str(high_score), white, 0, menu_font)
        message_center("Press B to go back", white, 80, pause_font)
        pygame.display.update()

        # Event handling for the high score screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                showing = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    # Go back to main menu
                    showing = False
                    main_menu()

        # Control the frame rate of the high score screen
        clock.tick(15)

def show_game_info():
    """Function to display game information."""
    info = True  # Flag to keep the game info screen running
    # List of strings containing the game information
    lines = [
        "Game Information:",
        "",
        "Objective:",
        " - Navigate the snake to eat the red food squares.",
        " - Each time the snake eats food, it grows longer.",
        " - Avoid colliding with the walls, obstacles, or your own tail.",
        "",
        "Controls:",
        " - Arrow Keys to move the snake:",
        "   Up, Down, Left, Right.",
        " - Press 'P' to pause the game.",
        "",
        "Features:",
        " - Power-Ups (various colors) provide temporary abilities:",
        "   - Yellow: Speed Boost",
        "   - Purple: Slow Down",
        "   - Orange: Score Multiplier",
        "   - Cyan: Invincibility",
        " - Randomly placed obstacles (blue squares) add challenge.",
        " - High score tracking to keep track of your best performance.",
        "",
        "Press 'B' to return to the main menu.",
    ]
    while info:
        # Fill the screen with black color
        game_window.fill(black)
        y_offset = -220  # Starting vertical offset for displaying text
        # Iterate through the lines and display them on the screen
        for line in lines:
            message_center(line, white, y_offset, info_font)
            y_offset += 20  # Increment the vertical offset for the next line

        pygame.display.update()

        # Event handling for the game info screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                info = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    # Go back to main menu
                    info = False
                    main_menu()

        # Control the frame rate of the game info screen
        clock.tick(15)

# Start the game by calling the main menu function
main_menu()

