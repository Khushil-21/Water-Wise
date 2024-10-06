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

class Jug:
    def __init__(self, x, y, capacity, current=0):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.current = current
        self.width = 60
        self.height = 120

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        water_height = int(self.height * (self.current / self.capacity))
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x, self.y + self.height - water_height, self.width, water_height))
        text = font.render(f"{self.current}/{self.capacity}", True, BLACK)
        screen.blit(text, (self.x, self.y + self.height + 10))

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text = small_font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        return False

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = BLUE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def water_jug_game():
    def get_user_input():
        num_jugs = 0
        jugs = []
        target = {}
        input_boxes = []
        
        num_jugs_box = InputBox(300, 100, 140, 32)
        random_fill_button = Button(500, 100, 150, 50, "Random Fill", lambda: random_fill())
        next_button = Button(700, 100, 150, 50, "Next", lambda: next_page())
        
        def random_fill():
            nonlocal num_jugs, jugs, target, input_boxes
            num_jugs = random.randint(2, 5)
            num_jugs_box.text = str(num_jugs)
            num_jugs_box.txt_surface = font.render(num_jugs_box.text, True, num_jugs_box.color)
            
            jugs = [Jug(100 + i*200, 300, random.randint(5, 20)) for i in range(num_jugs)]
            target = {i: random.randint(1, jugs[i].capacity) for i in range(num_jugs)}
            
            input_boxes = [InputBox(100 + i*200, 200, 140, 32, str(jugs[i].capacity)) for i in range(num_jugs)]
            input_boxes.extend([InputBox(100 + i*200, 250, 140, 32, str(target[i])) for i in range(num_jugs)])
        
        def next_page():
            nonlocal num_jugs, jugs, target
            try:
                num_jugs = int(num_jugs_box.text)
                if not (2 <= num_jugs <= 5):
                    raise ValueError("Number of jugs must be between 2 and 5")
                
                jugs = [Jug(100 + i*200, 300, int(input_boxes[i].text)) for i in range(num_jugs)]
                target = {i: int(input_boxes[i+num_jugs].text) for i in range(num_jugs)}
                
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

    jugs, target = get_user_input()

    moves = 0
    solution = None
    user_steps = []

    def fill_jug(i):
        nonlocal moves
        if jugs[i].current < jugs[i].capacity:
            jugs[i].current = jugs[i].capacity
            moves += 1
            user_steps.append(f"Fill Jug {chr(65+i)}")

    def empty_jug(i):
        nonlocal moves
        if jugs[i].current > 0:
            jugs[i].current = 0
            moves += 1
            user_steps.append(f"Empty Jug {chr(65+i)}")

    def pour(i, j):
        nonlocal moves
        amount = min(jugs[i].current, jugs[j].capacity - jugs[j].current)
        if amount > 0:
            jugs[i].current -= amount
            jugs[j].current += amount
            moves += 1
            user_steps.append(f"Pour {amount}L from Jug {chr(65+i)} to Jug {chr(65+j)}")

    def check_win():
        return all(jugs[i].current == target.get(i, 0) for i in range(len(jugs)))

    def get_jug_state():
        return tuple(jug.current for jug in jugs)

    def solve_problem():
        nonlocal solution
        visited = set()
        queue = deque([(get_jug_state(), [])])

        while queue:
            state, path = queue.popleft()
            if state in visited:
                continue
            visited.add(state)

            if all(state[i] == target.get(i, 0) for i in range(len(jugs))):
                solution = path
                return

            for i in range(len(jugs)):
                # Fill jug
                if state[i] < jugs[i].capacity:
                    new_state = list(state)
                    new_state[i] = jugs[i].capacity
                    queue.append((tuple(new_state), path + [(f"Fill Jug {chr(65+i)}", new_state)]))

                # Empty jug
                if state[i] > 0:
                    new_state = list(state)
                    new_state[i] = 0
                    queue.append((tuple(new_state), path + [(f"Empty Jug {chr(65+i)}", new_state)]))

                # Pour to another jug
                for j in range(len(jugs)):
                    if i != j and state[i] > 0 and state[j] < jugs[j].capacity:
                        new_state = list(state)
                        amount = min(state[i], jugs[j].capacity - state[j])
                        new_state[i] -= amount
                        new_state[j] += amount
                        queue.append((tuple(new_state), path + [(f"Pour {amount}L from Jug {chr(65+i)} to Jug {chr(65+j)}", new_state)]))

    buttons = []
    for i, jug in enumerate(jugs):
        buttons.append(Button(100 + i*200, 500, 150, 50, f"Fill Jug {chr(65+i)}", lambda i=i: fill_jug(i)))
        buttons.append(Button(100 + i*200, 560, 150, 50, f"Empty Jug {chr(65+i)}", lambda i=i: empty_jug(i)))
    for i in range(len(jugs)):
        for j in range(len(jugs)):
            if i != j:
                buttons.append(Button(100 + i*200, 620 + j*60, 150, 50, f"Pour {chr(65+i)} to {chr(65+j)}", lambda i=i, j=j: pour(i, j)))

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