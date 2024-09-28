import numpy as np

class Board:
  def __init__(self, matrix):
    self.size = len(matrix)
    self.matrix = matrix
    self.nodes = []
    self.possibleEdges = []

  def generateBoard(self):
    for i in range(self.size):
      for j in range (self.size):
        if self.matrix[i][j] != 0:
          self.nodes.append((i, j))
    
    for u in self.nodes:
      # Check if horizontal neighbours are possible
      if u[0] < self.size - 1:
        # Check entire row for first neighbour
        for i in range(1, self.size):
          v = (u[0], u[1] + i)
          if v in self.nodes:
            # A horizontal neighbour exists and can be connected
            self.possibleEdges.append((1, (u, v)))
            break
      
      # Check if vertical neighbours are possible
      if u[1] < self.size - 1:
        # Check entire column for first neighbour
        for i in range(1, self.size):
          v = (u[0] + i, u[1])
          if v in self.nodes:
            # A vertical neighbour exists and can be connected
            self.possibleEdges.append((1, (u, v)))
            break
         
         