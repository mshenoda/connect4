import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from functools import partial
from game import Connect4Game
from player import MinimaxAlphaBetaPlayer

COLOR_PLAYER_1 = "#ff1302"
COLOR_PLAYER_2 = "#ffd002"
FONT=("Lucida Sans Unicode", 14)

# Connect 4 App Class
class Connect4App(ctk.CTk):
    """
    The main application class for the Connect 4 game.
    
    This class utilizes the 'customtkinter' library for creating a custom-themed GUI,
    and the 'CTkMessagebox' class for displaying message boxes in the application.

    """
    def __init__(self):
        super().__init__()
        self.title("Connect 4")
        self.configure(fg_color="#0332bf", font=FONT)
        self.player_name = "You"
        self.ai_name = "MiniMax"
        self.depth = 1
        self.heuristic = "default"
        self.prompt_difficulty_level()
        self.game = Connect4Game(self.player_name, self.ai_name)
        self.ai_player = MinimaxAlphaBetaPlayer(self.ai_name, depth=self.depth, heuristic=self.heuristic)
        self.buttons = []
        self.choose_colors_button = None
        self.player1_indicator = None
        self.player2_indicator = None
        self.resizable(False, False)
        self.create_board()
        self.create_new_game_button()
        self.create_player_indicator()
        self.create_difficulty_label() 

    def run(self):
        """
        Starts the application main loop.
        """
        self.mainloop()

    def prompt_difficulty_level(self):
        """
        Prompts the user to select the difficulty level for the AI player.
        """
        prompt = CTkMessagebox(title="Difficulty Level", message="Game AI Difficulty", options=["Easy", "Medium", "Hard"], font=FONT).get()
        self.difficulty = prompt
        if prompt == "Easy":
            self.depth = 1
            self.heuristic = "threats"
        elif prompt == "Medium":
            self.depth = 3
            self.heuristic = "defensive"
        elif prompt == "Hard":
            self.depth = 3
            self.heuristic = "blocking_opponent"

    def create_difficulty_label(self):
        """
        Creates a label to display the current difficulty level.
        """
        self.difficulty_label = ctk.CTkLabel(self, text="Difficulty: " + self.difficulty, width=100, height=50, text_color="white", fg_color="transparent", font=FONT)
        self.difficulty_label.grid(row=self.game.rows + 1, column=self.game.cols-1, padx=5, pady=5, sticky="se")

    def update_difficulty_label(self):
        """
        Updates the difficulty label with the current difficulty level.
        """
        self.difficulty_label.configure(text="Difficulty: " + self.difficulty)

    def create_new_game_button(self):
        """
        Creates a button for starting a new game.
        """
        new_game_button = ctk.CTkButton(self, text="New Game", width=100, height=50, fg_color="#040a1c", corner_radius=10, hover=False, command=self.reset_game, font=FONT)
        new_game_button.grid(row=self.game.rows+1, column=3, padx=5, pady=5, sticky="w")

    def create_choose_color_button(self):
        """
        Creates a button for choosing the player colors.
        """
        def swap_colors():
            global COLOR_PLAYER_1, COLOR_PLAYER_2
            COLOR_PLAYER_1, COLOR_PLAYER_2 = COLOR_PLAYER_2, COLOR_PLAYER_1
            self.player1_indicator.configure(fg_color=COLOR_PLAYER_1)
            self.player2_indicator.configure(fg_color=COLOR_PLAYER_2)
        self.choose_colors_button = ctk.CTkButton(self, text="Color", width=100, height=50, fg_color="#040a1c", corner_radius=10, hover=False, command=swap_colors, font=FONT)
        self.choose_colors_button.grid(row=self.game.rows+1, column=3, padx=5, pady=5, sticky="e")

    def create_player_indicator(self):
        """
        Creates the player indicators and color selection button.
        """
        player1_txt = ctk.CTkLabel(self, text="   You", width=50, height=50, text_color="white", corner_radius=50, font=FONT)
        player1_txt.grid(row=self.game.rows+1, column=2, padx=5, pady=5, sticky="sw")
            
        self.player1_indicator = ctk.CTkLabel(self, text="", width=25, height=25, text_color="white", fg_color=COLOR_PLAYER_1, corner_radius=50)
        self.player1_indicator.grid(row=self.game.rows+1, column=2, padx=5, pady=5, sticky="e")
            
        player2_txt = ctk.CTkLabel(self, text="  MiniMax", width=50, height=50, text_color="white", corner_radius=50, font=FONT)
        player2_txt.grid(row=self.game.rows+1, column=4, padx=5, pady=5, sticky="sw")
        self.player2_indicator = ctk.CTkLabel(self, text="", width=25, height=25, text_color="#040a1c", fg_color=COLOR_PLAYER_2, corner_radius=50)
        self.player2_indicator.grid(row=self.game.rows+1, column=4, padx=5, pady=5, sticky="w")
        self.create_choose_color_button()

    def create_board(self):
        """
        Creates the game board buttons.
        """
        for row in range(self.game.rows):
            button_row = []
            for col in range(self.game.cols):
                button = ctk.CTkButton(self,width=100,height=100,text="",fg_color="#040a1c",corner_radius=60,hover=False,command=partial(self.make_move, col))
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

    def reset_game_prompt(self, message, status="info"):
        """
        Displays a prompt indicating the game result and asks the user if they want to play again.

        Parameters:
        - message: The message to be displayed in the prompt (string).
        - status: The status of the game ("won", "lost", or "info", default="info").
        """
        if status == "won":
            icon = "check"
        elif status == "lost": 
            icon = "cancel"
        else:
            icon = "info"
        prompt = CTkMessagebox(title="Game Over", message=f"{message} \nDo you want to play again?", icon=icon, option_1="Quit", option_2="Yes").get()
        if prompt == "Yes":
            self.reset_game()
        else:
            self.quit()

    def reset_game(self):
        """
        Resets the game state and creates a new game.
        """
        self.game = Connect4Game(self.player_name, self.ai_name)
        self.ai_player = MinimaxAlphaBetaPlayer(self.ai_name, depth=self.depth, heuristic=self.heuristic)
        self.buttons = []
        self.create_board()
        self.create_player_indicator()

    def make_move(self, col: int):
        """
        Makes a move on the game board and updates the UI.

        Parameters:
        - col: The column where the move is made (integer).
        """
        self.choose_colors_button.grid_forget()
        if self.game.game_over:
            self.reset_game_prompt("")
            return

        if self.game.current_player == self.game.player_1:
            color = COLOR_PLAYER_1
        else:
            color = COLOR_PLAYER_2

        row = self.game.get_next_open_row(col)
        if row is not None:
            self.buttons[row][col].configure(fg_color=color)
            self.game.make_move(col)
            self.update()
            if self.game.game_over:
                if self.game.current_player == self.ai_name:
                    self.reset_game_prompt("Sorry, you lost!", "lost")
                else:
                    self.reset_game_prompt("Congratulations, you Won!", "won")
            else:
                self.ai_move()

        if self.game.is_board_full():
            self.reset_game_prompt("It's a draw!")

    def ai_move(self):
        """
        Makes a move for the AI player and updates the UI.
        """
        self.choose_colors_button.grid_forget()
        col = self.ai_player.get_best_move(self.game)
        row = self.game.get_next_open_row(col)
        if row is not None:
            self.buttons[row][col].configure(fg_color=COLOR_PLAYER_2)
            self.game.make_move(col)
            if self.game.game_over:
                if self.game.current_player == self.ai_name:
                    self.reset_game_prompt("Sorry, you lost!", "lost")
                else:
                    self.reset_game_prompt("Congratulations, you Won!", "won")
            