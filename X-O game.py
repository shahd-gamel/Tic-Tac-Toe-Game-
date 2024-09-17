import pygame
from random import randrange


# Initialize Pygame
def initialize_pygame():
    pygame.init()
    pygame.font.init()  # Initialize the font module
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tic-Tac-Toe')
    return screen

# Set up display dimensions and colors
WIDTH, HEIGHT = 300, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)    # Color for X
BLUE = (0, 0, 255)   # Color for O
PURPLE = (128, 0, 128)  
LIGHT_GREY = (211, 211, 211) 

# Set up fonts
font = None

def initialize_font():
    global font
    font = pygame.font.Font(None, 100)

# Create board
def create_board():
    return [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]

# Function to draw the game board
def draw_board(screen, board, message=None):
    screen.fill(WHITE)  # Fill the screen with white
    for row in range(3):
        for col in range(3):
            # Color the cell background
            pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(col * 100, row * 100, 100, 100))
            pygame.draw.rect(screen, BLACK, pygame.Rect(col * 100, row * 100, 100, 100), 2)
            # Set the text color based on the symbol
            text_color = RED if board[row][col] == 'X' else BLUE if board[row][col] == 'O' else BLACK
            text = font.render(board[row][col], True, text_color)
            screen.blit(text, (col * 100 + 30, row * 100 + 30))

    if message:
       
        message_text = font.render(message, True, PURPLE  )
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - message_text.get_height() // 2))

# Player makes their move
def player_move(board, symbol, move):
    row = (move - 1) // 3
    col = (move - 1) % 3
    if board[row][col] not in ['X', 'O']:
        board[row][col] = symbol
        return True
    return False

# Computer makes its move
def computer_move(board, symbol):
    while True:
        move = randrange(1, 10)
        row = (move - 1) // 3
        col = (move - 1) % 3
        if board[row][col] not in ['X', 'O']:
            board[row][col] = symbol
            break

# Check if there's a winner
def check_winner(board, symbol):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],  # Row 1
        [board[1][0], board[1][1], board[1][2]],  # Row 2
        [board[2][0], board[2][1], board[2][2]],  # Row 3
        [board[0][0], board[1][0], board[2][0]],  # Column 1
        [board[0][1], board[1][1], board[2][1]],  # Column 2
        [board[0][2], board[1][2], board[2][2]],  # Column 3
        [board[0][0], board[1][1], board[2][2]],  # Diagonal 1
        [board[2][0], board[1][1], board[0][2]]   # Diagonal 2
    ]
    return [symbol, symbol, symbol] in win_conditions

# Let the player choose between X or O
def choose_player():
    while True:
        player = input("Choose your symbol (X/O): ").upper()
        if player in ['X', 'O']:
            return player
        else:
            print("Invalid choice. Please choose 'X' or 'O'.")

# Main game loop
def play_game():
    global board
    board = create_board()
    player_symbol = choose_player()
    computer_symbol = 'X' if player_symbol == 'O' else 'O'
    screen = initialize_pygame()
    initialize_font()

    running = True
    turn = 'player'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if turn == 'player' and event.type == pygame.MOUSEBUTTONDOWN:
                # Convert mouse click to board move
                x, y = pygame.mouse.get_pos()
                move = (y // 100) * 3 + (x // 100) + 1
                if player_move(board, player_symbol, move):
                    if check_winner(board, player_symbol):
                        draw_board(screen, board, "You win!")
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Wait for 2 seconds before quitting
                        print("You win!")
                        running = False
                    turn = 'computer'

        if turn == 'computer':
            computer_move(board, computer_symbol)
            if check_winner(board, computer_symbol):
                draw_board(screen, board, "Computer wins!")
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds before quitting
                print("Computer wins!")
                running = False
            turn = 'player'

        draw_board(screen, board)
        pygame.display.flip()  # Update the display

    pygame.quit()  # Quit the display properly after the game ends

# Game loop to keep playing as long as the player chooses
while True:
    play_game()
    if input("Do you want to play again? (y/n): ").lower() != 'y':
        print("Thanks for playing!")
        break
