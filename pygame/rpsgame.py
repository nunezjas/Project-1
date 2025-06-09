import pygame
import random
import sys
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sound files
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
draw_sound = pygame.mixer.Sound("draw.wav")

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)

# Fonts
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 40)

# Choices
choices = ["rock", "paper", "scissors"]

# Load images
rock_img = pygame.transform.scale(pygame.image.load("rock.png"), (100, 100))
paper_img = pygame.transform.scale(pygame.image.load("paper.png"), (100, 100))
scissors_img = pygame.transform.scale(pygame.image.load("scissors.png"), (100, 100))

# Load backgrounds
background = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
welcome_background = pygame.transform.scale(pygame.image.load("welcome_background.png"), (WIDTH, HEIGHT))

# Button positions
button_rects = {
    "rock": pygame.Rect(100, 250, 100, 100),
    "paper": pygame.Rect(250, 250, 100, 100),
    "scissors": pygame.Rect(400, 250, 100, 100)
}

# Start button
start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)

# Counters
user_wins = 0
computer_wins = 0
ties = 0

def get_result(player, computer):
    if player == computer:
        return "It's a draw!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "You win!"
    else:
        return "Computer wins!"

def draw_game(result_text):
    screen.blit(background, (0, 0))
    screen.blit(rock_img, button_rects["rock"].topleft)
    screen.blit(paper_img, button_rects["paper"].topleft)
    screen.blit(scissors_img, button_rects["scissors"].topleft)

    if result_text:
        result_surface = font.render(result_text, True, BLACK)
        screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, 50))

    pygame.display.flip()

def draw_welcome_screen():
    screen.blit(welcome_background, (0, 0))
    title = title_font.render("Welcome to Rock Paper Scissors", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

    pygame.draw.rect(screen, (0, 122, 204), start_button)
    start_text = font.render("Click to Start", True, WHITE)
    screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                             start_button.centery - start_text.get_height() // 2))

    pygame.display.flip()

# Welcome screen loop
showing_welcome = True
while showing_welcome:
    draw_welcome_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                showing_welcome = False

# Game loop
running = True
result_text = ""
while running:
    draw_game(result_text)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for choice, rect in button_rects.items():
                if rect.collidepoint(event.pos):
                    player_choice = choice
                    computer_choice = random.choice(choices)
                    result = get_result(player_choice, computer_choice)
                    result_text = f"{result} (Computer chose {computer_choice})"

                    if "win" in result.lower() and "computer" not in result.lower():
                        user_wins += 1
                        win_sound.play()
                    elif "computer wins" in result.lower():
                        computer_wins += 1
                        lose_sound.play()
                    else:
                        ties += 1
                        draw_sound.play()
                    break

# Display bar chart of results
labels = ['Computer Wins', 'User Wins', 'Ties']
values = [computer_wins, user_wins, ties]
colors = ['red', 'green', 'blue']

plt.figure(figsize=(8, 6))
plt.bar(labels, values, color=colors)
plt.title('Game Outcomes')
plt.xlabel('Outcome')
plt.ylabel('Count')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("game_outcomes.png")
plt.show()

pygame.quit()
sys.exit()

