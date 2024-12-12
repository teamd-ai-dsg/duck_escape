Snake Game README
Welcome to the Snake Game! This game features two distinct gameplay modes: Normal and Hard. Below is a description of each mode and how they function.

Modes
1. Normal Mode (normal.py)
In Normal Mode, the game offers a recreation of the classic Snake experience, dating back to 1985. Here's how it works:

Randomized Movement: The snake's next direction is determined randomly using the random module. The game doesn't involve any complex decision-making algorithms; it’s purely based on chance.
Shooting: The snake will shoot randomly when the opportunity arises. This randomness mimics the unpredictability of the original game.
2. Hard Mode (hard.py)
Hard Mode offers a more challenging gameplay experience with advanced AI behavior. Here’s how it differs:

A Search*: The snake uses a limited A* search algorithm to determine its next move. A* is a well-known pathfinding algorithm that helps the snake navigate through the environment to get closer to the player.
Scripted Backup Actions: If the A* algorithm fails to find a valid direction, the snake falls back on a scripted action pattern, which includes:
Jiggling: The snake makes quick, unpredictable movements to throw off the player.
Charging: The snake will charge towards the player in a more aggressive manner.
Shooting Mechanism: The snake will only shoot when it is aligned with the player’s snake. This ensures a more strategic and deliberate approach to attacking.

Installation
To play the game, you will need to have Python installed on your computer.

Clone the repository:
bash
Copy code
git clone https://github.com/teamd-ai-dsg
duck_escape.git

Navigate to the directory containing the game files:
bash
Copy code

Run the desired mode:
For Normal Mode:
bash
Copy code
python normal.py

For Hard Mode:
bash
Copy code
python hard.py

Dependencies
This game requires Python 3.12. The following libraries are used:
gamepy
numpy
random
deque


How to Play
In Normal Mode, you can expect a more casual, retro experience with random movement and shooting.
In Hard Mode, be prepared for a tougher opponent with more strategic behavior driven by pathfinding and reactive actions.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Enjoy the game and have fun mastering each mode!
