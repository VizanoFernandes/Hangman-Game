import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Fonts
FONT = pygame.font.SysFont("comicsans", 30)
LARGE_FONT = pygame.font.SysFont("comicsans", 50)

# Word list from random words
WORDS = ["python", "pygame", "developer", "challenge", "hangman", "interface", "function", "variable", "dynamic", "random"]

# Game variables
word = ""
guessed = []
wrong_attempts = 0
MAX_ATTEMPTS = 6
running_game = False

# Button variables
RADIUS = 20
gap = 15
letters = []
start_x = 50
start_y = 300
A = 65
for i in range(26):
    x = start_x + ((RADIUS * 2 + gap) * (i % 13))
    y = start_y + ((i // 13) * (gap + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

def reset_game():
    global word, guessed, wrong_attempts, letters, running_game
    word = random.choice(WORDS).upper()
    guessed = []
    wrong_attempts = 0
    for letter in letters:
        letter[3] = True
    running_game = True

def draw_start_screen():
    screen.fill(WHITE)
    title = LARGE_FONT.render("HANGMAN", True, BLACK)
    start_button = FONT.render("START GAME", True, WHITE, BLUE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50))
    screen.blit(start_button, (WIDTH // 2 - start_button.get_width() // 2, HEIGHT // 2 - start_button.get_height() // 2))

    pygame.display.update()

def draw():
    screen.fill(WHITE)

    # Draw title
    text = LARGE_FONT.render("HANGMAN", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

    # Draw word
    display_word = " ".join([letter if letter in guessed else "_" for letter in word])
    text = FONT.render(display_word, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

    # Draw attempts left
    attempts_text = FONT.render(f"Attempts Left: {MAX_ATTEMPTS - wrong_attempts}", True, RED)
    screen.blit(attempts_text, (WIDTH // 2 - attempts_text.get_width() // 2, 150))

    # Draw buttons
    for letter in letters:
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(screen, BLUE, (x, y), RADIUS, 3)
            text = FONT.render(char, True, BLACK)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    pygame.display.update()

def display_message(message, color):
    screen.fill(WHITE)
    text = LARGE_FONT.render(message, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    global wrong_attempts, running_game

    # Game loop
    run = True
    while run:
        if not running_game:
            draw_start_screen()
        else:
            draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if not running_game and event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
                if start_button.collidepoint(m_x, m_y):
                    reset_game()

            if running_game and event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, char, visible = letter
                    if visible:
                        distance = ((x - m_x) ** 2 + (y - m_y) ** 2) ** 0.5
                        if distance < RADIUS:
                            letter[3] = False
                            guessed.append(char)
                            if char not in word:
                                wrong_attempts += 1

        # Check win/lose conditions
        if running_game and all(letter in guessed for letter in word):
            display_message("You WON!", GREEN)
            reset_game()

        if running_game and wrong_attempts == MAX_ATTEMPTS:
            display_message(f"You LOST! The word was {word}", RED)
            reset_game()

main()
