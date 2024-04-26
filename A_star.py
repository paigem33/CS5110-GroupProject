import math
import heapq
from Agent import Agent
 
# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination
        # self.agent = agent # store an agent in the cell as well :)
 

class A_Star:
    def __init__(self, row, col):
        self.ROW = row
        self.COL = col
 
    # Check if a cell is valid (within the grid)
    def is_valid(self, row, col):
        return (row >= 0) and (row < self.ROW) and (col >= 0) and (col < self.COL)
    
    # Check if a cell is unblocked
    def is_unblocked(self, grid, row, col):
        return grid[row][col] == 0
    
    # Check if a cell is in the destination (on row 0)
    def is_destination(self, row, col):
        return row == 0
    
    # Calculate the heuristic value of a cell (Euclidean distance to destination)
    def calculate_h_value(self, row, col):
        return row  # Distance to row 0
    
    # Trace the path from source to destination
    def trace_path(self, cell_details, dest):
        # print("The Path is ")
        path = []
        row = dest[0]
        col = dest[1]
    
        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col
    
        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()
    
        # Print the path
        # for i in path:
        #     print("->", i, end=" ")
        # print()

    # this function returns the first step in the path (that isn't the cell the agent is already in)
    def first_step_of_path(self, cell_details, dest):
        path = []
        row = dest[0]
        col = dest[1]
    
        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col
    
        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()
        return path[1]
    
    # Implement the A* search algorithm
    # takes only grid and starting point as params, will find fastest to row 0 around the obstacles
    def a_star_search(self, grid, src):
        # Check if the source is valid
        if not self.is_valid(src[0], src[1]):
            print("Source is invalid")
            return
    
        # Check if we are already at the destination
        if self.is_destination(src[0], src[1]):
            # print("We are already at the destination")
            return
    
        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.COL)] for _ in range(self.ROW)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(self.COL)] for _ in range(self.ROW)]  # start grid with cell details?
    
        # Initialize the start cell details
        i = src[0]
        j = src[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j
    
        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))
    
        # Initialize the flag for whether destination is found
        found_dest = False
    
        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)
    
            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True
    
            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]
    
                # If the successor is valid, unblocked, and not visited
                if self.is_valid(new_i, new_j) and self.is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if self.is_destination(new_i, new_j):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        # print("The destination cell is found")
                        # Trace and print the path from source to destination
                        self.trace_path(cell_details, [new_i, new_j])
                        firstStep = self.first_step_of_path(cell_details, [new_i, new_j]) # added this, it returns first step of path
                        found_dest = True
                        return firstStep # return the first step of the path from the algorithm
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.calculate_h_value(new_i, new_j)
                        f_new = g_new + h_new
    
                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j
    
            if found_dest:
                break

        # If the destination is not found after visiting all cells
        if not found_dest:
            # print("Failed to find the destination cell")
            return None
 