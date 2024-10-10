import argparse
import heapq
import random
import math
from typing import Literal, Optional, Union

# ANSI color codes for the grid display
RESET = "\033[0m"
BG_BLACK = "\033[30m"
BG_RED = "\033[31m"
BG_GREEN = "\033[32m"
GB_YELLOW = "\033[33m"
BG_BLUE = "\033[34m"
BG_PURPLE = "\033[35m"

# Constants representing the values in the grid
BLANK = 0
START = 1
END = 2
WALL = 3




class Node:
    id: int
    state: int
    x: int
    y: int
    cost: float
    heuristic: float
    parent: Optional['Node']

    def __init__(self, id: int, state: int, x: int, y: int, cost: int = float('inf'), heuristic: int = 0):
        self.id = id
        self.state = state
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.parent = None
    

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        # Add a secondary tie-breaker (like item.id) to avoid comparing Node objects directly
        heapq.heappush(self.elements, (priority, item.id, item))  

    def get(self) -> 'Node':
        return heapq.heappop(self.elements)[2] 

def find_node(nodes, x, y):
    for line in nodes:
        for node in line:
            if node.x == x and node.y == y:
                return node
    return None


def generate_board(width, height, wall_percentage):
    if not (0 <= wall_percentage <= 100):
        raise ValueError("wall_percentage must be between 0 and 100")

    board = []
    id = 1

    for y in range(height):
        board.append([])
        for x in range(width):
            board[y].append(Node(id=id, state=BLANK, x=x, y=y))
            id+=1


    start_pos = (random.randint(0, height - 1), random.randint(0, width - 1))
    end_pos = (random.randint(0, height - 1), random.randint(0, width - 1))
    while end_pos == start_pos:
        end_pos = (random.randint(0, height - 1), random.randint(0, width - 1))

    total_cells = width * height
    num_walls = int(total_cells * (wall_percentage / 100))

    for _ in range(num_walls):
        while True:
            wall_pos = (random.randint(0, height - 1), random.randint(0, width - 1))
            if find_node(board, wall_pos[1], wall_pos[0]).state == BLANK:
                find_node(board, wall_pos[1], wall_pos[0]).state = WALL
                break

    start_node = find_node(board, start_pos[1], start_pos[0])
    end_node = find_node(board, end_pos[1], end_pos[0])

    start_node.state = START
    end_node.state = END

    return board, start_node, end_node


def display_grid(grid, path = None, closed_list = None):
    for row in grid:
        for cell in row:
            if cell.state == WALL:
                print(BG_RED + "██" + RESET, end="")
            elif cell.state == BLANK:
                if path != None and cell.id in [c.id for c in path]:
                    print(GB_YELLOW + "██" + RESET, end="")
                elif closed_list != None and cell in closed_list:
                    print(BG_PURPLE + "██" + RESET, end="")
                else:
                    print(BG_BLACK + "██" + RESET, end="")
            elif cell.state == START:
                print(BG_GREEN + "██" + RESET, end="")
            elif cell.state == END:
                print(BG_BLUE + "██" + RESET, end="")
        print()
    print()


def reconstruct_path(current):
    total = []

    while current.parent != None:
        total.append(current)
        current = current.parent

    return total

def heuristic(node1, node2):
    """Manhattan distance heuristic."""
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def reconstruct_path(end_node):
    current = end_node
    path = []
    while current is not None:
        path.append(current)
        current = current.parent
    path.reverse()
    return path

def get_neighbors(board, node: Node):
    neighbors = []
    for new_pos in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbors.append(find_node(board, node.x + new_pos[0], node.y + new_pos[1]))
    return neighbors


def a_star(board, start_node: Node, end_node: Node):
    open_list = PriorityQueue()
    open_list.put(start_node, 0)

    start_node.cost = 0
    start_node.heuristic = heuristic(start_node, end_node)

    closed_list = []

    while not open_list.is_empty():
        current_node = open_list.get()

        if current_node.x == end_node.x and current_node.y == end_node.y:
            return reconstruct_path(current_node), closed_list
        for neighbor in get_neighbors(board, current_node):
            new_cost = current_node.cost + 1
            if neighbor != None and neighbor not in closed_list and neighbor.state != WALL and (neighbor.cost == 0 or new_cost < neighbor.cost):
                neighbor.cost = new_cost
                neighbor.heuristic = heuristic(neighbor, end_node)
                priority = neighbor.cost + neighbor.heuristic
                open_list.put(neighbor, priority)
                neighbor.parent = current_node
        closed_list.append(current_node)
    return None




def main():
    parser = argparse.ArgumentParser(
        description="Generate and display a grid with walls, start, and end points."
    )
    parser.add_argument("width", type=int, help="The width of the grid.")
    parser.add_argument("height", type=int, help="The height of the grid.")
    parser.add_argument(
        "wall_percentage",
        type=float,
        help="The percentage of grid cells that should be walls (0-100).",
    )

    args = parser.parse_args()

    if args.width <= 0:
        raise ValueError("Width must be a positive integer.")
    if args.height <= 0:
        raise ValueError("Height must be a positive integer.")
    if not (0 <= args.wall_percentage <= 100):
        raise ValueError("wall_percentage must be between 0 and 100.")

    board, start_pos, end_pos = generate_board(args.width, args.height, args.wall_percentage)
    display_grid(board)

    path, closed_list = a_star(board, start_pos, end_pos)

    # print([c.id for c in path])


    display_grid(board, path=path, closed_list=closed_list)


if __name__ == "__main__":
    main()
