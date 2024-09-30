from utils import consts
import pygame
import math

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
    self.textCache = _NumberTextImageCache()
    self.drawPosition = (consts.EDGE_PADDING, consts.EDGE_PADDING)
    self.nodeSpacing = consts.NODES_SPACING
    self.screenSize = [consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT]
    self.userEdges = []

  def generateBoard(self):
    # Use matrix to get available nodes
    for i in range(self.size):
      for j in range (self.size):
        if self.matrix[i][j] != 0:
          self.nodes.append((i, j))
    
    for u in self.nodes:
      # Check if horizontal neighbours are possible
      if u[1] < self.size - 1:
        # Check entire row for first neighbour
        for i in range(1, self.size):
          v = (u[0], u[1] + i)
          if v in self.nodes:
            # A horizontal neighbour exists and can be connected
            # Edge has value 0 since no initial bridges are connected
            self.possibleEdges.append([0, [u, v]])
            break
      
      # Check if vertical neighbours are possible
      if u[0] < self.size - 1:
        # Check entire column for first neighbour
        for i in range(1, self.size):
          v = (u[0] + i, u[1])
          if v in self.nodes:
            # A vertical neighbour exists and can be connected
            # Edge has value 0 since no initial bridges are connected
            self.possibleEdges.append([0, [u, v]])
            break
  
  def initScreen(self):
    # Generates game screen display
    self.screenSurface = pygame.display.set_mode(self.screenSize, pygame.DOUBLEBUF)
  
  def getDrawPosition(self, node):
    # Uses node matrix position to calculate display relative position
    return (self.drawPosition[1] + node[1] * self.nodeSpacing, self.drawPosition[0] + node[0] * self.nodeSpacing)
  
  def drawSolveButton(self):
    button_position = [consts.SCREEN_WIDTH - consts.BUTTON_WIDTH, consts.SCREEN_HEIGHT - consts.BUTTON_HEIGHT]
    button_rect = pygame.Rect(button_position[0], button_position[1], consts.BUTTON_WIDTH, consts.BUTTON_HEIGHT)
    
    pygame.draw.rect(self.screenSurface, consts.GREEN, button_rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Solve", True, consts.BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    self.screenSurface.blit(text_surface, text_rect)
  
  def drawNodes(self):
    # Calculates position for every node and draws a circle with given value
    for u in self.nodes:
      pygame.draw.circle(self.screenSurface, consts.WHITE, self.getDrawPosition(u), 16)
      pygame.draw.circle(self.screenSurface, consts.BLACK, self.getDrawPosition(u), 16, 1)
      self.textCache.Draw(self.screenSurface, self.getDrawPosition(u), self.matrix[u[0]][u[1]])
  
  def drawPossibleEdges(self):
    for edge in self.possibleEdges:
      source = self.getDrawPosition(edge[1][0])
      destination = self.getDrawPosition(edge[1][1])
      pygame.draw.line(self.screenSurface, consts.GRAY, source, destination, 1)
  
  def drawUserEdges(self):
    if len(self.userEdges) == 0:
      return

    for edge in self.userEdges:
      source = self.getDrawPosition(edge[1][0])
      destination = self.getDrawPosition(edge[1][1])
      pygame.draw.line(self.screenSurface, consts.BLACK, source, destination, 5)
     
  def distanceToEdge(self, point, edge):
    # Unpack the coordinates of the line segment and the point
    (x1, y1) = self.getDrawPosition(edge[1][0])
    (x2, y2) = self.getDrawPosition(edge[1][1])
    (x3, y3) = point
    
    # Direction vector of the line segment
    dirx = x2 - x1
    diry = y2 - y1
    
    # Length squared of the direction vector (magnitude squared)
    dirSq = float(dirx ** 2 + diry ** 2)
    
    # Parametric equation of the point projection
    u = ((x3 - x1) * dirx + (y3 - y1) * diry) / dirSq
    
    # Clamp u to the range [0, 1] to ensure projection is on the segment
    u = min(max(0, u), 1)
    
    # Calculate the closest point (px, py) on the line segment to the point (x3, y3)
    px = x1 + u * dirx
    py = y1 + u * diry
    
    # Calculate the difference (distance vector) between the closest point and the point
    dx = px - x3
    dy = py - y3
    
    # Return the squared distance
    return math.sqrt(dx ** 2 + dy ** 2)
  
  def onEdgeClick(self, edge):
    # Switch edge value from 0,1 and 2
    edge[0] = (edge[0] + 1) % 3
    
    # Check if the edge already exists in userEdges (based on connected nodes)
    existing_edge_index = None
    for i, e in enumerate(self.userEdges):
        if e[1] == edge[1]:  # Compare the connected nodes
            existing_edge_index = i
            break

    if edge[0] != 0:
        if existing_edge_index is not None:
            # Update the existing edge's value
            self.userEdges[existing_edge_index] = edge
        else:
            # Add the new edge if it doesn't exist
            self.userEdges.append(edge)
    else:
        # Remove the edge if edge[0] is 0
        if existing_edge_index is not None:
            del self.userEdges[existing_edge_index]
  
  def handleClick(self, mouse_pos):
    # Distance to be considered an edge selection
    treshold = 10 # Pixels
    
    for edge in self.possibleEdges:
      distance = self.distanceToEdge(mouse_pos, edge)
      
      if distance <= treshold:
        self.onEdgeClick(edge)
  
  def update(self):
    # Function to run with every clock tick
    self.screenSurface.fill(consts.WHITE)
    self.drawPossibleEdges()
    self.drawUserEdges()
    self.drawNodes()
    self.drawSolveButton()
    
    for event in pygame.event.get():
      match event.type:
        case pygame.MOUSEBUTTONDOWN:
          self.handleClick(pygame.mouse.get_pos())
        case pygame.QUIT:
          pygame.quit()
          exit() 
