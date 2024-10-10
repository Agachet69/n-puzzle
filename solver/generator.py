import random

def flatten(board):
    return [tile for row in board for tile in row]

def count_inversions(board):
    flattened = flatten(board)
    flattened = [tile for tile in flattened if tile != 0] 
    inversions = 0
    for i in range(len(flattened)):
        for j in range(i + 1, len(flattened)):
            if flattened[i] > flattened[j]:
                inversions += 1
    return inversions

def find_blank_row(board):
    for row_index, row in enumerate(board):
        if 0 in row:
            return row_index

def is_solvable(board):
    inversions = count_inversions(board)
    size = len(board)
    
    if size % 2 != 0:
        return inversions % 2 == 0
    else:
        blank_row = find_blank_row(board)
        return (inversions + blank_row) % 2 != 0

def generate_puzzle(size, solvable=True):

    board = [[size * i + j for j in range(size)] for i in range(size)]
    tiles = flatten(board)
    random.shuffle(tiles)
    board = [tiles[i * size:(i + 1) * size] for i in range(size)]

    if solvable:
        while not is_solvable(board):
            random.shuffle(tiles)
            board = [tiles[i * size:(i + 1) * size] for i in range(size)]
    else:
        while is_solvable(board):
            random.shuffle(tiles)
            board = [tiles[i * size:(i + 1) * size] for i in range(size)]
    
    return board

def print_puzzle(board):
    for row in board:
        print(" ".join(f"{tile:2}" for tile in row))
    print()

def main():
    size = int(input("Enter puzzle size (e.g., 3 for 3x3): "))
    solvability_choice = input("Do you want the puzzle to be solvable? (yes/no): ").lower()
    solvable = solvability_choice == "yes"

    board = generate_puzzle(size, solvable)
    
    print("Generated Puzzle Board:")
    print_puzzle(board)
    print("This puzzle is solvable!" if is_solvable(board) else "This puzzle is unsolvable!")

if __name__ == "__main__":
    main()
