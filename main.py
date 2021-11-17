from types import LambdaType
from typing import Dict
import pygame, math
from pygame.mouse import get_pressed
from pygame.surface import Surface
import colors as cl
from queue import PriorityQueue
from spot import Spot

def h(p1: tuple[int,int], p2: tuple[int,int]) -> int:
  #Uses Euclidian distance to calculate distance between two points
  x1, y1 = p1
  x2, y2 = p2
  t = (x1-x2)**2 + (y1-y2)**2
  return int(10*math.sqrt(t))


def reconstruct_path(came_from: Dict, current: Spot, draw: LambdaType) -> None:
  '''
  Reconstructs the shortest path from the start node to the end node, tracing back using the came_from dict
  '''
  while current in came_from:
    current = came_from[current]
    current.make_path()
    draw()


def algorithm(draw: LambdaType, grid: list[list[Spot]], start: Spot, end: Spot) -> bool:
  '''
  The algorithm that implements A* Pathfinding
  A* pathfinding basically takes each spot, and gives an h score to its neighbors
  h score is determined by sitance from the start spot (known) + distance to the end(approximated) (g and f score)
  Keep applying h scores to neighbor spots, going by the lowest h score first, until end is reached
  Traces back the shortest path

  Uses the priorityQueue() function to easily draw the least element from the Queue (lowest h score)
  '''
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start)) #puts start node into the queue, first entry is h score, second is the order it was put in, 3rd is the object
  came_from = {} #keeps track which node a node came from previously
  g_score = {spot: float("inf") for row in grid for spot in row} #dictionary that keeps track of g scores (distance from start node)
  g_score[start] = 0
  f_score = {spot: float("inf") for row in grid for spot in row} #dictionary that keeps track of f scores (approx. distance from end node)
  f_score[start] = h(start.get_pos(), end.get_pos())

  open_set_hash = {start} #Keep track of items that are not in the priority queue

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
    
    current = open_set.get()[2] # gets and removes the node that has the lowest h score (tiebreaker its count)

    if current == end: #found the shortest path
      reconstruct_path(came_from, end, draw)
      end.make_end()
      start.make_start()
      return True

    for neighbor in current.diagonal_neighbors: 
      temp_g_score = g_score[current] + 14

      #if the current path has a better path then its neighbors, update the neighbors path to be the optimized one
      if temp_g_score < g_score[neighbor]:
        came_from[neighbor] = current
        g_score[neighbor] = temp_g_score
        f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) #update h score

        if neighbor not in open_set_hash: #add neighbor to the queue with updated h score
          count += 1
          open_set.put((f_score[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
          neighbor.make_open()
    
      draw()

      if current != start:
        current.make_closed() #can't be revisited
    
    for neighbor in current.neighbors: 
      temp_g_score = g_score[current] + 10

      #if the current path has a better path then its neighbors, update the neighbors path to be the optimized one
      if temp_g_score < g_score[neighbor]:
        came_from[neighbor] = current
        g_score[neighbor] = temp_g_score
        f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) #update h score

        if neighbor not in open_set_hash: #add neighbor to the queue with updated h score
          count += 1
          open_set.put((f_score[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
          neighbor.make_open()
    
      draw()

      if current != start:
        current.make_closed() #can't be revisited
    


def make_grid(rows: int, width: int) -> list[list[Spot]]:
  '''
  returns a 2 dimensional grid, calculates the gap between rows for cell size
  '''
  grid = []
  gap = width // rows

  for i in range(rows): 
    grid.append([])
    for j in range(rows):
      spot = Spot(i, j, gap, rows)
      grid[i].append(spot)
  
  for rowIndex, row in enumerate(grid): #making outside a border
    if rowIndex == 0 or rowIndex == len(grid)-1:
      for spot in row:
        spot.make_barrier()
    else:
      row[0].make_barrier()
      row[-1].make_barrier()

  
  return grid


def draw_grid(win: Surface, rows: int, width: int) -> None:
  '''
  Draws the lines of the grid 
  '''
  gap = width// rows
  for i in range(rows):
    pygame.draw.line(win, cl.GREY, (0,i*gap), (width, i*gap))
    for j in range(rows):
      pygame.draw.line(win, cl.GREY, (j*gap, 0), (j*gap, width))  


def draw(win: Surface, grid: list[list[Spot]], rows: int, width: int) -> None:
  '''
  draws the window, lines included
  '''
  win.fill(cl.WHITE)
  for row in grid:
    for spot in row:
      spot.draw(win)
  
  draw_grid(win, rows, width)
  pygame.display.update()


def get_clicked_pos(pos :tuple[int,int], rows: int, width: int) -> tuple[int,int]:
  '''
  get the row and column of the clicked position
  '''
  gap = width // rows
  y,x = pos
  
  row = y // gap
  col = x // gap
  return row,col


def main(win: Surface, width: int) -> None:
  '''
  The main function of the program, runs a loop that simulates the search algorithm and setup
  '''
  ROWS = 30
  grid = make_grid(ROWS ,width)

  start = None
  end = None

  run = True
  started = False

  #main loop, process whenever an event happens and determines what to do
  while run:
    draw(win, grid, ROWS, width)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if started:
        continue #prevents user form doing anything while algorithm is being visualized

      if pygame.mouse.get_pressed()[0]: #if left mouse button is pressed, create a start/end/barrier in that order
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, ROWS, width)
        spot = grid[row][col]

        #ensures that both the start and end are placed before placaing any barriers, and not on top of each other
        if not start and spot != end:
          start = spot
          start.make_start()

        elif not end and spot != start:
          end = spot
          end.make_end()
        
        elif spot != end and spot != start:
          spot.make_barrier()
      
      elif pygame.mouse.get_pressed()[2]: #if right mouse button is pressed,resets the current spot
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, ROWS, width)
        spot = grid[row][col]

        spot.reset()

        if spot == start: start = None
        elif spot == end: end = None
      
      if event.type == pygame.KEYDOWN: 
        #runs the algorithm if the space key is pressed
        if event.key == pygame.K_SPACE and not started and start and end:
          for row in grid:
            for spot in row:
              spot.update_neighbors(grid)
              spot.update_diagonal_neighbors(grid)
            
          algorithm(lambda: draw(win, grid, ROWS ,width),grid, start, end)

        #clears the board
        if event.key == pygame.K_c:
          start = None
          end = None
          grid = make_grid
          grid = make_grid(ROWS, width)


  pygame.quit()


if __name__ == "__main__":
  WINDOW_WIDTH = 900
  WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_WIDTH))
  pygame.display.set_caption("A* path finding algorithm")
  main(WINDOW,WINDOW_WIDTH)









