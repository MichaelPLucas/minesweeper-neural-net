from graphics import *
from board import *

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


def main():
  if sys.argv[1] == "custom":
    board = Board(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
  else:
    board = boards[sys.argv[1]]
  width = board.width * tile_width
  height = board.height * tile_height
  window = GraphWin("Minesweeper", width=width, height=height)
  board.generate_new_board(Point(0, 0))
  for tile in board.tiles.values():
    draw_tile(tile, board, window)

  first_click = window.getMouse()
  first_point = Point(int(first_click.x / tile_width), int(first_click.y / tile_height))
  board.generate_new_board(first_point)
  flooded = board.flood_fill(first_point, [])

  while True:
    for point in flooded:
      draw_tile(board.tiles[point], board, window)
    click = window.getMouse()
    point = Point(int(click.x / tile_width), int(click.y / tile_height))
    flooded = board.flood_fill(point, [])

  window.getMouse()
  window.close()

main()