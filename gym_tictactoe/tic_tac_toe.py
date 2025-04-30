import gymnasium as gym
import numpy as np
from gymnasium import spaces, error
import xml.etree.ElementTree as ET
import os
from typing import Any, Literal


class TicTacToeEnv(gym.Env):
    def __init__(self, players, board_size=3, win_size=3, seed=1234):
        super(TicTacToeEnv, self).__init__()
        self.win_size = win_size
        self.board_size = board_size
        self.symbols = {
            players[0]: "x",
            players[1]: "o"
        }
        self.players = [players[0], players[1]]
        self.action_space = spaces.MultiDiscrete([self.board_size * self.board_size, 2])
        self.observation_space = spaces.MultiDiscrete([3] * self.board_size * self.board_size)
        settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.xml')
        self.load_xml_settings(settings_file)
        self.truncated = False
        self.terminated = False

    def load_xml_settings(self, settings_file):
        settings_tree = ET.parse(settings_file)
        settings_root = settings_tree.getroot()
        for child in settings_root:
            if child.tag == 'Rewards':
                self.set_rewards(child)

    def set_rewards(self, rewards_section):
        self.rewards = {}
        for reward in rewards_section:
            self.rewards[reward.attrib['description']] = int(reward.attrib['reward'])

    def reset(self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,):
        
        self.terminated = False
        self.truncated = False
        super().reset(seed=seed, options=options)
        self.state_vector = np.zeros(self.board_size * self.board_size)
        info = {}
        return self.state_vector, info 

    # ------------------------------------------ GAME STATE CHECK ----------------------------------------
    def is_win(self):
        if self.check_horizontal():
            return True

        if self.check_vertical():
            return True

        return self.check_diagonal()

    def check_horizontal(self):
        grid = self.state_vector
        cnt = 0
        for i in range(0, self.board_size * self.board_size, self.board_size):
            cnt = 0
            k = i
            for j in range(1, self.board_size):
                (cnt, k) = (cnt + 1, k) if (grid[k] == grid[i + j] and grid[k] != 0) else (0, i + j)
                if cnt == self.win_size - 1:
                    return True

        return False

    def check_horizontal_size(self, line_size):
        #Warning! work only if win_size <= 3 and board_size <=4
        grid = self.state_vector
        cnt = 0
        hor_lines = 0
        for i in range(0, self.board_size * self.board_size, self.board_size):
            cnt = 0
            k = i
            for j in range(1, self.board_size):
                (cnt, k) = (cnt + 1, k) if (grid[k] == grid[i + j] and grid[k] != 0) else (0, i + j)
                if cnt == line_size - 1:
                    hor_lines += 1
                    break

        return hor_lines

    
    def check_vertical(self):
        grid = self.state_vector
        cnt = 0
        for i in range(0, self.board_size):
            cnt = 0
            k = i
            for j in range(self.board_size, self.board_size * self.board_size, self.board_size):
                (cnt, k) = (cnt + 1, k) if (grid[k] == grid[i + j] and grid[k] != 0) else (0, i + j)
                if cnt == self.win_size - 1:
                    return True

        return False

    def check_vertical_size(self, line_size):
        #Warning! work only if win_size <= 3 and board_size <=4
        grid = self.state_vector
        cnt = 0
        vert_lines = 0
        
        for i in range(0, self.board_size):
            cnt = 0
            k = i
            for j in range(self.board_size, self.board_size * self.board_size, self.board_size):
                (cnt, k) = (cnt + 1, k) if (grid[k] == grid[i + j] and grid[k] != 0) else (0, i + j)
                if cnt == self.win_size - 1:
                    vert_lines +=1
                    break

        return vert_lines


    def check_diagonal(self):
        grid = self.state_vector
        m = self.to_matrix(grid)
        m = np.array(m)

        for i in range(self.board_size - self.win_size + 1):
            for j in range(self.board_size - self.win_size + 1):
                sub_matrix = m[i:self.win_size + i, j:self.win_size + j]

                if self.check_matrix(sub_matrix):
                    return True

    def check_diagonal_size(self, line_size):
        grid = self.state_vector
        m = self.to_matrix(grid)
        m = np.array(m)
        diag_lines = 0

        for i in range(self.board_size - line_size + 1):
            for j in range(self.board_size - line_size + 1):
                sub_matrix = m[i:line_size + i, j:line_size + j]

                diag_lines += self.check_matrix_size(sub_matrix, line_size)
                
        return diag_lines

    def to_matrix(self, grid):
        m = []
        for i in range(0, self.board_size * self.board_size, self.board_size):
            m.append(grid[i:i + self.board_size])
        return m

    def check_matrix(self, m):
        cnt_primary_diag = 0
        cnt_secondary_diag = 0
        for i in range(self.win_size):
            for j in range(self.win_size):
                if i == j and m[0][0] == m[i][j] and m[0][0] != 0:
                    cnt_primary_diag += 1

                if i + j == self.win_size - 1 and m[0][self.win_size - 1] == m[i][j] and m[0][self.win_size - 1] != 0:
                    cnt_secondary_diag += 1

        return cnt_primary_diag == self.win_size or cnt_secondary_diag == self.win_size

    def check_matrix_size(self, m, line_size):
        cnt_primary_diag = 0
        cnt_secondary_diag = 0
        matrix_lines = 0
        
        for i in range(line_size):
            for j in range(line_size):
                if i == j and m[0][0] == m[i][j] and m[0][0] != 0:
                    cnt_primary_diag += 1

                if i + j == line_size - 1 and m[0][line_size - 1] == m[i][j] and m[0][line_size - 1] != 0:
                    cnt_secondary_diag += 1

        if cnt_primary_diag == line_size:
            matrix_lines += 1
        if cnt_secondary_diag == line_size:
            matrix_lines += 1
        
        return matrix_lines


    def is_draw(self):
        for i in range(self.board_size * self.board_size):
            if self.state_vector[i] == 0:
                return False
        return True

    # ------------------------------------------ ACTIONS ----------------------------------------
    def step(self, action_player):
        action = action_player[0]
        n_player = action_player[1]
        reward_type = 'still_in_game'
        error = False
        message = None
        
        if (action < 0) | (action >= self.board_size * self.board_size):
            message = 'bad_position'
            error = True
        elif n_player < 0 or n_player >= len(self.players):  
            message = 'bad_player'
            error = True

        if self.state_vector[action] != 0:
            message = 'bad_position'
            error = True

        if error:
            self.truncated = True
        else:
            self.state_vector[action] = self.players[n_player]

            if self.is_win():
                reward_type = 'win'
                self.terminated = True
            elif self.is_draw():
                reward_type = 'draw'
                self.terminated = True
            else:
                reward_type = 'still_in_game'

        return (self.state_vector, 
               self.rewards[reward_type], 
               self.terminated, 
               self.truncated, 
               {'message': message} if message else {})
    
    # ------------------------------------------ DISPLAY ----------------------------------------
    def get_state_vector_to_display(self):
        new_state_vector = []
        for value in self.state_vector:
            if value == 0:
                new_state_vector.append(value)
            else:
                new_state_vector.append(self.symbols[value])
        return new_state_vector

    def print_grid_line(self, grid, offset=0):
        print(" " + "-" * (self.board_size * 4 + 1))
        for i in range(self.board_size):
            if grid[i + offset] == 0:
                print(" | " + " ", end='')
            else:
                print(" | " + str(grid[i + offset]), end='')
        print(" |")

    def display_grid(self, grid):
        for i in range(0, self.board_size * self.board_size, self.board_size):
            self.print_grid_line(grid, i)

        print(" " + "-" * (self.board_size * 4 + 1))
        print()

    def render(self, mode=None, close=False):
        self.display_grid(self.get_state_vector_to_display())

    def close(self):
        return None

    def seed(self, seed=None):
        return [seed]
