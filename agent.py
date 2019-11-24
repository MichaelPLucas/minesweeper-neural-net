import numpy as np
from graphics import Point

class Agent:
  def __init__(self, num_tiles):
    self.num_tiles = num_tiles
    self.weights = np.random.rand(num_tiles, num_tiles)
    self.hweights = np.random.rand(num_tiles, num_tiles)
    self.learning_rate = -.001

  def get_move(self, board):
    input_matrix = self.convert_to_matrix(board)
    layer1 = np.matmul(input_matrix, self.weights)
    layer1 = np.maximum(layer1, 0) # ReLU
    scores = np.matmul(layer1, self.hweights)

    ex_scores = [np.exp(scores) for score in scores]
    ex_sum = sum(ex_scores)
    softmax_scores = [ex_score / ex_sum for ex_score in ex_scores]

    actual_scores = self.get_actual_scores(board)

    loss = sum([actual_scores[i] - softmax_scores[i] for i in range(len(actual_scores))]) / len(actual_scores)
    deriv_loss = [[l if l > 0 else 0 for l in loss[0]]]

    weights_gradient = np.dot(layer1.T, deriv_loss)
    hweights_gradient = np.dot(scores.T, deriv_loss)

    self.weights += weights_gradient * self.learning_rate
    self.hweights += hweights_gradient * self.learning_rate

    best_index = softmax_scores.index(max(softmax_scores))
    return Point(best_index % board.width, int(best_index / board.width))

  def convert_to_matrix(self, board):
    matrix = np.zeros((1, self.num_tiles))
    for tile in board.tiles.values():
      value = -1
      if tile.revealed:
        value = sum([1 for neighbor in board.get_neighbors(Point(tile.x, tile.y)) if board.tiles[neighbor].is_bomb])
      matrix[0][tile.x + tile.y * board.width] = value
    return matrix

  def get_actual_scores(self, board):
    matrix = np.zeros((1, self.num_tiles))
    for tile in board.tiles.values():
      if tile.is_bomb:
        matrix[0][tile.x + tile.y * board.width] = -5
      else:
        matrix[0][tile.x + tile.y * board.width] = board.flood_count(Point(tile.x, tile.y), [])
    return matrix