import random

import torch
import torch.nn as nn

from ttt_ai.game.agent.agent import Agent
from ttt_ai.game.field import FieldState
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class NNAgent(Agent):
    """
    An agent that uses a neural network to play Tic Tac Toe.
    """

    def __init__(
            self,
            model: nn.Module,
            field_state_type: FieldState = FieldState.X,
            randomness: float = 0.2,
    ):
        super().__init__(field_state_type, randomness)
        self.model = model
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()

    def load_weights(self, path: str) -> None:
        """
        Load the weights of the neural network from a file.
        Args:
            path (str): The path to the file containing the weights.
        """
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

    def save_weights(self, path: str) -> None:
        """
        Save the weights of the neural network to a file.
        Args:
            path (str): The path to the file where the weights will be saved.
        """
        torch.save(self.model.state_dict(), path)

    def get_best_move(self, board) -> int | None:
        """Get the best move for the current board state using a neural network.
        Args:
            board: The current state of the Tic Tac Toe board.
        Returns:
            The best move for the current player.
        """
        next_move = self.get_next_move(board)
        return next_move

    def get_next_move(self, board) -> int | None:
        """Get the next move for the current board state using a neural network.
        Args:
            board: The current state of the Tic Tac Toe board.
        Returns:
            The next move for the current player.
        """
        # Check if the board is full or if there is a winner
        # If the board is full or there is a winner, return None
        if (
                board.is_board_full()
                or board.is_winner(FieldState.X)
                or board.is_winner(FieldState.O)
        ):
            return None

        if random.uniform(0, 1) < self.epsilon:
            return (
                board.get_flat_index_of_radom_free_field()
            )  # Random move if randomness condition is met
        else:
            # If randomness condition is not met, use minimax algorithm

            if board.is_empty():
                return random.choice(
                    [0, 2, 8]
                )  # pick a random corner as the first move

            # Convert the board state to a tensor
            board_tensor = torch.tensor(board.flatten(), dtype=torch.float)
            board_tensor = board_tensor.unsqueeze(0)
            # Initialize the neural network model

            # Forward pass through the model to get the predicted scores for each move
            with torch.no_grad():
                scores = self.model(board_tensor)
                # Get the index of the move with the highest score
            best_move = torch.argmax(scores).item()
            # _, best_move = torch.max(scores.data, 1)

            # Check if the best move is valid
            if board[best_move // 3, best_move % 3].state == FieldState.EMPTY:
                return best_move
            else:
                # If the best move is not valid, return a random valid move
                return board.get_flat_index_of_radom_free_field()
