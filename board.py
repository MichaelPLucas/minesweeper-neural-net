import random
from graphics import Point

class Tile:
  def __init__(self, x, y, is_bomb):
    self.x = x
    self.y = y
    self.is_bomb = is_bomb
    self.revealed = False

class Board:
  def __init__(self, width, height, num_bombs):
    self.width = width
    self.height = height
    self.num_bombs = num_bombs
    self.tiles = {}

  def generate_new_board(self, point):
    bombs = random.sample([(x, y) for y in range(self.height) for x in range(self.width) if not (point.x - 1 <= x <= point.x + 1 and point.y - 1 <= y <= point.y + 1)], k=self.num_bombs)
    tiles = [Tile(x, y, (x, y) in bombs) for y in range(self.height) for x in range(self.width)]
    for tile in tiles:
      self.tiles[(tile.x, tile.y)] = tile

  def flood_fill(self, point, seen):
    if (point.x, point.y) in seen:
      return seen

    self.tiles[(point.x, point.y)].revealed = True
    seen.append((point.x, point.y))

    if self.tiles[(point.x, point.y)].is_bomb:
      return seen

    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if self.tiles[neighbor].is_bomb:
        return seen

    flooded = []
    for neighbor in neighbors:
      flooded += self.flood_fill(Point(neighbor[0], neighbor[1]), seen)
    
    return seen + flooded

  def flood_count(self, point, seen):
    if (point.x, point.y) in seen:
      return len(seen)

    seen.append((point.x, point.y))

    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if self.tiles[neighbor].is_bomb:
        return len(seen)

    flooded = []
    for neighbor in neighbors:
      flooded += self.flood_fill(Point(neighbor[0], neighbor[1]), seen)
    
    return len(seen) + len(flooded)

  def get_neighbors(self, point):
    neighbors = []
    x, y = point.x, point.y
    if x > 0:
      neighbors.append((x - 1, y))
      if y > 0:
        neighbors.append((x, y - 1))
        neighbors.append((x - 1, y - 1))
      if y < self.height - 1:
        neighbors.append((x, y + 1))
        neighbors.append((x - 1, y + 1))
    if x < self.width - 1:
      neighbors.append((x + 1, y))
      if y > 0:
        if not (x, y - 1) in neighbors: neighbors.append((x, y - 1))
        neighbors.append((x + 1, y - 1))
      if y < self.height - 1:
        if not (x, y + 1) in neighbors: neighbors.append((x, y + 1))
        neighbors.append((x + 1, y + 1))
    return neighbors

  def print_board(self):
    bomb_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
    for tile in self.tiles.values():
      bomb_grid[tile.y][tile.x] = 1 if tile.is_bomb else 0
    for row in bomb_grid:
      print(row)