import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Water Jug Problem Solver Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

# Jug class to represent a water jug
class Jug:
    def __init__(self, x, y, capacity, current=0):
        self.x = x  # x-coordinate of the jug
        self.y = y  # y-coordinate of the jug
        self.capacity = capacity  # maximum capacity of the jug
        self.current = current  # current amount of water in the jug
        self.width = 60  # width of the jug's visual representation
        self.height = 120  # height of the jug's visual representation

    def draw(self, screen):
        """
        Draws the jug on the screen.
        """
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)  # Draw the jug outline
        water_height = int(self.height * (self.current / self.capacity))  # Calculate the height of the water level
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x, self.y + self.height - water_height, self.width, water_height))  # Draw the water level
        text = font.render(f"{self.current}/{self.capacity}", True, BLACK)  # Render the current/capacity text
        screen.blit(text, (self.x, self.y + self.height + 10))  # Display the current/capacity text

# Button class to represent a clickable button
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle representing the button
        self.text = text  # Text displayed on the button
        self.action = action  # Function to be called when the button is clicked
        self.color = GRAY  # Default color of the button

    def draw(self, screen):
        """
        Draws the button on the screen.
        """
        pygame.draw.rect(screen, self.color, self.rect)  # Draw the button rectangle
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Draw the button outline
        text = small_font.render(self.text, True, BLACK)  # Render the button text
        text_rect = text.get_rect(center=self.rect.center)  # Center the text on the button
        screen.blit(text, text_rect)  # Display the button text

    def handle_event(self, event):
        """
        Handles mouse events for the button.
        Returns True if the button is clicked, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()  # Call the button's action function
                return True
        return False

# InputBox class to represent a text input box
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)  # Rectangle representing the input box
        self.color = BLACK  # Default color of the input box
        self.text = text  # Text inside the input box
        self.txt_surface = font.render(text, True, self.color)  # Rendered text surface
        self.active = False  # Flag indicating if the input box is active

    def handle_event(self, event):
        """
        Handles events for the input box.
        Returns the input text if the user presses Enter, None otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # Toggle the active state
            else:
                self.active = False  # Deactivate the input box
            self.color = BLUE if self.active else BLACK  # Change the color based on the active state
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Return the input text if Enter is pressed
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Remove the last character if Backspace is pressed
                else:
                    self.text += event.unicode  # Add the typed character to the input text
                self.txt_surface = font.render(self.text, True, self.color)  # Re-render the text surface
        return None

    def draw(self, screen):
        """
        Draws the input box on the screen.
        """
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))  # Display the input text
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Draw the input box outline

