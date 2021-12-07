import sys
from typing_extensions import NotRequired
import math
from copy import deepcopy
from grid import get_neighbors, Node

class AstarNode(Node):
    def __init__(self, row, col, node_type):
        super().__init__(row, col, node_type)
        self.h_cost = sys.maxsize
        self.g_cost = sys.maxsize
        self.f_cost = sys.maxsize
        self.root_node = None

    def calculate_h_cost(self, finish_node):
        row_move = math.copysign(1, finish_node.row - self.row)
        col_move = math.copysign(1, finish_node.col - self.col)
        row = self.row
        col = self.col
        cost = 0

        while row != finish_node.row and col != finish_node.col:
            cost += 14
            col += col_move
            row += row_move
        
        while row != finish_node.row:
            cost += 10
            row += row_move
        
        while col != finish_node.col:
            cost += 10
            col += col_move

        self.h_cost = cost
        return cost

    def calculate_g_cost(self, root_node):
        move_cost = 10 if self.row == root_node.row or self.col == root_node.col else 14
        g_cost = move_cost + root_node.g_cost

        if g_cost < self.g_cost:
            self.g_cost = g_cost
            self.root_node = root_node

        return self.g_cost

    def calculate_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost
        return self.f_cost

def get_current_grid(grid, open_set, closed_set, node_types):
    grid = deepcopy(grid)

    for node in open_set:
        grid[node.row][node.col].node_type = node_types['Open']

    for node in closed_set:
        grid[node.row][node.col].node_type = node_types['Explored']

    return grid

def find_path(grid, node_config):
    open_set = []
    closed_set = []
    grid_history = []

    node_types = node_config['nodeTypes']

    grid = [[AstarNode(node['row'], node['col'], node['nodeType']) for node in row] for row in grid]

    start_node = [[node.node_type == node_types['Start'] for node in row] for row in grid]
    if max(max(start_node)) == False:
        return 0, None
    start_node = grid[start_node.index(max(start_node))][max(start_node).index(max(max(start_node)))]

    finish_node = [[node.node_type == node_types['Finish'] for node in row] for row in grid]
    if max(max(finish_node)) == False:
        return 1, None
    finish_node = grid[finish_node.index(max(finish_node))][max(finish_node).index(max(max(finish_node)))]

    open_set.append(start_node)
    current_node = start_node

    start_node.calculate_h_cost(finish_node)
    start_node.g_cost = 0
    start_node.calculate_f_cost()

    while not current_node is finish_node:
        neighbors = get_neighbors(current_node, grid)
        
        for neighbor in neighbors:
            neighbor.calculate_g_cost(current_node)
            
            
            if neighbor in open_set or neighbor in closed_set:                
                continue

            if neighbor.node_type != node_types['Obstacle']:
                neighbor.calculate_h_cost(finish_node)
                neighbor.calculate_f_cost()
                open_set.append(neighbor)
            
        open_set.remove(current_node)
        closed_set.append(current_node)

        grid_history.append(get_current_grid(grid, open_set, closed_set, node_types))
        
        if not open_set:
            return 2, grid_history

        current_node = min(open_set, key=lambda x: x.f_cost)


    path = []
    while not current_node is start_node:
        path.append(current_node)
        current_node = current_node.root_node

    return path, grid_history