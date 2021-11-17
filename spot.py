import colors as cl
import pygame
from pygame.surface import Surface

class Spot:
  '''
  Spot class is a class used for keeping track of the attributes of each spot on the grid
  '''

  def __init__(self, row: int, col: int, width: int, total_rows: int):
    self.row = row
    self.col = col
    self.x = row * width
    self.y = col * width
    self.color = cl.WHITE
    self.neighbors = []
    self.diagonal_neighbors = []
    self.width = width
    self.total_rows = total_rows

  def get_pos(self) -> tuple[int, int]:
    #retrieves the current position of the spot
    return (self.row, self.col)
  
  def is_closed(self) -> bool:
    #determines if a current spot is closed
    return self.color == cl.RED
  
  def is_open(self) -> bool:
    #determines if a current spot is open
    return self.colol == cl.GREEN

  def is_barrier(self) -> bool:
    #determines it a current spot is a barrier
    return self.color == cl.BLACK
  
  def is_start(self) -> bool:
    #determines if a current spot is the starting spot
    return self.color == cl.ORANGE
  
  def is_end(self) -> bool:
    #determines if a current spot is the end spot
    return self.color == cl.PURPLE
  
  def reset(self) -> None:
    #resets the current spot
    self.color = cl.WHITE
  
  def make_closed(self) -> None:
    #Makes the current spot closed
    self.color = cl.RED
  
  def make_open(self) -> None:
    #Makes the current spot open
    self.color = cl.GREEN

  def make_barrier(self) -> None:
    #Makes the current spot a barrier
    self.color = cl.BLACK
  
  def make_start(self) -> None:
    #Makes the current spot the start spot
    self.color = cl.ORANGE
  
  def make_end(self) -> None:
    #Makes the current spot the end spot
    self.color = cl.TURQUOISE
  
  def make_path(self) -> None:
    #Makes the current spot a path
    self.color = cl.PURPLE
  
  def draw(self, win: Surface) -> None:
    #Draws the spot on the grid
    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

  def update_neighbors(self, grid) -> None:
    #check if the neighbord around are barriers
    self.neighbors = []
    if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #check if neighbor below is a barrier
      self.neighbors.append(grid[self.row + 1][self.col])
    
    if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #check if neighbor above is a barrier
      self.neighbors.append(grid[self.row - 1][self.col])
    
    if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #check if neighbor to the right is a barrier
      self.neighbors.append(grid[self.row][self.col + 1])
    
    if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #check if neighbor to the left is a barrier
      self.neighbors.append(grid[self.row][self.col - 1])
  
  def update_diagonal_neighbors(self,grid) -> None:
    self.diagonal_neighbors = []

    if self.col < self.total_rows - 1 and self.row < self.total_rows - 1\
    and not grid[self.row + 1][self.col].is_barrier()\
    and not grid[self.row][self.col+1].is_barrier()\
    and not grid[self.row+1][self.col+1].is_barrier(): #check if southeast node is a barrier
        self.diagonal_neighbors.append(grid[self.row + 1][self.col+1])  

    if self.col < self.total_rows - 1 and self.col > 0\
    and not grid[self.row - 1][self.col].is_barrier()\
    and not grid[self.row][self.col + 1].is_barrier()\
    and not grid[self.row-1][self.col + 1].is_barrier(): #check if southwest node is a barrier
        self.diagonal_neighbors.append(grid[self.row - 1][self.col+1])  
    
    if self.col > 0 and self.row < self.total_rows - 1\
    and not grid[self.row + 1][self.col].is_barrier()\
    and not grid[self.row][self.col - 1].is_barrier()\
    and not grid[self.row+1][self.col - 1].is_barrier(): #check if northeast node is a barrier
        self.diagonal_neighbors.append(grid[self.row + 1][self.col-1])  

    if self.col > 0 and self.col > 0\
    and not grid[self.row - 1][self.col].is_barrier()\
    and not grid[self.row][self.col - 1].is_barrier()\
    and not grid[self.row - 1][self.col - 1].is_barrier(): #check if northwest node is a barrier
        self.diagonal_neighbors.append(grid[self.row - 1][self.col-1])  
    

  
  def __lt__(self, other) -> bool:
    #handles comparing if one spot is less than another
    return False