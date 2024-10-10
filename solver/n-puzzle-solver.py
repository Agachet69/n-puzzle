import argparse
from copy import deepcopy
import json
import math
import time
from utils import PriorityQueue

SIZE = 3
UNSLOVED_BOARD = [
    [5, 8, 1],
    [6, 0, 3],
    [7, 4, 2],
]

# UNSLOVED_BOARD = [
#     [1, 0, 3],
#     [5, 2, 6],
#     [4, 7, 8],
# ]

def create_final_state(size):
    if (size <= 2):
        raise Exception('Wrong table format')
    max_val = (size * size) - 1

    correct_array = []
    number = 1


    while number < max_val:
        x = 0
        line = []
        
        while x < size:
            if number > max_val:
                line.append(0)
            else :
                line.append(number)
            x+=1
            number+=1

        correct_array.append(line)
    
    return correct_array

# SOLVED_BOARD = create_final_state(SIZE)



def generate_neighbbor(state):
    empty_pos_x, empty_pos_y = next((x, y) for y, row in enumerate(state) for x, value in enumerate(row) if value == 0)

    neighbors = []

    if empty_pos_x != 0:
        neighbor_state = deepcopy(state)
        neighbor_state[empty_pos_y][empty_pos_x] = neighbor_state[empty_pos_y][empty_pos_x - 1]
        neighbor_state[empty_pos_y][empty_pos_x - 1] = 0
        neighbors.append(neighbor_state)
    if empty_pos_x < SIZE - 1:
        neighbor_state = deepcopy(state)
        neighbor_state[empty_pos_y][empty_pos_x] = neighbor_state[empty_pos_y][empty_pos_x + 1]
        neighbor_state[empty_pos_y][empty_pos_x + 1] = 0
        neighbors.append(neighbor_state)
    if empty_pos_y != 0:
        neighbor_state = deepcopy(state)
        neighbor_state[empty_pos_y][empty_pos_x] = neighbor_state[empty_pos_y - 1][empty_pos_x]
        neighbor_state[empty_pos_y - 1][empty_pos_x] = 0
        neighbors.append(neighbor_state)
    if empty_pos_y < SIZE - 1:
        neighbor_state = deepcopy(state)
        neighbor_state[empty_pos_y][empty_pos_x] = neighbor_state[empty_pos_y + 1][empty_pos_x]
        neighbor_state[empty_pos_y + 1][empty_pos_x] = 0
        neighbors.append(neighbor_state)
    
    return neighbors


def manhatan_distance(state, final_state):
    total_distance = 0

    for y, row in enumerate(state):
        for x, value in enumerate(row):
            if value != 0:
                final_pos_x, final_pos_y = next((x, y) for y, row in enumerate(final_state) for x, v in enumerate(row) if v == value)
                total_distance += abs(x - final_pos_x) + abs(y - final_pos_y)
    
    return total_distance

def euclidian_distance(state, final_state):
    total_distance = 0

    for y, row in enumerate(state):
        for x, value in enumerate(row):
            if value != 0:
                final_pos_x, final_pos_y = next((x, y) for y, row in enumerate(final_state) for x, v in enumerate(row) if v == value)
                total_distance += math.sqrt((x - final_pos_x)**2 + (y - final_pos_y)**2)
    
    return total_distance

def tiles_out_of_places(state, final_state):
    total_distance = 0

    for y, row in enumerate(state):
        for x, value in enumerate(row):
            if value != 0:
                final_pos_x, final_pos_y = next((x, y) for y, row in enumerate(final_state) for x, v in enumerate(row) if v == value)
                if x != final_pos_x or y != final_pos_y:
                    total_distance += 1
    
    return total_distance

def reconstruct_path(final_state, parent):
    path = []

    while final_state != None:
        path.append(final_state)
        final_state = parent.pop() if len(parent) else None
    
    path.reverse()
    return path

def display_state(state):
    for row in state:
        print(" ".join([str(value) for value in row]))
    print()

