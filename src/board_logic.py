class BoardLogic:
    def __init__(self, matrix, update_callback=None):
        self.size = len(matrix)
        self.matrix = matrix
        self.nodes = []
        self.possibleEdges = []
        self.userEdges = []
        self.generateBoard()
        self.update_callback = update_callback

    def generateBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] != 0:
                    self.nodes.append((i, j))

        for u in self.nodes:
            if u[1] < self.size - 1:
                for i in range(1, self.size):
                    v = (u[0], u[1] + i)
                    if v in self.nodes:
                        self.possibleEdges.append([0, [u, v]])
                        break

            if u[0] < self.size - 1:
                for i in range(1, self.size):
                    v = (u[0] + i, u[1])
                    if v in self.nodes:
                        self.possibleEdges.append([0, [u, v]])
                        break

    def isCrossing(self, newEdge):
        (x1, y1), (x2, y2) = newEdge[1]
        
        def cross_product(p1, p2, p3):
            return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

        def is_point_on_segment(p1, p2, p):
            return (min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and
                    min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1]))

        for edge in self.userEdges:
            (x3, y3), (x4, y4) = edge[1]
            p1, p2 = (x1, y1), (x2, y2)
            p3, p4 = (x3, y3), (x4, y4)
            
            d1 = cross_product(p3, p4, p1)
            d2 = cross_product(p3, p4, p2)
            d3 = cross_product(p1, p2, p3)
            d4 = cross_product(p1, p2, p4)
            
            if d1 * d2 < 0 and d3 * d4 < 0:
                return True

        return False

    def onEdgeClick(self, edge):
        if self.isCrossing(edge):
            return

        edge[0] = (edge[0] + 1) % 3
        existing_edge_index = None
        for i, e in enumerate(self.userEdges):
            if e[1] == edge[1]:
                existing_edge_index = i
                break

        if edge[0] != 0:
            if existing_edge_index is not None:
                self.userEdges[existing_edge_index] = edge
            else:
                self.userEdges.append(edge)
        else:
            if existing_edge_index is not None:
                del self.userEdges[existing_edge_index]

    def getEdgeCount(self, x, y):
        count = 0
        for edge in self.userEdges:
            if (x, y) in edge[1]:
                count += edge[0]
        return count

    def checkIfSolved(self):
        for i in range(self.size):
            for j in range(self.size):
                nodeValue = self.matrix[i][j]
                if nodeValue != 0:
                    count = self.getEdgeCount(i, j)
                    if count != nodeValue:
                        return False
        return True

    def solve(self):
        if not self.possibleEdges:
            self.generateBoard()
            
        while self.applyHeuristics():
            if self.update_callback:
                self.update_callback()
            
        if self.automaticSolve():
            print("Game solved")
        else:
            print("No solution")

    def applyHeuristics(self):
        # Aplicar las heurísticas para simplificar el tablero antes de resolver exhaustivamente
        changes_made = False

        for i in range(self.size):
            for j in range(self.size):
                nodeValue = self.matrix[i][j]
                if nodeValue == 0:
                    continue

                # Encontrar todos los vecinos conectados al nodo actual
                neighbors = [edge for edge in self.possibleEdges if (i, j) in edge[1]]
                
                # Heurística 1: Si el nodo tiene el mismo número de vecinos que el valor del nodo
                if len(neighbors) == nodeValue:
                    for edge in neighbors:
                        if edge[0] < 2 and not self.isCrossing(edge):  # Verificar si el puente no cruza
                            edge[0] = 2
                            if edge not in self.userEdges:
                                self.userEdges.append(edge)
                                print("Heurística 1 aplicada")
                            changes_made = True
                
                # Heurística 2: Si el nodo tiene valor 1 y solo un vecino
                elif nodeValue == 1 and len(neighbors) == 1:
                    edge = neighbors[0]
                    if edge[0] < 1 and not self.isCrossing(edge):  # Verificar si el puente no cruza
                        edge[0] = 1
                        if edge not in self.userEdges:
                            self.userEdges.append(edge)
                            print("Heurística 2 aplicada")
                        changes_made = True

        return changes_made

    def automaticSolve(self, edgeIndex=0):
        if edgeIndex >= len(self.possibleEdges):
            return self.checkIfSolved()

        edge = self.possibleEdges[edgeIndex]
        
        for bridges in [0, 1, 2]:
            edge[0] = bridges
            if bridges > 0:
                if not self.isCrossing(edge):
                    self.userEdges.append(edge)
                else:
                    continue
            else:
                if edge in self.userEdges:
                    self.userEdges.remove(edge)
            
            if self.update_callback:
                self.update_callback()
            
            if self.automaticSolve(edgeIndex + 1):
                return True

            if edge in self.userEdges:
                self.userEdges.remove(edge)
                
            if self.update_callback:
                self.update_callback()

        return 
