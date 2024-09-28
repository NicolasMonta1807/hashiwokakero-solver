import numpy as np

def readgame(filename):
  with open(filename, 'r') as f:
    try:
      lines = f.readlines()
      size = [int(x) for x in lines[0].split(',')]
      
      matrix = np.zeros(size, dtype=int)
      
      for i, line in enumerate(lines[1:]):
        for x in line:
          if x != '\n':
            matrix[i] = int(x)
    
      return matrix
    except FileNotFoundError:
      # TODO: Better handle exception
      print("File not found")
      exit()
      
    