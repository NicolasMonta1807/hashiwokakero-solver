import pygame
from utils import reader, consts

filename = ("./boards/example.txt")

gameMatrix = reader.readgame(filename)

print(gameMatrix)