import argparse
import random
import time
from graphics import *
from board import *
from agent import *

parser = argparse.ArgumentParser(description="Start up a game of minesweeper")
parser.add_argument("--difficulty",
                    default="expert",
                    choices=["beginner", "intermediate", "expert", "custom_standard", "custom"],
                    help="The game difficulty.")
parser.add_argument("--width",
                    default=30,
                    type=int,
                    help="The board width. To be used with 'custom' difficulty.")
parser.add_argument("--height",
                    default=24,
                    type=int,
                    help="The board height. To be used with 'custom' difficulty.")
parser.add_argument("--num_bombs",
                    default=200,
                    type=int,
                    help="The number of bombs. To be used with 'custom' difficulty.")
parser.add_argument("--input",
                    default="mouse",
                    choices=["mouse", "agent"],
                    help="The input type for the game.")
args = parser.parse_args()

tile_width = 20
tile_height = 20
boards = {}
boards["beginner"] = Board(9, 9, 10)
boards["intermediate"] = Board(16, 16, 40)
boards["expert"] = Board(30, 16, 99)
boards["custom_standard"] = Board(30, 24, 200)

def draw_tile(tile, board, window):
  p1 = Point(tile.x * tile_width, tile.y * tile_height)
  p2 = Point((tile.x + 1) * tile_width, (tile.y + 1) * tile_height)
  t = Rectangle(p1, p2)
  if tile.revealed:
    t.setFill(color_rgb(200, 200, 200))
    t.draw(window)
    if tile.is_bomb:
      bomb = Circle(Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), tile_width / 3)
      bomb.setFill(color_rgb(0, 0, 0))
      bomb.draw(window)
    else:
      neighbors = board.get_neighbors(Point(tile.x, tile.y))
      bomb_count = sum([1 if board.tiles[point].is_bomb else 0 for point in neighbors])
      if bomb_count > 0:
        text = Text(Point((tile.x + .5) * tile_width, (tile.y + .6) * tile_height), str(bomb_count))
        text.setSize(int(tile_height / 2))
        text.draw(window)
  else:
    t.setFill(color_rgb(150, 150, 150))
    t.draw(window)
    if tile.flagged:
      tri = Polygon(Point((tile.x + .15) * tile_width, (tile.y + .15) * tile_height),
                    Point((tile.x + .15) * tile_width, (tile.y + .85) * tile_height),
                    Point((tile.x + .85) * tile_width, (tile.y + .5) * tile_height))
      tri.setFill(color_rgb(255, 50, 50))
      tri.draw(window)

def main():
  if args.difficulty == "custom":
    board = Board(args.width, args.height, args.num_bombs)
  else:
    board = boards[args.difficulty]
  width = board.width * tile_width
  height = board.height * tile_height
  window = GraphWin("Minesweeper", width=width, height=height)
  board.generate_new_board(Point(0, 0))
  agent = Agent(board.width * board.height)
  for tile in board.tiles.values():
    draw_tile(tile, board, window)

  # Normal game flow for player control
  if args.input == "mouse":
    first_click = window.getMouse()
    first_point = Point(int(first_click.x / tile_width), int(first_click.y / tile_height))
    board.generate_new_board(first_point)
    flooded = board.flood_fill(first_point, [])

    while True:
      for point in list(set(flooded)):
        draw_tile(board.tiles[point], board, window)
    
      click = window.getMouse()
      point = Point(int(click.x / tile_width), int(click.y / tile_height))

      if board.tiles[(point.x, point.y)].is_bomb:
        main()
        break

      flooded = board.flood_fill(point, [])

    window.close()
  
  # Game flow for agent training and action
  else:
    point = random.choice(list(board.tiles.keys()))
    board.generate_new_board(Point(point[0], point[1]))
    flooded = board.flood_fill(Point(point[0], point[1]), [])

    while True:
      for point in list(set(flooded)):
        draw_tile(board.tiles[point], board, window)

      predictions = agent.train(board)
      to_flag = []
      to_click = []
      flooded = []
      for point, prediction in predictions.items():
        if prediction > .8:
          board.tiles[point].flagged = True
          flooded.append(point)
        else:
          board.tiles[point].flagged = False
          flooded.append(point)
        if prediction < .3:
          if board.tiles[point].is_bomb:
            point = random.choice(list(board.tiles.keys()))
            board.generate_new_board(Point(point[0], point[1]))
            board.flood_fill(Point(point[0], point[1]), [])
            flooded = list(board.tiles.keys())
            for point in list(set(flooded)):
              draw_tile(board.tiles[point], board, window)
            flooded = []
            continue
          flooded += board.flood_fill(Point(point[0], point[1]), [])

main()