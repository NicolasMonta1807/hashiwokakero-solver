from src.node import Node, direction_to_vector, is_in_grid
from src.ui_elements import Button, ProcessElements
from src.arg_parser import parse_args
import pygame
import os

ABS_DIR: str = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FONT_PATH: str = ABS_DIR + '/data/SpaceMono-Regular.ttf'


def print_node_data(node: Node) -> None:
    print(f"Node at ({node.x}, {node.y})")
    print(f"Type: {node.n_type}")
    print("-------------------------")
    print(f"Island count: {node.i_count}")
    print(f"Island current_in: {node.current_in}")
    print(f"Island needed: {node.needed}")
    print("-------------------------")
    print(f"Bridge thickness: {node.b_thickness}")
    print(f"Bridge direction: {node.b_dir}")
    print("-------------------------\n")


def grid_to_surface(grid_size: tuple[int, int], grid: list[list[Node]], cell_unit: int) -> None:
    """
    Draws the background grid, bridges and islands to the passed surface.
    """
    pygame.init()
    offset = (int(cell_unit * 0.75), int(cell_unit * 0.75))
    root_size = (grid_size[0] + offset[0], grid_size[1] + offset[1])
    root = pygame.display.set_mode(root_size)
    font: pygame.font.Font = pygame.font.Font(None, 36)
    grid_width = len(grid)
    grid_height = len(grid[0])
    line_thickness = int(cell_unit / 15)
    all_islands: list[Node] = []
    for i in range(grid_width):
        for j in range(grid_height):
            if grid[i][j].n_type == 1:
                all_islands.append(grid[i][j])
    grid_surface: pygame.surface.Surface = pygame.Surface(grid_size)

    root.fill((255, 255, 255))
    for i in range(grid_width):
        text_surface = font.render(str(i), False, (0, 0, 0))
        text_size = text_surface.get_size()
        position = (cell_unit // 2 + i * cell_unit - text_size[0] / 2 + offset[0], 0)
        root.blit(text_surface, position)
    for j in range(grid_height):
        text_surface = font.render(str(j), False, (0, 0, 0))
        text_size = text_surface.get_size()
        position = (0, cell_unit // 2 + j * cell_unit - text_size[1] / 2 + offset[1])
        root.blit(text_surface, position)    

    grid_surface.fill((255, 255, 255))
    cursor = int(cell_unit / 2), int(cell_unit / 2)
    for j in range(grid_width):
        pygame.draw.line(grid_surface, (220, 220, 220), (cursor[0] + j * cell_unit, 0), (cursor[0] + j * cell_unit, root_size[1]), line_thickness // 2)
    for i in range(grid_height):
        pygame.draw.line(grid_surface, (220, 220, 220), (0, cursor[1] + i * cell_unit), (root_size[0], cursor[1] + i * cell_unit), line_thickness // 2)

    drawn_bridges = []
    for i in range(grid_width):
        for j in range(grid_height):
            if grid[i][j].n_type == 2 and [i, j] not in drawn_bridges:
                bridge_direction = grid[i][j].b_dir
                current = [i, j]
                nodes_of_bridge = [current,]
                vector = direction_to_vector(bridge_direction)
                thickness = grid[i][j].b_thickness
                forward_found = False
                backward_found = False
                index = 1
                while not (forward_found and backward_found):
                    if not forward_found:
                        forward = [current[0] + vector[0] * index, current[1] + vector[1] * index]
                        if is_in_grid(forward[0], forward[1], grid_width, grid_height):
                            nodes_of_bridge.append(forward)
                            if grid[forward[0]][forward[1]].n_type == 1:
                                forward_found = True
                                
                    if not backward_found:
                        backward = [current[0] - vector[0] * index, current[1] - vector[1] * index]
                        if is_in_grid(backward[0], backward[1], grid_width, grid_height):
                            nodes_of_bridge.insert(0, backward)
                            if grid[backward[0]][backward[1]].n_type == 1:
                                backward_found = True
                    index += 1
                drawn_bridges.extend(nodes_of_bridge)
                start_pos = (nodes_of_bridge[0][0] * cell_unit + cell_unit // 2, nodes_of_bridge[0][1] * cell_unit + cell_unit // 2)
                end_pos = (nodes_of_bridge[-1][0] * cell_unit + cell_unit // 2, nodes_of_bridge[-1][1] * cell_unit + cell_unit // 2)
                if thickness == 1:
                    pygame.draw.line(grid_surface, (0, 0, 0), start_pos, end_pos, line_thickness)
                else:
                    opposite_direction = (bridge_direction + 1)
                    if opposite_direction % 2 == 0:
                        pygame.draw.line(grid_surface, (0, 0, 0), (start_pos[0] + cell_unit / 15, start_pos[1]), (end_pos[0] + cell_unit // 15, end_pos[1]), line_thickness)
                        pygame.draw.line(grid_surface, (0, 0, 0), (start_pos[0] - cell_unit / 15, start_pos[1]), (end_pos[0] - cell_unit // 15, end_pos[1]), line_thickness)
                    else:
                        pygame.draw.line(grid_surface, (0, 0, 0), (start_pos[0], start_pos[1] + cell_unit / 15), (end_pos[0], end_pos[1] + cell_unit // 15), line_thickness)
                        pygame.draw.line(grid_surface, (0, 0, 0), (start_pos[0], start_pos[1] - cell_unit / 15), (end_pos[0], end_pos[1] - cell_unit // 15), line_thickness)


    # draw the islands
    for island in all_islands:
        position = (cell_unit // 2 + island.x * cell_unit, cell_unit // 2 + island.y * cell_unit)
        pygame.draw.circle(grid_surface, (0, 0, 0), position, int(cell_unit / 2.3))
        pygame.draw.circle(grid_surface, (255, 255, 255), position, int(cell_unit / 2.5))
        text_surface = font.render(str(island.i_count), False, (0, 0, 0))
        text_size = text_surface.get_size()
        grid_surface.blit(text_surface, (position[0] - text_size[0] / 2, position[1] - text_size[1] / 2))
    root.blit(grid_surface, offset)
    return root


def draw_grid(grid: list[list[Node]]) -> None:
    """
    Takes a 2D list of nodes and draws it on the screen with Pygame.
    """
    pygame.init()
    grid_width = len(grid)
    grid_height = len(grid[0])
    ratio = grid_width / grid_height
    if ratio > 1:
        window_size = (800, int(800 / ratio))
    else:
        window_size = (int(800 * ratio), 800)
    cell_size = window_size[0] // grid_width
    root: pygame.surface.Surface = grid_to_surface(window_size, grid, cell_size)
    pygame.display.set_caption("Hashiwokakero Grid Visualizer")
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        pygame.display.update()
    pygame.quit()


def main():
    import sys
    grid = parse_args(sys.argv)
    if grid == -1:
        return
    draw_grid(grid)


if __name__ == "__main__":
    main()
