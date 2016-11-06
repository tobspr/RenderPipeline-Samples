

# This is just the launcher, have a look at src/GameControl.py

import os
import sys

print("This sample is currently broken! Please wait until it is fixed. You can "
      "run it on your own risk by commenting line 10 in this file.")
# sys.exit(0)

# Change to the current directory
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__))))

# Append the current directory to the path
sys.path.insert(0, os.getcwd())

from src.GameControl import GameControl
game = GameControl()
game.run()
