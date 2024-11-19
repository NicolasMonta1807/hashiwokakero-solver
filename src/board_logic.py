from src.text_to_csv import txt_to_csv
from src.solver import solve, draw_grid, Node

class BoardLogic:
    def __init__(self, matrix, filename, update_callback=None):
        self.source = filename
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

    def solve(self):
        csv_filename = self.source.replace('.txt', '.csv')
        txt_to_csv(self.source, csv_filename)

        grid = self.gen_grid(csv_filename)

        solved_grid, steps = solve(grid)

        print(f"Solved in {steps} steps")

        draw_grid(solved_grid)

    # Método para generar la cuadrícula a partir del archivo .csv
    def gen_grid(self, csv_file):
        grid = []
        with open(csv_file, 'r') as file:
            data = file.readline().split(";;")
            width, height = int(data[0]), int(data[1])
            grid_data = data[2]

            # Crear nodos a partir de los datos de la cuadrícula
            index = 0
            for i in range(width):
                row = []
                for j in range(height):
                    node = Node(i, j)
                    if grid_data[index] != '0':
                        node.make_island(int(grid_data[index]))
                    row.append(node)
                    index += 1
                grid.append(row)

        return grid
