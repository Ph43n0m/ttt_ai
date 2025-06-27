import random

import torch
import torch.nn as nn

from ttt_ai.game.agent.agent import Agent
from ttt_ai.game.field import FieldState


class NNAgent(Agent):
    """
    An agent that uses a neural network to play Tic Tac Toe.
    """

    def __init__(
            self, field_state_type: FieldState = FieldState.X, randomness: float = 0.2
    ):
        super().__init__(field_state_type, randomness)
        self.model = NNModel()

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
        """        Get the best move for the current board state using a neural network.
        Args:
            board: The current state of the Tic Tac Toe board.
        Returns:
            The best move for the current player.
        """
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
                    [0, 2, 6, 8]
                )  # pick a random corner as the first move

            # Convert the board state to a tensor
            board_tensor = torch.tensor(
                board.flatten(), dtype=torch.float
            )
            board_tensor = board_tensor.unsqueeze(0)
            # Initialize the neural network model

            # Forward pass through the model to get the predicted scores for each move
            with torch.no_grad():
                scores = self.model(board_tensor)
                # Get the index of the move with the highest score
            best_move = torch.argmax(scores).item()

            # Check if the best move is valid
            if board[best_move // 3, best_move % 3].state == FieldState.EMPTY:
                return best_move
            else:
                # If the best move is not valid, return a random valid move
                return board.get_flat_index_of_radom_free_field()


# Define the neural network model
class NNModel(nn.Module):
    def __init__(self):
        super(NNModel, self).__init__()
        self.fc1 = nn.Linear(9, 128)  # Input layer
        self.fc2 = nn.Linear(128, 64)  # Hidden layer
        self.fc3 = nn.Linear(64, 9)  # Output layer

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # Activation function for first layer
        x = torch.relu(self.fc2(x))  # Activation function for second layer
        x = self.fc3(x)  # Output layer
        return x
