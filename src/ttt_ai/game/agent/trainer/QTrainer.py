import torch
import torch.nn as nn
from torch import optim


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(
            self,
            old_board_flattened,
            action,
            reward_for_move,
            new_board_flattened,
            game_over,
    ):
        old_board_flattened = torch.tensor(old_board_flattened, dtype=torch.float)
        new_board_flattened = torch.tensor(new_board_flattened, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward_for_move = torch.tensor(reward_for_move, dtype=torch.float)
        # (n, x)

        if len(old_board_flattened.shape) == 1:
            # (1, x)
            old_board_flattened = torch.unsqueeze(old_board_flattened, 0)
            new_board_flattened = torch.unsqueeze(new_board_flattened, 0)
            action = torch.unsqueeze(action, 0)
            reward_for_move = torch.unsqueeze(reward_for_move, 0)
            game_over = (game_over,)

        # 1: predicted Q values with current state
        pred = self.model(old_board_flattened)

        target = pred.clone()
        for idx in range(len(game_over)):
            Q_new = reward_for_move[idx]
            if not game_over[idx]:
                Q_new = reward_for_move[idx] + self.gamma * torch.max(
                    self.model(new_board_flattened[idx])
                )

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
