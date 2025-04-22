from IPython.display import clear_output
import random

taken_spaces = set()
board = ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


def display_board(board):
    print(' ' * 3 + '|' + ' ' * 3 + '|' + ' ' * 3)
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('-' * 3 + '|' + '-' * 3 + '|' + '-' * 3)
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-' * 3 + '|' + '-' * 3 + '|' + '-' * 3)
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print(' ' * 3 + '|' + ' ' * 3 + '|' + ' ' * 3)


def place_marker(board, marker, position):
    board[int(position)] = marker
    taken_spaces.add(int(position))

    display_board(board)


def player_input():
    global taken_spaces, board
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
        if space.isnumeric():
            if space not in taken_spaces:
                space_choice = True
                #taken_spaces.add(int(space))
                place_marker(board, marker, space)
            else:
                print("That spot is taken...")
        else:
            print("Invalid entry...")


def win_check(board, mark):
    winning_sets = [{1, 2, 3}, {1, 5, 9}, {1, 4, 7},
                    {2, 5, 8},
                    {3, 5, 7}, {3, 6, 9},
                    {4, 5, 6}]

    trio_counter = 0
    for trio in winning_sets:
        for position in trio:
            if board[position] == mark:
                trio_counter += 1
        if trio_counter == 3:
            return True
        else:
            trio_counter = 0

    return False


def choose_first():
    n = random.randint(1, 2)
    if n is 1:
        return 1
    else:
        return 2


def tie_check():
    full_set = set(range(1, 10))
    if taken_spaces == full_set:
        return True


def replay():
    acceptable_responses = ["Y", "N"]
    waiting = True
    while waiting:
        play_again_bool = input("Do you wish to play again? (Y/N) ")
        if play_again_bool.isalpha() and play_again_bool in acceptable_responses:
            if play_again_bool is "Y":
                return True
            else:
                return False
        else:
            print("Invalid entry...")


print("Welcome to Tic Tac Toe!")
playing = True
while playing:
    first_player = choose_first()
    print(f"Player {first_player} will go first!")
    print(f"Here is the board. Player {first_player}, you may begin.")
    display_board(board)

    game_won = False
    tie = False
    while not game_won and not tie:
        player_input()

        if win_check(board, "X"):
            print("X's win!")
            game_won = True
        if win_check(board, "O"):
            print("O's win!")
            game_won = True
        if tie_check():
            print("Tie game!")
            tie = True

    if game_won or tie_check():
        playing = replay()
        if playing:
            taken_spaces = set()
            board = ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        else:
            print("Good game!")

