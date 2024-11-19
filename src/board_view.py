import pygame
import math
from utils import consts
from src.board_logic import BoardLogic

class _NumberTextImageCache:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.surfaces = [self.font.render(str(i), True, consts.BLACK) for i in range(10)]

    def Draw(self, screen, pos, number):
        surface = self.surfaces[number]
        screen.blit(surface, surface.get_rect(center=pos))

class BoardView:
    def __init__(self, logic : BoardLogic):
        self.logic = logic
        self.textCache = _NumberTextImageCache()
        self.screenSurface = None
        self.drawPosition = (consts.EDGE_PADDING, consts.EDGE_PADDING)
        self.nodeSpacing = consts.NODES_SPACING
        self.screenSize = [consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT]
        
        self.logic.update_callback = self.update

    def initScreen(self):
        self.screenSurface = pygame.display.set_mode(self.screenSize, pygame.DOUBLEBUF)

    def getDrawPosition(self, node):
        return (self.drawPosition[1] + node[1] * self.nodeSpacing, self.drawPosition[0] + node[0] * self.nodeSpacing)

    def distanceToEdge(self, point, edge):
        # Unpack the coordinates using the drawing positions
        (x1, y1) = self.getDrawPosition(edge[1][0])
        (x2, y2) = self.getDrawPosition(edge[1][1])
        (x3, y3) = point

        # Calculate the direction vector
        dirx = x2 - x1
        diry = y2 - y1
        dirSq = float(dirx ** 2 + diry ** 2)

        # Parametric equation to find the projection
        u = ((x3 - x1) * dirx + (y3 - y1) * diry) / dirSq
        u = min(max(0, u), 1)

        px = x1 + u * dirx
        py = y1 + u * diry

        dx = px - x3
        dy = py - y3

        return math.sqrt(dx ** 2 + dy ** 2)
    
    def isSolveButtonPressed(self, mouse_pos):
        button_position = [consts.SCREEN_WIDTH - consts.BUTTON_WIDTH, consts.SCREEN_HEIGHT - consts.BUTTON_HEIGHT]
        button_rect = pygame.Rect(button_position[0], button_position[1], consts.BUTTON_WIDTH, consts.BUTTON_HEIGHT)
        
        return button_rect.collidepoint(mouse_pos)
        
    def handleClick(self, mouse_pos, threshold=20):
        
        if self.isSolveButtonPressed(mouse_pos):
            self.logic.solve()
            return
        
        for edge in self.logic.possibleEdges:
            distance = self.distanceToEdge(mouse_pos, edge)
            if distance <= threshold:
                self.logic.onEdgeClick(edge)
                break

    def drawSolveButton(self):
        button_position = [consts.SCREEN_WIDTH - consts.BUTTON_WIDTH, consts.SCREEN_HEIGHT - consts.BUTTON_HEIGHT]
        button_rect = pygame.Rect(button_position[0], button_position[1], consts.BUTTON_WIDTH, consts.BUTTON_HEIGHT)
        pygame.draw.rect(self.screenSurface, consts.GREEN, button_rect)
        font = pygame.font.Font(None, consts.NORMAL_FONT)
        text_surface = font.render("Solve", True, consts.BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screenSurface.blit(text_surface, text_rect)

    def drawNodes(self):
        for u in self.logic.nodes:
            pygame.draw.circle(self.screenSurface, consts.WHITE, self.getDrawPosition(u), 16)
            pygame.draw.circle(self.screenSurface, consts.BLACK, self.getDrawPosition(u), 16, 1)
            self.textCache.Draw(self.screenSurface, self.getDrawPosition(u), self.logic.matrix[u[0]][u[1]])

    def drawPossibleEdges(self):
        for edge in self.logic.possibleEdges:
            source = self.getDrawPosition(edge[1][0])
            destination = self.getDrawPosition(edge[1][1])
            pygame.draw.line(self.screenSurface, consts.GRAY, source, destination, consts.EDGE_WITH)

    def drawUserEdges(self):
        for edge in self.logic.userEdges:
            source = self.getDrawPosition(edge[1][0])
            destination = self.getDrawPosition(edge[1][1])
            
            # Dibujar la línea
            pygame.draw.line(self.screenSurface, consts.BLACK, source, destination, consts.USER_EDGE_WIDTH)
            
            # Calcular el punto medio de la línea y ajustar el offset según la orientación
            if edge[1][0][0] == edge[1][1][0]:  # Línea vertical
                midpoint = ((source[0] + destination[0]) // 2, ((source[1] + destination[1]) // 2) - consts.VERTICAL_OFFSET)
            else:  # Línea horizontal
                midpoint = (((source[0] + destination[0]) + consts.HORIZONTAL_OFFSET) // 2, (source[1] + destination[1]) // 2)
            
            # Renderizar el texto que indica la cantidad de puentes
            font = pygame.font.Font(None, consts.NORMAL_FONT)
            label = font.render(str(edge[0]), True, consts.BLACK)
            
            # Obtener el rectángulo de texto y centrarlo en el punto medio con offset
            text_rect = label.get_rect(center=midpoint)
            
            # Dibujar el texto en la pantalla
            self.screenSurface.blit(label, text_rect)

    def drawWinner(self):
        self.screenSurface.fill(consts.WHITE)
        screen_center = (consts.SCREEN_WIDTH / 2, consts.SCREEN_HEIGHT / 2)
        text_box = pygame.Rect(0, 0, consts.BUTTON_WIDTH, consts.BUTTON_HEIGHT)
        text_box.center = screen_center
        pygame.draw.rect(self.screenSurface, consts.WHITE, text_box)
        font = pygame.font.Font(None, consts.NORMAL_FONT)
        text_surface = font.render("You Win!", True, consts.GREEN)
        text_rect = text_surface.get_rect(center=text_box.center)
        self.screenSurface.blit(text_surface, text_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(pygame.mouse.get_pos())
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.screenSurface.fill(consts.WHITE)
        self.drawPossibleEdges()
        self.drawUserEdges()
        self.drawNodes()
        self.drawSolveButton()
        pygame.display.flip()

        # if self.logic.checkIfSolved():
        #     self.drawWinner()
