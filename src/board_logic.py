# board_logic.py
class BoardLogic:
    def __init__(self, matrix):
        self.size = len(matrix)
        self.matrix = matrix
        self.nodes = []
        self.possibleEdges = []
        self.userEdges = []

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

            if d1 == 0 and is_point_on_segment(p3, p4, p1):
                continue
            if d2 == 0 and is_point_on_segment(p3, p4, p2):
                continue
            if d3 == 0 and is_point_on_segment(p1, p2, p3):
                continue
            if d4 == 0 and is_point_on_segment(p1, p2, p4):
                continue

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
