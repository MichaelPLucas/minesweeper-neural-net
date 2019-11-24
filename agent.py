import numpy as np

class Agent:
  def __init__(self, num_tiles):
    self.num_tiles = num_tiles
    self.weights = np.empty((num_tiles, 50))
    self.hweights = np.empty((50, num_tiles))
    self.learning_rate = -.001

  def get_next_move(self, board):
    input_matrix = self.convert_to_matrix(board)

  def convert_to_matrix(self, board):
    matrix = np.zeros((1, self.num_tiles))
    for tile in board.tiles.values():
      value = -1
      if tile.revealed:
        value = sum([1 for neighbor in board.get_neighbors((tile.x, tile.y)) if neighbor.is_bomb])
      matrix[tile.x + tile.y * board.width] = value
    return matrix