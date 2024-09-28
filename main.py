import pygame
from utils import reader, consts
from src.board import Board

filename = ("./boards/example.txt")

gameMatrix = reader.readgame(filename)

board = Board(gameMatrix)

board.generateBoard()

print("Nodes: ", board.nodes)
print()
print("Bridges: ", board.possibleEdges)