# Gymnasium TicTacToe
---------
Gymnasium TicTacToe is a light Tic-Tac-Toe environment for Gymnasium.

## Features

- **Multi-agent support**: Simple two-player turn-based gameplay.
- **Configurable board**: Adjust board size and winning line length.
- **Customizable rewards**: Tweak win, loss, draw, and invalid-move penalties via `settings.xml`.
- **Gymnasium-compliant**: Follows the standard Gymnasium API (`reset()`, `step()`, `render()`).

## Installation

### 1. Prerequisites

- Python 3.7 or higher
- [Gymnasium](https://github.com/Farama-Foundation/Gymnasium)

```bash
pip install gymnasium
```


### 2. Download and install `gym-tictactoe`
```bash
git clone https://github.com/cesarluisg/gym-tictactoe.git
cd gym-tictactoe
python setup.py install
```

## Quickstart

Start by importing the package and initializing the environment

```python
import gymnasium as gym
import gym_tictactoe
env = gym.make('TicTacToe-v0', players=[-1, 1], board_size=3, win_size=3) 
```

As the TicTacToe is a two players game, you have to create two players (here we use random as action choosing strategy). The environment is not handling the two players part, so you have to do it in your code as shown below.
> **Note on actions**: Every action is a two-element array `[cell_index, player_index]`. The first value specifies the board cell (0-based index), and the second indicates which player (by index 0 or 1 into the `players` list) places the mark.

```python
player = 0
terminated = False
truncated = False
reward = 0

# Reset the env before playing
last_state, info = env.reset()

env.render()

while not (terminated or truncated):
    # Random action
    action = env.action_space.sample()[0]
    while last_state[action] != 0:
        action = env.action_space.sample()[0]
    
    if player == 0:
        state, reward, terminated, truncated, infos = env.step([action, player])
    elif player == 1:
        state, reward, terminated, truncated, infos = env.step([action, player])

    env.render()
    # If the game isn't over, change the current player
    if not (terminated | truncated):
        player = 0 if player == 1 else 1
    else :
        if reward == 10:
            print("Draw !")
        elif reward == -20:
            print("Infos : " + str(infos))
            if player == 0:
                print("Random wins ! Reward : " + str(reward))
            elif player == 1:
                print("AI wins ! Reward : " + str(-reward))
        elif reward == 20:
            if player == 0:
                print("AI wins ! Reward : " + str(reward))
            elif player == 1:
                print("Random wins ! Reward : " + str(reward))
```

*Warning : If you play on a position where you or your opponent already played, you'll get a 'bad_position' reward and will loose the game*

## Configuration

After installation, locate `settings.xml` in your Python site-packages under `gym_tictactoe`. You can adjust:

| Parameter         | Description                       | Default |
|-------------------|-----------------------------------|---------|
| `reward_win`      | Reward for winning the game       | 20      |
| `reward_loss`     | Penalty for losing                | -20     |
| `reward_draw`     | Reward for a draw                 | 10      |
| `reward_bad_move` | Penalty for invalid move          | -5      |

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Make your changes and add tests
4. Submit a Pull Request

Please follow the existing coding style and include clear commit messages.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Forked and maintained by César Luis Guzmán to support Gymnasium.*
