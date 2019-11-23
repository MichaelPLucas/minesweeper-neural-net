import random

class Tile:
  def __init__(self, x, y, is_bomb):
    self.x = x
    self.y = y
    self.is_bomb = is_bomb
    self.revealed = True

class Board:
  def __init__(self, width, height, num_bombs):
    self.width = width
    self.height = height
    self.num_bombs = num_bombs
    self.tiles = {}

  def generate_new_board(self):
    bombs = random.sample([(x, y) for y in range(self.height) for x in range(self.width)], k=self.num_bombs)
    tiles = [Tile(x, y, (x, y) in bombs) for y in range(self.height) for x in range(self.width)]
    for tile in tiles:
      self.tiles[(tile.x, tile.y)] = tile

  def print_board(self):
    bomb_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
    for tile in self.tiles.values():
      bomb_grid[tile.y][tile.x] = 1 if tile.is_bomb else 0
    for row in bomb_grid:
      print(row)