def water_jug_game():
    """
    Main function that runs the Water Jug Problem Solver Game.
    """
    def get_user_input():
        """
        Function to get user input for the number of jugs, their capacities, and target amounts.
        Returns a tuple containing the list of jugs and the target dictionary.
        """
        num_jugs = 0
        jugs = []
        target = {}
        input_boxes = []
        
        num_jugs_box = InputBox(300, 100, 140, 32)  # Input box for the number of jugs
        random_fill_button = Button(500, 100, 150, 50, "Random Fill", lambda: random_fill())  # Button to randomly fill the jugs and targets
        next_button = Button(700, 100, 150, 50, "Next", lambda: next_page())  # Button to proceed to the game
        
        def random_fill():
            """
            Function to randomly fill the jugs and targets.
            """
            nonlocal num_jugs, jugs, target, input_boxes
            num_jugs = random.randint(2, 5)  # Randomly choose the number of jugs between 2 and 5
            num_jugs_box.text = str(num_jugs)
            num_jugs_box.txt_surface = font.render(num_jugs_box.text, True, num_jugs_box.color)
            
            jugs = [Jug(100 + i*200, 300, random.randint(5, 20)) for i in range(num_jugs)]  # Create jugs with random capacities
            target = {i: random.randint(1, jugs[i].capacity) for i in range(num_jugs)}  # Set random target amounts for each jug
            
            input_boxes = [InputBox(100 + i*200, 200, 140, 32, str(jugs[i].capacity)) for i in range(num_jugs)]  # Input boxes for jug capacities
            input_boxes.extend([InputBox(100 + i*200, 250, 140, 32, str(target[i])) for i in range(num_jugs)])  # Input boxes for target amounts
        
        def next_page():
            """
            Function to validate the user input and proceed to the game.
            Returns a tuple containing the list of jugs and the target dictionary if the input is valid, None otherwise.
            """
            nonlocal num_jugs, jugs, target
            try:
                num_jugs = int(num_jugs_box.text)
                if not (2 <= num_jugs <= 5):
                    raise ValueError("Number of jugs must be between 2 and 5")
                
                jugs = [Jug(100 + i*200, 300, int(input_boxes[i].text)) for i in range(num_jugs)]  # Create jugs with user-specified capacities
                target = {i: int(input_boxes[i+num_jugs].text) for i in range(num_jugs)}  # Set target amounts from user input
                
                if any(target[i] > jugs[i].capacity for i in range(num_jugs)):
                    raise ValueError("Target amount cannot exceed jug capacity")
                
                return jugs, target
            except ValueError as e:
                print(f"Error: {str(e)}")
                return None
        
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                num_jugs_box.handle_event(event)
                
                for box in input_boxes:
                    box.handle_event(event)
                
                if random_fill_button.handle_event(event):
                    random_fill()
                
                if next_button.handle_event(event):
                    result = next_page()
                    if result:
                        return result
            
            screen.fill(WHITE)
            
            text = font.render("Enter the number of jugs (2-5):", True, BLACK)
            screen.blit(text, (100, 100))
            num_jugs_box.draw(screen)
            
            for i in range(len(input_boxes)):
                if i < num_jugs:
                    text = font.render(f"Jug {chr(65+i)} Capacity:", True, BLACK)
                    screen.blit(text, (100 + i*200, 180))
                else:
                    text = font.render(f"Jug {chr(65+i-num_jugs)} Target:", True, BLACK)
                    screen.blit(text, (100 + (i-num_jugs)*200, 230))
                input_boxes[i].draw(screen)
            
            random_fill_button.draw(screen)
            next_button.draw(screen)
            
            pygame.display.flip()
            clock.tick(30)

    jugs, target = get_user_input()  # Get the list of jugs and target dictionary from the user

    moves = 0  # Number of moves made by the user
    solution = None  # Solution path found by the solver
    user_steps = []  # List of steps taken by the user

    def fill_jug(i):
        """
        Function to fill a jug with water.
        """
        nonlocal moves
        if jugs[i].current < jugs[i].capacity:
            jugs[i].current = jugs[i].capacity  # Fill the jug to its capacity
            moves += 1  # Increment the move count
            user_steps.append(f"Fill Jug {chr(65+i)}")  # Add the step to the user's steps list

    def empty_jug(i):
        """
        Function to empty a jug of water.
        """
        nonlocal moves
        if jugs[i].current > 0:
            jugs[i].current = 0  # Empty the jug
            moves += 1  # Increment the move count
            user_steps.append(f"Empty Jug {chr(65+i)}")  # Add the step to the user's steps list

    def pour(i, j):
        """
        Function to pour water from one jug to another.
        """
        nonlocal moves
        amount = min(jugs[i].current, jugs[j].capacity - jugs[j].current)  # Calculate the amount of water that can be poured
        if amount > 0:
            jugs[i].current -= amount  # Decrease the water in the source jug
            jugs[j].current += amount  # Increase the water in the destination jug
            moves += 1  # Increment the move count
            user_steps.append(f"Pour {amount}L from Jug {chr(65+i)} to Jug {chr(65+j)}")  # Add the step to the user's steps list

    def check_win():
        """
        Function to check if the current state of jugs matches the target state.
        Returns True if the goal is reached, False otherwise.
        """
        return all(jugs[i].current == target.get(i, 0) for i in range(len(jugs)))

    def get_jug_state():
        """
        Function to get the current state of all jugs as a tuple.
        """
        return tuple(jug.current for jug in jugs)

    def solve_problem():
        """
        Function to solve the Water Jug Problem using the BFS algorithm.
        """
        nonlocal solution
        visited = set()  # Set to store visited states
        queue = deque([(get_jug_state(), [])])  # Queue for BFS, initially containing the starting state and an empty path

        while queue:
            state, path = queue.popleft()  # Get the next state and its path from the queue
            if state in visited:
                continue  # Skip if the state has already been visited
            visited.add(state)  # Mark the state as visited

            if all(state[i] == target.get(i, 0) for i in range(len(jugs))):  # Check if the current state matches the target state
                solution = path  # Store the solution path
                return  # Exit the function since the solution is found

            for i in range(len(jugs)):
                # Fill jug
                if state[i] < jugs[i].capacity:
                    new_state = list(state)
                    new_state[i] = jugs[i].capacity
                    queue.append((tuple(new_state), path + [(f"Fill Jug {chr(65+i)}", new_state)]))  # Add the new state and path to the queue

                # Empty jug
                if state[i] > 0:
                    new_state = list(state)
                    new_state[i] = 0
                    queue.append((tuple(new_state), path + [(f"Empty Jug {chr(65+i)}", new_state)]))  # Add the new state and path to the queue

                # Pour to another jug
                for j in range(len(jugs)):
                    if i != j and state[i] > 0 and state[j] < jugs[j].capacity:
                        new_state = list(state)
                        amount = min(state[i], jugs[j].capacity - state[j])
                        new_state[i] -= amount
                        new_state[j] += amount
                        queue.append((tuple(new_state), path + [(f"Pour {amount}L from Jug {chr(65+i)} to Jug {chr(65+j)}", new_state)]))  # Add the new state and path to the queue

    buttons = []
    for i, jug in enumerate(jugs):
        buttons.append(Button(100 + i*200, 500, 150, 50, f"Fill Jug {chr(65+i)}", lambda i=i: fill_jug(i)))  # Button to fill a jug
        buttons.append(Button(100 + i*200, 560, 150, 50, f"Empty Jug {chr(65+i)}", lambda i=i: empty_jug(i)))  # Button to empty a jug
    for i in range(len(jugs)):
        for j in range(len(jugs)):
            if i != j:
                buttons.append(Button(100 + i*200, 620 + j*60, 150, 50, f"Pour {chr(65+i)} to {chr(65+j)}", lambda i=i, j=j: pour(i, j)))  # Button to pour from one jug to another

    solve_button = Button(WIDTH - 200, HEIGHT - 100, 150, 50, "Solve for me", solve_problem)
    buttons.append(solve_button)

    game_state = "playing"
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_state == "playing":
                for button in buttons:
                    button.handle_event(event)

        if game_state == "playing":
            moves_text = font.render(f"Moves: {moves}", True, BLACK)
            screen.blit(moves_text, (10, 10))

            target_text = font.render(f"Target: " + ", ".join([f"Jug {chr(65+i)} = {target[i]}" for i in target]), True, BLACK)
            screen.blit(target_text, (10, 50))

            for button in buttons:
                button.draw(screen)

            for jug in jugs:
                jug.draw(screen)

            if check_win():
                game_state = "won"

        elif game_state == "solution":
            solution_text = font.render("Solution:", True, BLACK)
            screen.blit(solution_text, (WIDTH // 2 - 50, 50))
            for i, (action, state) in enumerate(solution):
                step_text = small_font.render(f"{i+1}. {action}: {state}", True, BLACK)
                screen.blit(step_text, (WIDTH // 2 - 200, 100 + i*30))

        elif game_state == "won":
            win_text = font.render("You Win!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 50, 50))
            
            steps_text = font.render("Your steps:", True, BLACK)
            screen.blit(steps_text, (WIDTH // 2 - 50, 100))
            for i, step in enumerate(user_steps):
                step_text = small_font.render(f"{i+1}. {step}", True, BLACK)
                screen.blit(step_text, (WIDTH // 2 - 200, 150 + i*30))

        if solution and game_state == "playing":
            game_state = "solution"

        pygame.display.flip()
        clock.tick(30)

        if game_state in ["solution", "won"]:
            # Show the "You Win!" screen indefinitely
            pass

water_jug_game()
# Explanation of the entire code:
# This code implements a graphical Water Jug Problem Solver game using Pygame.
# It consists of several main components:

# 1. Imports and Initialization:
#    - Pygame and other necessary modules are imported.
#    - Pygame is initialized and the display window is set up.

# 2. Constants and Global Variables:
#    - Colors, fonts, and display dimensions are defined.

# 3. Classes:
#    - Jug: Represents a water jug with properties like capacity, current amount, and methods to draw itself.
#    - Button: Represents clickable buttons in the game interface.

# 4. Helper Functions:
#    - solve(): Implements the BFS algorithm to find the solution to the Water Jug Problem.
#    - check_win(): Checks if the current jug states match the target state.

# 5. Main Game Loop (water_jug_game()):
#    - Sets up the game state, jugs, buttons, and other necessary variables.
#    - Runs the main game loop, handling events, updating game state, and rendering the display.

# Execution flow of the entire code:
# 1. The script starts by importing necessary modules and initializing Pygame.
# 2. Global constants and variables are defined.
# 3. The Jug and Button classes are defined.
# 4. Helper functions like solve() and check_win() are defined.
# 5. The water_jug_game() function is defined, which sets up the game:
#    a. Game variables are initialized (jugs, buttons, game state, etc.).
#    b. The main game loop starts:
#       - Event handling (quit, button clicks)
#       - Game state updates
#       - Screen rendering based on the current game state
#       - Checking for win condition
#       - Displaying solution if requested
#       - Updating the display
# 6. The water_jug_game() function is called to start the game.
# 7. The game runs until the user closes the window or the game reaches an end state.

# This structure allows for an interactive, visual representation of the Water Jug Problem,
# where users can manipulate jugs, see the solution, and play the game to reach the target state.
