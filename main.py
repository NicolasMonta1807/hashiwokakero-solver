import pygame
from utils import reader, consts
from src.board import Board
import sys

def main(filename):
  gameMatrix = reader.readgame(filename)

  pygame.init()
  board = Board(gameMatrix)
  board.generateBoard()
  board.initScreen(512, 512)

  clock = pygame.time.Clock()
  pygame.display.set_caption("Hashiwokakero - By TwoMates")
  solved = False
  while not solved:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        solved = True
      else:
        continue
    board.update()
    clock.tick(120)
    pygame.display.flip()
pygame.quit()

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print(f"Usage python3 {sys.argv[0]} board-file")
    exit()
  
  filename = sys.argv[1]
  
  main(filename)