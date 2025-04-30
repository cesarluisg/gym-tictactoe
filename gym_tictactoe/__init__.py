from gymnasium.envs.registration import register

register(
    id="TicTacToe-v0",
    entry_point="gym_tictactoe.tic_tac_toe:TicTacToeEnv"
)