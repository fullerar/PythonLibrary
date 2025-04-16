from IPython.display import clear_output

taken_spaces = set()


def display_board(board):
    print(' ' * 3 + '|' + ' ' * 3 + '|' + ' ' * 3)
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('-' * 3 + '|' + '-' * 3 + '|' + '-' * 3)
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-' * 3 + '|' + '-' * 3 + '|' + '-' * 3)
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print(' ' * 3 + '|' + ' ' * 3 + '|' + ' ' * 3)


# test_board = ['#', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
# display_board(test_board)

def player_input():
    global taken_spaces
    marker_choice = False
    acceptable_markers = ['X', 'O']
    while not marker_choice:
        marker = input("Please enter X or O: ")
        if marker.isalpha() and marker in acceptable_markers:
            marker_choice = True
        else:
            print("Invalid entry...")

    space_choice = False
    spaces = set(range(1, 10))
    acceptable_spaces = spaces.difference(taken_spaces)
    while not space_choice:
        space = input("Please pick a space (1-9): ")
        if space.isnumeric() and space not in taken_spaces:
            space_choice = True
            taken_spaces.add(int(space))


    print(f"acceptable: {acceptable_spaces}")
    print(f"taken: {taken_spaces}")

    return marker


player_input()
