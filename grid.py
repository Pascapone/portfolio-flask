import random

class Node:
    def __init__(self, row, col, node_type):
        self.row = row
        self.col = col
        self.node_type = node_type

def get_neighbors(node, grid):
        neighbors = []
        rows = len(grid)
        cols = len(grid[0])

        for row in range(-1, 2):
            for col in range(-1, 2):
                if row == 0 and col == 0: continue
                elif node.col + col >= cols or node.row + row >= rows: continue
                elif node.col + col < 0 or node.row + row < 0: continue

                neighbors.append(grid[row + node.row][col + node.col])

        return neighbors     

def create_grid(node_config, num_obstacles, stick_percentage, rows, cols):      
    
    node_types = node_config['nodeTypes']
    grid = [[Node(row, col, node_types['Unblocked']) for col in range(cols)] for row in range(rows)]

    open_set = [node for row in grid for node in row if node.node_type == node_types['Unblocked']] 
    stick_set = []
    for _ in range(num_obstacles):
        current_node = None        
        if random.random() > stick_percentage or not stick_set: 
            index = random.randint(0, len(open_set) - 1)
            current_node = open_set[index]
            current_node.node_type = node_types['Obstacle']
                        
            open_set.remove(current_node)  
            if current_node in stick_set:
                stick_set.remove(current_node)
            
        else:
            index = random.randint(0, len(stick_set) - 1)
            current_node = stick_set[index]
            current_node.node_type = node_types['Obstacle']
            
            stick_set.remove(current_node)
            if current_node in open_set:
                open_set.remove(current_node)            
          
        neighbors = get_neighbors(current_node, grid)
        open_neighbours = [node for node in neighbors if node.node_type == node_types['Unblocked']]

        for neighbor in open_neighbours:
            if neighbor in stick_set: 
                continue
            stick_set.append(neighbor)

    index = random.randint(0, len(open_set) - 1)
    current_node = open_set[index]
    current_node.node_type = node_types['Start']
    open_set.remove(current_node) 

    index = random.randint(0, len(open_set) - 1)
    current_node = open_set[index]
    current_node.node_type = node_types['Finish']
    open_set.remove(current_node) 

    return grid