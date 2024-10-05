import pygame
import sys
import random

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

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text = small_font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

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
        
        input_state = "num_jugs"
        current_jug = 0
        
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if input_state == "num_jugs":
                    result = input_box.handle_event(event)
                    if result:
                        num_jugs = int(result)
                        if 2 <= num_jugs <= 5:
                            input_state = "jug_capacity"
                            input_boxes = [InputBox(100, 100 + i*60, 140, 32) for i in range(num_jugs)]
                        else:
                            print("Please enter a number between 2 and 5")
                
                elif input_state == "jug_capacity":
                    for i, box in enumerate(input_boxes):
                        result = box.handle_event(event)
                        if result:
                            capacity = int(result)
                            jugs.append(Jug(100 + i*200, 200, capacity))
                            if i == num_jugs - 1:
                                input_state = "target_amount"
                                input_boxes = [InputBox(100, 100 + i*60, 140, 32) for i in range(num_jugs)]
                            break
                
                elif input_state == "target_amount":
                    for i, box in enumerate(input_boxes):
                        result = box.handle_event(event)
                        if result:
                            target_amount = int(result)
                            if target_amount > 0:
                                target[i] = target_amount
                            if i == num_jugs - 1:
                                return jugs, target
            
            screen.fill(WHITE)
            
            if input_state == "num_jugs":
                text = font.render("Enter the number of jugs (2-5):", True, BLACK)
                screen.blit(text, (100, 50))
                input_box.draw(screen)
            
            elif input_state == "jug_capacity":
                text = font.render("Enter jug capacities:", True, BLACK)
                screen.blit(text, (100, 50))
                for i, box in enumerate(input_boxes):
                    jug_text = font.render(f"Jug {chr(65+i)}:", True, BLACK)
                    screen.blit(jug_text, (50, 100 + i*60))
                    box.draw(screen)
            
            elif input_state == "target_amount":
                text = font.render("Enter target amounts (0 if not a target):", True, BLACK)
                screen.blit(text, (100, 50))
                for i, box in enumerate(input_boxes):
                    jug_text = font.render(f"Jug {chr(65+i)}:", True, BLACK)
                    screen.blit(jug_text, (50, 100 + i*60))
                    box.draw(screen)
            
            pygame.display.flip()
            clock.tick(30)

    jugs, target = get_user_input()

    buttons = []
    for i, jug in enumerate(jugs):
        buttons.extend([
            Button(700, 100 + i*120, 150, 50, f"Fill Jug {chr(65+i)}", lambda i=i: fill_jug(i)),
            Button(700, 160 + i*120, 150, 50, f"Empty Jug {chr(65+i)}", lambda i=i: empty_jug(i)),
        ])
    for i in range(len(jugs)):
        for j in range(len(jugs)):
            if i != j:
                buttons.append(Button(700, 220 + i*120 + j*60, 150, 50, f"Pour {chr(65+i)} to {chr(65+j)}", lambda i=i, j=j: pour(i, j)))

    solve_button = Button(700, 700, 150, 50, "Solve Problem", solve_problem)
    buttons.append(solve_button)

    moves = 0
    
    def fill_jug(i):
        nonlocal moves
        if jugs[i].current < jugs[i].capacity:
            jugs[i].current = jugs[i].capacity
            moves += 1

    def empty_jug(i):
        nonlocal moves
        if jugs[i].current > 0:
            jugs[i].current = 0
            moves += 1

    def pour(i, j):
        nonlocal moves
        amount = min(jugs[i].current, jugs[j].capacity - jugs[j].current)
        if amount > 0:
            jugs[i].current -= amount
            jugs[j].current += amount
            moves += 1

    def check_win():
        return all(jugs[i].current == target.get(i, 0) for i in range(len(jugs)))

    def solve_problem():
        # Implement the solving algorithm here
        pass

    running = True
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)

        for jug in jugs:
            jug.draw(screen)

        for button in buttons:
            button.draw(screen)

        moves_text = font.render(f"Moves: {moves}", True, BLACK)
        screen.blit(moves_text, (10, 10))

        target_text = font.render(f"Target: " + ", ".join([f"Jug {chr(65+i)} = {target[i]}" for i in target]), True, BLACK)
        screen.blit(target_text, (10, 50))

        if check_win():
            win_text = font.render("You Win!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 50, 100))

        pygame.display.flip()

    pygame.quit()

water_jug_game()