def solve(heuristic, start, end):
    priority_queue = PriorityQueue()

    closed_list = {}

    initial_cost = 0

    if heuristic == "Manhatan-distance":
            calculate_heuristic = manhatan_distance
    if heuristic == "Euclidian-distance":
            calculate_heuristic = euclidian_distance
    if heuristic == "Tiles-out-of-places":
            calculate_heuristic = tiles_out_of_places

    heuristic = calculate_heuristic(start, end)

    priority_queue.add(initial_cost + heuristic, start, initial_cost, None)

    while not priority_queue.is_empty():
        priority, current_state, actual_cost, parent = priority_queue.pop()

        if current_state == end:
            return reconstruct_path(current_state, parent)
        
        closed_list[json.dumps(current_state)] = True

        for neighbor in generate_neighbbor(current_state):

            try:
                closed_list[json.dumps(neighbor)]
            except:
                neighbor_cost = actual_cost + 1

                neighbor_heuristic = calculate_heuristic(neighbor, end)

                priority_queue.add(neighbor_cost // SIZE + neighbor_heuristic, neighbor, neighbor_cost, parent + [current_state] if parent else [current_state])
    raise Exception('Not solvable.')

def is_solvable(board):
    def count_inversions(board):
        inv_count = 0
        board_flat = [tile for row in board for tile in row if tile != 0]  # Flatten board and exclude blank space (0)
        for i in range(len(board_flat)):
            for j in range(i + 1, len(board_flat)):
                if board_flat[i] > board_flat[j]:
                    inv_count += 1
        return inv_count

    size = len(board)
    inversions = count_inversions(board)

    if size % 2 == 1:  # Odd grid
        return inversions % 2 == 0
    else:  # Even grid
        blank_row = size - next(i for i, row in enumerate(board) if 0 in row)  # Find the blank row from the bottom
        return (inversions + blank_row) % 2 == 1


def parse_args():
    parser = argparse.ArgumentParser(description="Select a heuristic function.")
    parser.add_argument(
        '-H', '--heuristic',
        choices=['Manhatan-distance', 'Euclidian-distance', 'Tiles-out-of-places'],
        required=True,
        help="Select the heuristic function: \"Manhatan-distance\", \"Euclidian-distance\" or \"Tiles-out-of-places\"."
    )
    parser.add_argument(
        'path',
        type=str,
        help="Path to the input file containing the board."
    )
    return parser.parse_args()

def create_resolved(size):

    if (size <= 2):
        print('Wrong table format')
        return False
    
    max_val = (size * size) - 1


    correct_array = [[0] * size for _ in range(size)]

    x_pos = 0
    y_pos = 0


    for number in range(1, max_val + 1):
        correct_array[y_pos][x_pos] = number
        if x_pos + 1 < size and correct_array[y_pos][x_pos + 1] == 0 and (y_pos - 1 < 0 or correct_array[y_pos - 1][x_pos] != 0):
            x_pos += 1
        elif y_pos + 1 < size and correct_array[y_pos + 1][x_pos] == 0 :
            y_pos += 1
        elif x_pos - 1 >= 0 and correct_array[y_pos][x_pos - 1] == 0 :
            x_pos -= 1
        elif y_pos - 1 >= 0 and correct_array[y_pos - 1][x_pos] == 0 :
            y_pos -= 1
        
    return correct_array

def parse_board(file_path):
    board = []
    board_size = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.split('#')[0].strip()

            if not line:
                continue

            if board_size is None:
                try:
                    board_size = int(line)
                except ValueError:
                    raise ValueError("The first valid line must contain the board size.")
            else:
                row = line.split()
                if len(row) != board_size:
                    raise ValueError(f"Each row must have exactly {board_size} elements.")
                board.append(row)

    if len(board) != board_size:
        raise ValueError(f"The board should have {board_size} rows, but found {len(board)}.")

    return board_size, board

def main():

    args = parse_args()

    # parse_board(args.file_path)
    
    size = 4

    # start_board = [
    #     [5, 8, 1],
    #     [6, 0, 3],
    #     [7, 4, 2],
    # ]

    # start_board = [
    #     [5, 7, 2],
    #     [8, 6, 4],
    #     [3, 1, 0],
    # ]


    start_board = [
        [9,  5, 10, 15 ],
        [14, 12,  1,  6 ],
        [ 4,  2,  3,  8 ],
        [13,  7,  0, 11 ],
        ]

    
    final_board = create_resolved(size)


    if is_solvable(start_board):
        print("Board not solvable.")
        return
    
    start_time = time.time()
    solution = solve(args.heuristic, start=start_board, end=final_board)
    end_time = time.time()

    elapsed_time = end_time - start_time

    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)

    for board in solution:
        display_state(board)

    print(f"Solution find in {len(solution)} mouvements.")
    print(f"Solution find in {int(hours):02} hours, {int(minutes):02} minutes, {seconds:.2f} seconds.")

if __name__ == "__main__":
    main()

    