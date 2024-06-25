import pygame
import sys
import random

# Constants
SCREEN_SIZE = 600  # Size of the game window
CELL_SIZE = SCREEN_SIZE // 3  # Size of each cell in the grid
LINE_WIDTH = 15  # Width of lines separating cells

# Button Constants
BUTTON_WIDTH = 350  # Width of menu buttons
BUTTON_HEIGHT = 50  # Height of menu buttons
BUTTON_PADDING = 20  # Padding between menu buttons
BUTTON_COLOR = pygame.Color('lightgray')  # Color of menu buttons
BUTTON_HOVER_COLOR = pygame.Color('gray')  # Color when mouse hovers over menu buttons

# Colors
BG_COLOR = pygame.Color('white')  # Background color of the game
LINE_COLOR = pygame.Color('gray')  # Color of grid lines
X_COLOR = pygame.Color('red')  # Color of X marks
O_COLOR = pygame.Color('blue')  # Color of O marks
TEXT_COLOR = pygame.Color('black')  # Color of text

# Initialize Pygame
pygame.init()

# Initialize Font
FONT = pygame.font.Font(None, 36)  # Default font for text rendering

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]  # Initialize an empty grid

    def display_board(self, screen):
        # Draw X and O marks on the board
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 'O':
                    # Draw O with a border
                    pygame.draw.circle(screen, O_COLOR, (int(col * CELL_SIZE + CELL_SIZE // 2), int(row * CELL_SIZE + CELL_SIZE // 2)), CELL_SIZE // 3, 10)
                elif self.grid[row][col] == 'X':
                    # Draw X with a border
                    pygame.draw.line(screen, X_COLOR, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4), (col * CELL_SIZE + CELL_SIZE * 3 // 4, row * CELL_SIZE + CELL_SIZE * 3 // 4), 10)
                    pygame.draw.line(screen, X_COLOR, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE * 3 // 4), (col * CELL_SIZE + CELL_SIZE * 3 // 4, row * CELL_SIZE + CELL_SIZE // 4), 10)

        # Draw lines separating cells
        self.draw_lines(screen)

    def draw_lines(self, screen):
        # Draw vertical and horizontal lines between cells
        for i in range(1, self.size):
            pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE), LINE_WIDTH)

    def update_board(self, move, symbol):
        row, col = move
        if self.grid[row][col] == '':
            self.grid[row][col] = symbol
            return True  # Move successfully made
        return False  # Cell already occupied

    def check_win_combination(self, player_symbol):
        # Check all rows and columns for winning combinations
        for row in range(self.size):
            if all(cell == player_symbol for cell in self.grid[row]):
                return True

        for col in range(self.size):
            if all(self.grid[row][col] == player_symbol for row in range(self.size)):
                return True

        # Check diagonals for winning combinations
        if all(self.grid[i][i] == player_symbol for i in range(self.size)) or all(self.grid[i][self.size - 1 - i] == player_symbol for i in range(self.size)):
            return True

        return False

    def is_full(self):
        # Check if the board is completely filled
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == '':
                    return False
        return True

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            ("Single Player vs AI", self.show_difficulty_select),  # Button to select single player mode
            ("Two Player", self.start_two_player),  # Button to start two-player mode
            ("Exit", self.exit_game)  # Button to exit the game
        ]
        self.difficulty_buttons = [
            ("Easy", "easy"),  # Difficulty button for easy AI
            ("Medium", "medium"),  # Difficulty button for medium AI
            ("Hard", "hard")  # Difficulty button for hard AI
        ]
        self.selected_difficulty = "easy"  # Default difficulty

    def draw_button(self, text, rect, is_hovered):
        # Function to draw a button on the screen
        color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        pygame.draw.rect(self.screen, color , rect)
        text_surf = FONT.render(text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def show_difficulty_select(self):
        # Show difficulty selection buttons
        self.buttons.clear()  # Clear existing buttons
        for text, difficulty in self.difficulty_buttons:
            self.buttons.append((text, lambda difficulty=difficulty: self.start_single_player(difficulty)))

    def run(self):
        # Main loop to run the menu
        while True:
            self.screen.fill(BG_COLOR)  # Fill the screen with background color
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position

            for index, (text, _) in enumerate(self.buttons):
                # Draw buttons on the screen
                rect = pygame.Rect((SCREEN_SIZE - BUTTON_WIDTH) // 2, 200 + index * (BUTTON_HEIGHT + BUTTON_PADDING), BUTTON_WIDTH, BUTTON_HEIGHT)
                is_hovered = rect.collidepoint(mouse_pos)  # Check if mouse is hovering over the button
                self.draw_button(text, rect, is_hovered)

            for event in pygame.event.get():
                # Event handling loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, (text, action) in enumerate(self.buttons):
                        rect = pygame.Rect((SCREEN_SIZE - BUTTON_WIDTH) // 2, 200 + index * (BUTTON_HEIGHT + BUTTON_PADDING), BUTTON_WIDTH, BUTTON_HEIGHT)
                        if rect.collidepoint(mouse_pos):
                            action()  # Perform action associated with the clicked button

            pygame.display.flip()  # Update display

    def start_single_player(self, difficulty):
        # Start single player game with selected difficulty
        self.buttons = [
            ("Single Player vs AI", self.show_difficulty_select),  # Button to select single player mode
            ("Two Player", self.start_two_player),  # Button to start two-player mode
            ("Exit", self.exit_game)  # Button to exit the game
        ]
        self.selected_difficulty = difficulty

        # Start the game with selected difficulty
        game = Game(self.screen)
        game.start_single_player_game(self.selected_difficulty)

    def start_two_player(self):
        # Start two-player game
        self.buttons = [
            ("Single Player vs AI", self.show_difficulty_select),  # Button to select single player mode
            ("Two Player", self.start_two_player),  # Button to start two-player mode
            ("Exit", self.exit_game)  # Button to exit the game
        ]

        # Start the game in two-player mode
        game = Game(self.screen)
        game.start_two_player_game()

    def exit_game(self):
        # Exit the game
        pygame.quit()
        sys.exit()

class Game:
    def __init__(self, screen):
        # Initialize the game
        self.screen = screen
        self.board = Board(3)  # Initialize a 3x3 game board
        self.players = []  # List to store players
        self.current_player_index = 0  # Index of current player
        self.game_mode = None  # Game mode (single player or two player)
        self.difficulty = None  # Difficulty level for AI
        self.game_state = "ongoing"  # Game state (ongoing, win, draw)

    def start_single_player_game(self, difficulty):
        # Start single player game
        self.game_mode = "single_player"
        self.difficulty = difficulty
        self.players.append(HumanPlayer("Player 1", "X"))  # Human player
        self.players.append(AIPlayer("Computer", "O", self.difficulty))  # AI player
        self.current_player_index = 0
        self.run_game()

    def start_two_player_game(self):
        # Start two player game
        self.game_mode = "two_player"
        self.players.append(HumanPlayer("Player 1", "X"))  # Player 1
        self.players.append(HumanPlayer("Player 2", "O"))  # Player 2
        self.current_player_index = 0
        self.run_game()

    def run_game(self):
        # Main game loop
        while self.game_state == "ongoing":
            self.handle_events()  # Handle events such as quitting or making moves

            self.screen.fill(BG_COLOR)  # Fill screen with background color
            self.board.display_board(self.screen)  # Display game board
            pygame.display.update()  # Update display

            current_player = self.players[self.current_player_index]  # Current player's turn
            self.make_move(current_player)  # Make a move for the current player

            if self.board.check_win_combination(current_player.symbol):
                self.game_state = "win"  # Game over - win
                self.end_game(current_player)
            elif self.board.is_full():
                self.game_state = "draw"  # Game over - draw
                self.end_game(None)
            else:
                self.current_player_index = (self.current_player_index + 1) % len(self.players)  # Switch to the next player

    def handle_events(self):
        # Handle events during the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_state == "ongoing":
                current_player = self.players[self.current_player_index]
                if isinstance(current_player, HumanPlayer):
                    current_player.handle_events(self.board, self.screen)

    def make_move(self, player):
        # Make a move for the current player
        if isinstance(player, HumanPlayer):
            player.make_move(self.board, self.screen)
        elif isinstance(player, AIPlayer):
            player.make_move(self.board)

    def end_game(self, winner):
        # End the game and display winner or draw message
        if self.game_state == "win":
            print(f"{winner.name} wins!")
            main_game = Main()
            main_game.draw_board(self.board)
            main_game.display_winner(winner)
        elif self.game_state == "draw":
            print("It's a draw!")
            main_game = Main()
            main_game.draw_board(self.board)
            main_game.display_winner(None)

        pygame.time.wait(3000)  # Pause for 3 seconds before quitting
        pygame.quit()
        sys.exit()

class Player:
    def __init__(self, name, symbol, player_type):
        # Initialize player attributes
        self.name = name
        self.symbol = symbol
        self.player_type = player_type

    def make_move(self, board):
        # Abstract method for making a move
        raise NotImplementedError("This method should be overridden in subclasses")

    def handle_events(self, board, screen=None):
        # Abstract method for handling events
        raise NotImplementedError("This method should be overridden in subclasses")

    def choose_symbol(self):
        # Return player's symbol
        return self.symbol

class HumanPlayer(Player):
    def __init__(self, name, symbol):
        # Initialize human player
        super().__init__(name, symbol, "human")
        self.move_made = False  # Flag to indicate if move is made

    def make_move(self, board, screen=None):
        # Make a move on the board
        self.move_made = False
        while not self.move_made:
            self.handle_events(board, screen)

    def handle_events(self, board, screen=None):
        # Handle mouse events for human player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0] // CELL_SIZE
                mouseY = event.pos[1] // CELL_SIZE
                if board.update_board((mouseY, mouseX), self.symbol):
                    self.move_made = True
                    if screen:
                        screen.fill(BG_COLOR)
                        board.display_board(screen)
                        pygame.display.update()

class AIPlayer(Player):
    def __init__(self, name, symbol, difficulty):
        # Initialize AI player
        super().__init__(name, symbol, "AI")
        self.difficulty = difficulty  # Difficulty level for AI

    def make_move(self, board):
        # Make a move based on AI difficulty
        if self.difficulty == 'easy':
            self.make_easy_move(board)
        elif self.difficulty == 'medium':
            self.make_medium_move(board)
        elif self.difficulty == 'hard':
            self.make_hard_move(board)

    def make_easy_move(self, board):
        # Make an easy move (randomly)
        empty_cells = [(row, col) for row in range(board.size) for col in range(board.size) if board.grid[row][col] == '']
        move = random.choice(empty_cells)
        board.update_board(move, self.symbol)

    def make_medium_move(self, board):
        # Make a medium-level move
        if not self.try_to_win(board):
            if not self.block_opponent(board):
                self.make_easy_move(board)

    def make_hard_move(self, board):
        # Make a hard-level move using minimax algorithm
        best_score = -float('inf')
        best_move = None
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == '':
                    board.grid[row][col] = self.symbol
                    score = self.minimax(board, False)
                    board.grid[row][col] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        board.update_board(best_move, self.symbol)

    def try_to_win(self, board):
        # Check if AI can win in the next move
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == '':
                    board.grid[row][col] = self.symbol
                    if board.check_win_combination(self.symbol):
                        return True
                    board.grid[row][col] = ''
        return False

    def block_opponent(self, board):
        # Block opponent from winning in the next move
        opponent_symbol = 'X' if self.symbol == 'O' else 'O'
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == '':
                    board.grid[row][col] = opponent_symbol
                    if board.check_win_combination(opponent_symbol):
                        board.grid[row][col] = self.symbol
                        return True
                    board.grid[row][col] = ''
        return False

    def minimax(self, board, is_maximizing):
        # Minimax algorithm for finding the best move
        scores = {self.symbol: 1, 'draw': 0, 'opponent': -1}
        if board.check_win_combination(self.symbol):
            return scores[self.symbol]
        elif board.check_win_combination('X' if self.symbol == 'O' else 'O'):
            return scores['opponent']
        elif board.is_full():
            return scores['draw']

        if is_maximizing:
            best_score = -float('inf')
            for row in range(board.size):
                for col in range(board.size):
                    if board.grid[row][col] == '':
                        board.grid[row][col] = self.symbol
                        score = self.minimax(board, False)
                        board.grid[row][col] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            opponent_symbol = 'X' if self.symbol == 'O' else 'O'
            for row in range(board.size):
                for col in range(board.size):
                    if board.grid[row][col] == '':
                        board.grid[row][col] = opponent_symbol
                        score = self.minimax(board, True)
                        board.grid[row][col] = ''
                        best_score = min(score, best_score)
            return best_score

class Main:
    def __init__(self):
        # Initialize the main game window
        self.window = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.exiting = False  # Flag to control game exit

    def draw_board(self, board):
        # Draw the game board on the screen
        self.window.fill(BG_COLOR)
        board.draw_lines(self.window)
        board.display_board(self.window)
        pygame.display.update()

    def display_winner(self, winner):
        # Display winner or draw message on the screen
        if winner:
            winner_text = f"{winner.name} wins!"
        else:
            winner_text = "It's a draw!"
        text_surf = FONT.render(winner_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
        self.window.blit(text_surf, text_rect)
        pygame.display.update()
        pygame.time.wait(3000)  # Pause for 3 seconds before quitting

    def exit_game(self):
        # Exit the game
        pygame.quit()
        sys.exit()

# Example usage of the Menu class
if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Tic Tac Toe")  # Set window title
    menu = Menu(screen)  # Create a menu object
    menu.run()  # Run the menu loop to start the game
