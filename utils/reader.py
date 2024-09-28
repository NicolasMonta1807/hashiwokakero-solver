import numpy as np

def readgame(filename):
  with open(filename, 'r') as f:
    try:
      dimensions = f.readline().strip().split(",")      
      rows = int(dimensions[0])
      
      matrix = []
      
      for _ in range(rows):
        line = f.readline().strip()
        row = [int(char) for char in line]
        matrix.append(row)
    
      return np.array(matrix)
    except FileNotFoundError:
      # TODO: Better handle exception
      print("File not found")
      exit()
      
    