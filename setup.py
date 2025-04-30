from setuptools import setup, find_packages

setup(name='gym_tictactoe',
      version='0.1.1',
      description='Light TicTacToe Gymnasium environment',
      author='Clement Romac',
      author_email='clement.romac@gmail.com',
      maintainer="César Guzmán",
      maintainer_email="cesarluisg@gmail.com",
      url="https://github.com/cesarluisg/gym-tictactoe",
      license="MIT",
      packages=find_packages(),
      #include_package_data=True,
      package_data={              
         "gym_tictactoe": ["settings.xml"],
      },      
      install_requires=[
        "gymnasium>0.26.0",
        "numpy"
      ],
      dependency_links=[],
      entry_points={
        "gymnasium.envs": [
            "TicTacToe-v0 = gym_tictactoe.tic_tac_toe:TicTacToeEnv",
        ],
      },
)