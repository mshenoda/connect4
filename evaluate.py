import os
import time
import random
from tqdm import tqdm
from game import Connect4Game
from player import MinimaxAlphaBetaPlayer
import matplotlib.pyplot as plt

class MinimaxPlayerSettings:
    def __init__(self, name, depth, heuristic):
        self.name = f"{name} (d={depth},h={heuristic})"
        self.depth = depth
        self.heuristic = heuristic

def evaluate_ai_players(evaluation_dir, num_games, player1_settings:MinimaxPlayerSettings, player2_settings:MinimaxPlayerSettings):
        os.makedirs(evaluation_dir, exist_ok=True)
        player1_name = player1_settings.name
        player2_name = player2_settings.name
        player1 = MinimaxAlphaBetaPlayer(player1_name, depth=player1_settings.depth, heuristic=player1_settings.heuristic)
        player2 = MinimaxAlphaBetaPlayer(player2_name, depth=player1_settings.depth, heuristic=player2_settings.heuristic)
        player1_wins = 0
        player2_wins = 0
        draws = 0

        # Track win rate, average game length, and evaluation time over time
        player1_win_rates = []
        player2_win_rates = []
        average_game_lengths = []
        evaluation_times = []

        for game_num in tqdm(range(1, num_games + 1)):
            game = Connect4Game(player1_name, player2_name)

            # Randomly select which player goes first
            first_player = random.choice([game.player_1, game.player_2])
            game.current_player = first_player

            start_time = time.time()  # Start time for evaluation

            moves = 0
            while not game.game_over and not game.is_board_full():
                if game.current_player == game.player_1:
                    move = player1.get_best_move(game)
                else:
                    move = player2.get_best_move(game)
                game.make_move(move)
                moves += 1

            evaluation_time = time.time() - start_time  # End time for evaluation

            if game.game_over:
                if game.current_player == game.player_1:
                    player1_wins += 1
                else:
                    player2_wins += 1
            else:
                draws += 1

            # Calculate win rates, average game length, and evaluation time at current game number
            player1_win_rate = player1_wins / game_num * 100
            player2_win_rate = player2_wins / game_num * 100
            evaluation_times.append(evaluation_time)
            player1_win_rates.append(player1_win_rate)
            player2_win_rates.append(player2_win_rate)
            average_game_lengths.append(moves)

        total_games = player1_wins + player2_wins + draws
        player1_win_percentage = player1_wins / total_games * 100
        player2_win_percentage = player2_wins / total_games * 100
        draw_percentage = draws / total_games * 100

        result_message = f"{player1_name} wins: {player1_win_percentage:.2f}%\n"
        result_message += f"{player2_name} wins: {player2_win_percentage:.2f}%\n"
        result_message += f"Draws: {draws} {draw_percentage:.2f}%\n"
        result_message += f"Avg Moves: {(sum(average_game_lengths)/len(average_game_lengths)):.2f}"

        print(result_message)

        # Plot win rates over time
        plt.figure(figsize=(10, 6))
        plt.plot(player1_win_rates, label=player1_name)
        plt.plot(player2_win_rates, label=player2_name)
        plt.xlabel("Game Number")
        plt.ylabel("Win Rate (%)")
        plt.title("Win Rate of AI Players")
        plt.legend()
        plt.savefig(evaluation_dir+f"/win_rate_{player1_name}_{player2_name}.png")

        # Plot average game length over time
        plt.figure(figsize=(10, 6))
        plt.plot(average_game_lengths)
        plt.xlabel("Game Number")
        plt.ylabel("Game Moves (moves)")
        plt.title("Game Moves")
        plt.savefig(evaluation_dir+f"/game_moves_{player1_name}_{player2_name}.png")

        # Plot evaluation time over time
        plt.figure(figsize=(10, 6))
        plt.plot(evaluation_times)
        plt.xlabel("Game Number")
        plt.ylabel("Game Time (seconds)")
        plt.title("Game Duration")
        plt.savefig(evaluation_dir+f"/game_time_{player1_name}_{player2_name}.png")

        plt.close('all')


num_games = 100

player1 = MinimaxPlayerSettings("AI1", depth=1, heuristic="threats")
player2 = MinimaxPlayerSettings("AI2", depth=1, heuristic="defensive")
evaluate_ai_players("results/threats_vs_defensive", num_games, player1, player2)

player1 = MinimaxPlayerSettings("AI1", depth=1, heuristic="threats")
player2 = MinimaxPlayerSettings("AI2", depth=1, heuristic="blocking_opponent")
evaluate_ai_players("results/threats_vs_blocking_opponent", num_games, player1, player2)

player1 = MinimaxPlayerSettings("AI1", depth=1, heuristic="defensive")
player2 = MinimaxPlayerSettings("AI2", depth=1, heuristic="blocking_opponent")
evaluate_ai_players("results/defensive_vs_blocking_opponent", num_games, player1, player2)

player1 = MinimaxPlayerSettings("AI1", depth=1, heuristic="threats")
player2 = MinimaxPlayerSettings("AI2", depth=1, heuristic="random")
evaluate_ai_players("results/threats_vs_random", num_games, player1, player2)

player1 = MinimaxPlayerSettings("AI1", depth=1, heuristic="defensive")
player2 = MinimaxPlayerSettings("AI2", depth=1, heuristic="random")
evaluate_ai_players("results/defensive_vs_random", num_games, player1, player2)

player1 = MinimaxPlayerSettings("AI1", depth=1, heuristic="blocking_opponent")
player2 = MinimaxPlayerSettings("AI2", depth=1, heuristic="random")
evaluate_ai_players("results/blocking_opponent_vs_random", num_games, player1, player2)