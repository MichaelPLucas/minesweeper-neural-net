# Minesweeper Neural Net

This is an implementation of a basic minesweeper game in python along with a neural net to pay the game. As someone who has played a lot of minesweeper this seemed like a fun project to pick up to see if I could create an AI to play better than myself.

## Implementation Details

As it stands the neural net uses 5x5 tile frames as inputs and collects info on the number of bombs around tiles on the fringe of the revealed area. The neural net has a 25 > 10 > 1 layout of layer sizes and assumes 0 bias for simplicity, although I intend to change this as a part of fine-tuning the networks hyper-parameters. The network uses the sigmoid function as it's activation function and currently uses simple subtraction as it's loss function. This is again subject to change drastically. This project uses numpy so make sure to install that before attempting to use it.

## Usage

To run minesweeper simply run `python game.py`. The following options are allowed.
```
usage: game.py [-h]
               [--difficulty {beginner,intermediate,expert,custom_standard,custom}]
               [--width WIDTH] [--height HEIGHT] [--num_bombs NUM_BOMBS]
               [--input {mouse,agent}]

Start up a game of minesweeper

optional arguments:
  -h, --help            show this help message and exit
  --difficulty {beginner,intermediate,expert,custom_standard,custom}
                        The game difficulty.
  --width WIDTH         The board width. To be used with 'custom' difficulty.
  --height HEIGHT       The board height. To be used with 'custom' difficulty.
  --num_bombs NUM_BOMBS
                        The number of bombs. To be used with 'custom'
                        difficulty.
  --input {mouse,agent}
                        The input type for the game.
```
The default is mouse control on expert difficulty.