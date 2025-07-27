# ttt_ai

## Project Overview

A Python-based Tic-Tac-Toe AI project. This codebase provides an environment for playing, analyzing, and extending
Tic-Tac-Toe games, with a focus on AI-driven gameplay and automation.

## Features

- Play Tic-Tac-Toe games via script or automated interface
- Agent vs Agent and Agent vs PC ("Fluent Tic-Tac-Toe") gameplay
- Modular code structure for easy extension
- Utilities for game state analysis

## Usage

1. Ensure Python 3.8+ is installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. To play an agent vs agent game (choose agent types: minimax, nn_v1, nn_v2), confiugure the main and run:
   ```
   python src/ttt_ai/play_agent_game.py
   ```
4. To play an agent vs the PC game "Fluent Tic-Tac-Toe", install and configure "Fluent Tic-Tac-Toe" first, then run:
   ```
   python src/ttt_ai/play_real_game.py
   ```

**Agent types:**

- `minimax`
- `nn_v1`
- `nn_v2`

**Note:**

- "Fluent Tic-Tac-Toe" must be installed and running for agent vs PC gameplay.
- Extend or modify AI logic in `src/ttt_ai/game/agent/`.

## File Structure

- `src/ttt_ai/play_agent_game.py`: Start agent vs agent games.
- `src/ttt_ai/play_real_game.py`: Start agent vs PC ("Fluent Tic-Tac-Toe") games.
- `src/ttt_ai/game/agent/`: AI agent implementations.
- `src/ttt_ai/game/`: Core game logic and state management.
- `src/ttt_ai/tools/`: Utilities for logging, plotting, and screenshotting.
- `assets/`: Images, models, and results for the project.
- `tests/`: Unit tests for game and agent modules.

## License

See `LICENSE` for details.
