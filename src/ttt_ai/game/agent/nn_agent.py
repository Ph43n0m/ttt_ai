import random
from collections import deque

import torch
import torch.nn as nn

from ttt_ai.game.agent.agent import Agent
from ttt_ai.game.agent.minimax_agent import MiniMaxAgent
from ttt_ai.game.agent.trainer.QTrainer import QTrainer
from ttt_ai.game.field import FieldState

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


def is_valid_move(board, move: int) -> bool:
    """
    Check if the move is valid.
    Args:
        board: The current state of the Tic Tac Toe board.
        move: The move to check.
    Returns:
        True if the move is valid, False otherwise.
    """
    return board.get_field_by_flat_index(move).state == FieldState.EMPTY


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
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.minimax_agent = MiniMaxAgent(
            field_state_type, 0.0
        )  # internal minimax agent for reinforcement learning
        self.perfect_hit_reward = 0

    def load_weights(self, path: str, training: bool = True) -> None:
        """
        Load the weights of the neural network from a file.
        Args:
            :param path:
            :param training:
        """
        # self.model.load_state_dict(torch.load(path))
        self.model = torch.load(path, weights_only=False)

        if training:
            self.model.train()  # set model to train mode
        else:
            self.model.eval()  # set model to evaluation mode

        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def save_weights(self, path: str) -> None:
        """
        Save the weights of the neural network to a file.
        Args:
            path (str): The path to the file where the weights will be saved.
        """
        # torch.save(self.model.state_dict(), path)
        torch.save(self.model, path)

    def remember(
        self,
        old_board_flattened,
        chosen_field,
        reward_for_move,
        new_board_flattened,
        game_over,
    ):
        self.memory.append(
            (
                old_board_flattened,
                chosen_field,
                reward_for_move,
                new_board_flattened,
                game_over,
            )
        )  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, chosen_field, reward_for_move, new_board_flattened, game_over in mini_sample:
        #    self.trainer.train_step(state, chosen_field, reward_for_move, new_board_flattened, game_over)

    def train_short_memory(
        self,
        old_board_flattened,
        action,
        reward_for_move,
        new_board_flattened,
        game_over,
    ):
        self.trainer.train_step(
            old_board_flattened, action, reward_for_move, new_board_flattened, game_over
        )

    def _calculate_reward(self, board) -> float:
        return super()._calculate_reward(board) + self.perfect_hit_reward

    def perform_action(self, board) -> None:
        old_board_flattened = board.flatten()
        chosen_field = super().perform_action(board)
        new_board_flattened = board.flatten()
        reward_for_move = self._calculate_reward(board)
        game_over = board.is_game_over()

        # train short memory
        self.train_short_memory(
            old_board_flattened,
            chosen_field,
            reward_for_move,
            new_board_flattened,
            game_over,
        )

        # remember
        self.remember(
            old_board_flattened,
            chosen_field,
            reward_for_move,
            new_board_flattened,
            game_over,
        )

        if game_over:
            self.train_long_memory()
            if self.total_reward > self.record:
                self.record = self.total_reward

    def get_best_move(self, board) -> int | None:
        """Get the next move for the current board state using a neural network.
        Args:
            board: The current state of the Tic Tac Toe board.
        Returns:
            The next move for the current player.
        """
        self.perfect_hit_reward = 0  # Reset the perfect hit reward for each move
        # Check if the board is full or if there is a winner
        # If the board is full or there is a winner, return None
        if board.is_game_over():
            return None

        # Randomness condition to explore the board
        if random.uniform(0, 1) < self._get_epsilon_by_game_count():
            return (
                board.get_flat_index_of_radom_free_field()
            )  # Random move if randomness condition is met
        else:
            if board.is_empty():
                return 0  # If the board is empty, return the first move

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

            best_minimax_move = self.minimax_agent.get_best_move(board)

            # Check if the best move is valid
            if is_valid_move(board, best_move):
                self.n_best_move += 1
                if best_minimax_move == best_move:
                    self.perfect_hit_reward = 0.5  # If the best move is also the best move from the minimax agent, count it as a good move

                return best_move
            else:
                # If the best move is not valid, return a random valid move
                self.n_invalid_move += 1
                self.perfect_hit_reward = -0.1

                # return board.get_flat_index_of_radom_free_field()
                return (
                    best_minimax_move
                    if is_valid_move(board, best_minimax_move)
                    else board.get_flat_index_of_radom_free_field()
                )
