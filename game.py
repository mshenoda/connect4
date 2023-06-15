# This module doesn't require any external dependencies.

class Connect4Game:
    """
    Connect4Game Class

    This class represents the Connect 4 game. It provides methods to initialize the game, make moves, check for a win, switch players, and get the valid moves.
    """
    def __init__(self, player1:str, player2:str):
        """
        Initializes a new instance of the Connect4Game class.
        
        Args:
            player1: A string representing the name of player 1.
            player2: A string representing the name of player 2.
        """
        self.rows = 6
        self.cols = 7
        self.win_condition = 4
        self.empty = " "
        self.player_1 = player1
        self.player_2 = player2
        self.board = [[self.empty] * self.cols for _ in range(self.rows)]
        self.current_player = self.player_1
        self.game_over = False
       
    def make_move(self, col:int):
        """
        Makes a move in the specified column.
        
        Args:
            col: An integer representing the column in which the move is to be made.
        """
        if not self.game_over and self.is_valid_move(col):
            row = self.get_next_open_row(col)
            self.board[row][col] = self.current_player
            if self.check_win(row, col):
                self.game_over = True
            else:
                self.switch_players()

    def is_valid_move(self, col:int):
        """
        Checks if a move is valid in the specified column.
        
        Args:
            col: An integer representing the column to check.
        
        Returns:
            True if the move is valid, False otherwise.
        """
        return col is not None and 0 <= col < self.cols and self.board[0][col] == self.empty

    def get_next_open_row(self, col:int):
        """
        Gets the next available row in the specified column.
        
        Args:
            col: An integer representing the column to check.
        
        Returns:
            The index of the next available row in the specified column, or None if the column is full.
        """
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == self.empty:
                return row
        return None

    def check_win(self, row:int, col:int):
        """
        Checks if the last move resulted in a win.
        
        Args:
            row: An integer representing the row of the last move.
            col: An integer representing the column of the last move.
        
        Returns:
            True if the last move resulted in a win, False otherwise.
        """
        player = self.board[row][col]

        # Check row
        for c in range(self.cols - self.win_condition + 1):
            if self.board[row][c : c + self.win_condition] == [player] * self.win_condition:
                return True

        # Check column
        for r in range(self.rows - self.win_condition + 1):
            if [self.board[i][col] for i in range(r, r + self.win_condition)] == [player] * self.win_condition:
                return True

        # Check positive diagonal
        for r in range(self.rows - self.win_condition + 1):
            for c in range(self.cols - self.win_condition + 1):
                if [self.board[r + i][c + i] for i in range(self.win_condition)] == [player] * self.win_condition:
                    return True

        # Check negative diagonal
        for r in range(self.rows - self.win_condition + 1):
            for c in range(self.win_condition - 1, self.cols):
                if [self.board[r + i][c - i] for i in range(self.win_condition)] == [player] * self.win_condition:
                    return True

        return False

    def switch_players(self):
        """
        Switches the current player.
        If the current player is player 1, sets the current player to player 2, and vice versa.
        """
        self.current_player = self.player_2 if self.current_player == self.player_1 else self.player_1

    def is_board_full(self):
        """
        Checks if the game board is full.
        
        Returns:
            True if the game board is full, False otherwise.
        """
        return all(self.board[0][col] != self.empty for col in range(self.cols))

    def get_valid_moves(self):
        """
        Gets a list of valid moves (columns) that can be made in the current game state.
        
        Returns:
            A list of valid moves (columns) that are not full.
        """
        return [col for col in range(self.cols) if self.is_valid_move(col)]
