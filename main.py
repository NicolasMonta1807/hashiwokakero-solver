import pygame
from utils import reader
from src.board_view import BoardView
from src.board_logic import BoardLogic
import sys

def main(filename):  
  gameMatrix = reader.readgame(filename)

  pygame.init()
  pygame.mixer.stop()
  
  logic = BoardLogic(gameMatrix)
  
  view = BoardView(logic)
  view.initScreen()

  clock = pygame.time.Clock()
  pygame.display.set_caption("Hashiwokakero - By TwoMates")
  while True:      
    view.update()
    clock.tick(120)

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print(f"Usage python3 {sys.argv[0]} board-file")
    exit()
  
  filename = sys.argv[1]
  
  main(filename)