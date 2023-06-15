import copy
import random
from game import Connect4Game

class MinimaxAlphaBetaPlayer:
    """
    MinimaxAlphaBetaPlayer Class

    This class represents a player that uses the Minimax algorithm with alpha-beta pruning to make decisions in a Connect4Game.
    The class has methods for evaluating the game position using different heuristics and selecting the best move for the current player.
    """
    def __init__(self, player_name:str, depth:int=1, heuristic:str='default'):
        """
        Initializes the MinimaxAlphaBetaPlayer class.

        Parameters:
        - player_name: The name of the player (string).
        - depth: The depth of the search tree for the minimax algorithm (integer, default=1).
        - heuristic: The heuristic to be used for evaluating the game position (string, default='default').
        """
        self.player = player_name
        self.depth = depth
        self.heuristic = heuristic

    def get_best_move(self, game:Connect4Game):
        """
        Returns the best move for the current player in the given Connect4Game.

        Parameters:
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The best move for the current player (integer).
        """
        best_score = float("-inf")
        best_move = None

        for move in game.get_valid_moves():
            temp_game = copy.deepcopy(game)
            temp_game.make_move(move)
            score = self.minimax(temp_game, self.depth, float("-inf"), float("inf"), False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, game:Connect4Game, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning for determining the best move.

        Parameters:
        - game: The Connect4Game object representing the current game state.
        - depth: The current depth of the search tree (integer).
        - alpha: The best value that the maximizing player can guarantee at this level or above (float).
        - beta: The best value that the minimizing player can guarantee at this level or above (float).
        - maximizing_player: A boolean value indicating whether the current player is the maximizing player.

        Returns:
        - The evaluated score for the current game state (integer).
        """
        if depth == 0 or game.game_over:
            return self.evaluate_position(game)

        if maximizing_player:
            max_eval = float("-inf")
            for move in game.get_valid_moves():
                temp_game = copy.deepcopy(game)
                temp_game.make_move(move)
                eval_score = self.minimax(temp_game, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in game.get_valid_moves():
                temp_game = copy.deepcopy(game)
                temp_game.make_move(move)
                eval_score = self.minimax(temp_game, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_position(self, game:Connect4Game):
        """
        Evaluates the game position using the specified heuristic.

        Parameters:
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current game position (integer).
        """
        if self.heuristic == 'blocking_opponent':
            return self.evaluate_blocking_opponent(game)
        elif self.heuristic == 'defensive':
            return self.evaluate_defensive(game)
        elif self.heuristic == 'threats':
            return self.evaluate_threats(game)
        elif self.heuristic == 'random':
            return self.evaluate_random(game)
        else:
            return self.evaluate_threats(game)
    
    def evaluate_random(self, game:Connect4Game):
        """
        Evaluates the game position randomly.

        Parameters:
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current game position (integer).
        """
        if game.game_over:
            if game.current_player == self.player:
                return -100  # If the current player loses, assign a low evaluation value
            else:
                return 100  # If the current player wins, assign a high evaluation value
        else:
            return random.randint(-100, 100)  # If the game is not over, return a random evaluation value between -100 and 100

    def evaluate_blocking_opponent(self, game:Connect4Game):
        """
        Evaluates the game position based on blocking the opponent's moves.

        Parameters:
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current game position (integer).
        """
        score = 0

        # Evaluate rows
        for row in range(game.rows):
            for col in range(game.cols - game.win_condition + 1):
                window = game.board[row][col : col + game.win_condition]
                score += self.evaluate_blocking_opponent_window(window, game)

        # Evaluate columns
        for col in range(game.cols):
            for row in range(game.rows - game.win_condition + 1):
                window = [game.board[row + i][col] for i in range(game.win_condition)]
                score += self.evaluate_blocking_opponent_window(window, game)

        # Evaluate positive diagonals
        for row in range(game.rows - game.win_condition + 1):
            for col in range(game.cols - game.win_condition + 1):
                window = [game.board[row + i][col + i] for i in range(game.win_condition)]
                score += self.evaluate_blocking_opponent_window(window, game)

        # Evaluate negative diagonals
        for row in range(game.rows - game.win_condition + 1):
            for col in range(game.win_condition - 1, game.cols):
                window = [game.board[row + i][col - i] for i in range(game.win_condition)]
                score += self.evaluate_blocking_opponent_window(window, game)

        return score
    
    def evaluate_defensive(self, game:Connect4Game):
        """
        Evaluates the game position based on defensive moves.

        Parameters:
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current game position (integer).
        """
        score = 0

        # Evaluate rows
        for row in range(game.rows):
            for col in range(game.cols - game.win_condition + 1):
                window = game.board[row][col:col + game.win_condition]
                score += self.evaluate_defensive_window(window, game)

        # Evaluate columns
        for col in range(game.cols):
            for row in range(game.rows - game.win_condition + 1):
                window = [game.board[row + i][col] for i in range(game.win_condition)]
                score += self.evaluate_defensive_window(window, game)

        # Evaluate positive diagonals
        for row in range(game.rows - game.win_condition + 1):
            for col in range(game.cols - game.win_condition + 1):
                window = [game.board[row + i][col + i] for i in range(game.win_condition)]
                score += self.evaluate_defensive_window(window, game)

        # Evaluate negative diagonals
        for row in range(game.rows - game.win_condition + 1):
            for col in range(game.win_condition - 1, game.cols):
                window = [game.board[row + i][col - i] for i in range(game.win_condition)]
                score += self.evaluate_defensive_window(window, game)

        return score
    
    def evaluate_threats(self, game:Connect4Game):
        """
        Evaluates the game position based on potential threats.

        Parameters:
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current game position (integer).
        """
        score = 0

        # Evaluate rows
        for row in range(game.rows):
            for col in range(game.cols - game.win_condition + 1):
                window = game.board[row][col : col + game.win_condition]
                score += self.evaluate_threats_window(window, game)

        # Evaluate columns
        for col in range(game.cols):
            for row in range(game.rows - game.win_condition + 1):
                window = [game.board[row + i][col] for i in range(game.win_condition)]
                score += self.evaluate_threats_window(window, game)

        # Evaluate positive diagonals
        for row in range(game.rows - game.win_condition + 1):
            for col in range(game.cols - game.win_condition + 1):
                window = [game.board[row + i][col + i] for i in range(game.win_condition)]
                score += self.evaluate_threats_window(window, game)

        # Evaluate negative diagonals
        for row in range(game.rows - game.win_condition + 1):
            for col in range(game.win_condition - 1, game.cols):
                window = [game.board[row + i][col - i] for i in range(game.win_condition)]
                score += self.evaluate_threats_window(window, game)

        return score


    def evaluate_blocking_opponent_window(self, window, game:Connect4Game):
        """
        Evaluates a window of the game board for blocking the opponent's moves.

        Parameters:
        - window: The window of the game board to be evaluated (list).
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current window (integer).
        """
        score = 0

        # Evaluate window for AI player
        if window.count(self.player) == game.win_condition:
            score += 100
        elif window.count(self.player) == game.win_condition - 1 and window.count(game.empty) == 1:
            score += 10
        elif window.count(self.player) == game.win_condition - 2 and window.count(game.empty) == 2:
            score += 5

        # Evaluate window for opponent player
        opponent = game.player_2 if self.player == game.player_1 else game.player_1
        if window.count(opponent) == game.win_condition:
            score -= 100
        elif window.count(opponent) == game.win_condition - 1 and window.count(game.empty) == 1:
            score -= 10
        elif window.count(opponent) == game.win_condition - 2 and window.count(game.empty) == 2:
            score -= 5

        return score
    
    def evaluate_defensive_window(self, window, game:Connect4Game):
        """
        Evaluates a window of the game board for defensive moves.

        Parameters:
        - window: The window of the game board to be evaluated (list).
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current window (integer).
        """
        score = 0

        opponent = game.player_2 if self.player == game.player_1 else game.player_1

        if window.count(opponent) == game.win_condition:
            score -= 100
        elif window.count(opponent) == game.win_condition - 1 and window.count(game.empty) == 1:
            score -= 10
        elif window.count(opponent) == game.win_condition - 2 and window.count(game.empty) == 2:
            score -= 5

        return score
    
    def evaluate_threats_window(self, window, game:Connect4Game):
        """
        Evaluates a window of the game board for potential threats.

        Parameters:
        - window: The window of the game board to be evaluated (list).
        - game: The Connect4Game object representing the current game state.

        Returns:
        - The evaluation score for the current window (integer).
        """
        score = 0

        # Evaluate window for AI player
        if window.count(self.player) == game.win_condition - 1 and window.count(game.empty) == 1:
            score += 20

        # Evaluate window for opponent player
        opponent = game.player_2 if self.player == game.player_1 else game.player_1
        if window.count(opponent) == game.win_condition - 1 and window.count(game.empty) == 1:
            score -= 50

        return score