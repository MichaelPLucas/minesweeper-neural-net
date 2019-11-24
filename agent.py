import numpy as np
from graphics import Point

class Agent:
  def __init__(self, num_tiles):
    self.num_tiles = num_tiles
    self.weights = np.random.rand(25, 20)
    self.hweights = np.random.rand(20, 1)
    self.learning_rate = .1

  def sigmoid(self, x, w):
    z = np.dot(x, w)
    return 1 / (1 + np.exp(-z))

  def sigmoid_deriv(self, x, w):
    return self.sigmoid(x, w) * (1 - self.sigmoid(x, w))

  def run(self, x):
    hlayer = self.sigmoid(x, self.weights)
    return (hlayer, self.sigmoid(hlayer, self.hweights))

  def get_loss(self, y, yhat):
    return y - yhat

  def train(self, board):
    predictions = {}
    for point, y in self.get_dataset(board):
      xs = self.get_frame(board, point)
      hlayer, yhat = self.run(xs)
      predictions[(point.x, point.y)] = yhat[0][0]

      loss = self.get_loss(y, yhat)

      hweights_grad = np.dot(hlayer.T, loss * self.sigmoid_deriv(hlayer, self.hweights))
      weights_grad = np.dot(xs.T, np.dot(loss * self.sigmoid_deriv(hlayer, self.hweights), hlayer) * self.sigmoid_deriv(xs, self.weights))

      self.weights += weights_grad * self.learning_rate
      self.hweights += hweights_grad * self.learning_rate
    return predictions

  def get_dataset(self, board):
    dataset = []
    for tile in board.tiles.values():
      if not tile.revealed and any([board.tiles[n].revealed for n in board.get_neighbors(Point(tile.x, tile.y))]):
        y = np.array([[1 if tile.is_bomb else 0]])
        dataset.append((Point(tile.x, tile.y), y))
    return dataset

  # Get a 5x5 frame around the point in question.
  # This represents all surrounding tiles and all the tiles they are touching.
  # The idea is to capture all information which indicates whether or not the given tile is a bomb.
  def get_frame(self, board, point):
    frame = np.zeros((1, 25))
    for x in range(-2, 2):
      for y in range(-2, 2):
        index = x + y * 5 + 12
        if x + point.x < 0 or y + point.y < 0 or x + point.x >= board.width or y + point.y >= board.height:
          frame[0][index] = 0
        elif board.tiles[(point.x + x, point.y + y)].flagged:
          frame[0][index] = -1
        elif board.tiles[(point.x + x, point.y + y)].revealed:
          neighbors = board.get_neighbors(Point(point.x, point.y))
          bomb_count = sum([1 if board.tiles[n].is_bomb else 0 for n in neighbors])
          frame[0][index] = bomb_count
    return frame