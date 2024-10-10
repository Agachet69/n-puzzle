def create_resolved(puzzle):
    size = len(puzzle)

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

table = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0],
        [7, 8, 0],
        [7, 8, 0],
        [7, 8, 0]
    ]

create_resolved(table)