from utils import consts
import pygame

class _NumberTextImageCache:
	def __init__(self):
		self.font = pygame.font.Font(None, 36)
		self.surfaces = []
		for i in range(0, 10):
			self.surfaces.append(self.font.render(str(i), True, consts.BLACK))

	def Draw(self, screen, pos, number):
		surface = self.surfaces[number]
		screen.blit(surface, surface.get_rect(center = pos))

class Board:
  def __init__(self, matrix):
    self.size = len(matrix)
    self.matrix = matrix
    self.nodes = []
    self.possibleEdges = []
    self.screenSurface = None
    self.numberCache = _NumberTextImageCache()
    self.drawPosition = (consts.EDGE_PADDING, consts.EDGE_PADDING)
    self.nodeSpacing = consts.NODES_SPACING

  def generateBoard(self):
    # Use matrix to get available nodes
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
  
  def initScreen(self, widht, height):
    # Generates game screen display
    screenSize = [widht, height]
    self.screenSurface = pygame.display.set_mode(screenSize, pygame.DOUBLEBUF)
  
  def getDrawPosition(self, node):
    # Uses node matrix position to calculate display relative position
    return (self.drawPosition[1] + node[1] * self.nodeSpacing, self.drawPosition[0] + node[0] * self.nodeSpacing)
  
  def drawNodes(self, screen):
    # Calculates position for every node and draws a circle with given value
    for u in self.nodes:
      pygame.draw.circle(screen, consts.WHITE, self.getDrawPosition(u), 16)
      pygame.draw.circle(screen, consts.BLACK, self.getDrawPosition(u), 16, 1)
      self.numberCache.Draw(screen, self.getDrawPosition(u), self.matrix[u[0]][u[1]])
  
  def update(self):
    # Function to run with every clock tick
    self.screenSurface.fill(consts.WHITE)
    self.drawNodes(self.screenSurface)