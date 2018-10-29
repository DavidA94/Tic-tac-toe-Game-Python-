__author__ = "David Antonucci"
__version__ = "1.0.0"

import os
import re
import sys
from colorama import Back, Fore, Style
from typing import List, Tuple

NEUTRAL_PLAYER = ' '


def ask_for_move(player: chr) -> Tuple[int, int]:
    """
    Prompts the player for a move
    :param player: The player who is being asked to make their move
    :return: The 1-based coordinates given by the user to place their move in
    """

    while True:
        move = input(f"Player {player} - Enter the coordinate to play your move: ")
        match = re.match("^ *(\d+) *,? *(\d+) *$", move)

        if match is None:
            print("\nInvalid coordinate given. Please enter the coordinate in the format x, y.")
        else:
            return int(match[1]), int(match[2])


def get_board_size() -> int:
    """
    Gets the board size the user wants to play
    :return: The size of the board, which will be without the bounds of [2, 10]
    """

    while True:
        size = input("How big would you like your board to be ([2, 10])? ").strip()

        if re.match("^\d+$", size) is None:
            print(f"\nThe entered value {size} is not a number. Please enter a number")
        else:
            int_size = int(size)
            if int_size < 2 or int_size > 10:
                print(f"\nThe given value is outside the bounds. Must be between 2 and 10 (inclusive)")
            else:
                return int_size


def get_diagonal_winner(board: List[List[str]]) -> chr:
    """
    Checks both diagonals for a winner
    :param board: The board to process
    :return: The winner or NEUTRAL_PLAYER if nobody has won
    """

    # Works basically the same as the horizontal and vertical checks. See there for comments

    backward_winner = board[0][-0]  # top left to bottom right
    forward_winner = board[0][-1]  # top right to bottom left

    # Loop through the diagonals one time, and keep track of if everything stays the same
    for diagonal in range(len(board)):
        if backward_winner != NEUTRAL_PLAYER and board[diagonal][diagonal] != backward_winner:
            backward_winner = NEUTRAL_PLAYER

        # Python array shenanigans
        if forward_winner != NEUTRAL_PLAYER and board[diagonal][-diagonal - 1] != forward_winner:
            forward_winner = NEUTRAL_PLAYER

    # If we had a winner, then return that winner, otherwise, return the NEUTRAL_PLAYER
    if backward_winner != NEUTRAL_PLAYER:
        return backward_winner

    if forward_winner != NEUTRAL_PLAYER:
        return forward_winner

    return NEUTRAL_PLAYER


def get_horizontal_winner(board: List[List[str]]) -> chr:
    """
    Checks all horizontal rows for a winner
    :param board: The board to process
    :return: The winner or NEUTRAL_PLAYER if nobody has won
    """

    # Loop through all the rows
    for row in board:
        # Get the entry of the first cell in the row
        winner = row[0]

        # Loop through each cell in a given row
        for cell in row:

            # If we haven't already found a blank cell this row
            # and if the current cell is not our current value,
            # then set it to be a NEUTRAL_PLAYER (not a winner)
            if winner != NEUTRAL_PLAYER and cell != winner:
                winner = NEUTRAL_PLAYER
                break

        # Return the player if they won
        if winner != NEUTRAL_PLAYER:
            return winner

    # If we make it this far, then we did not find a winner
    return NEUTRAL_PLAYER


def get_vertical_winner(board: List[List[str]]) -> chr:
    """
    Checks all vertical rows for a winner
    :param board: The board to process
    :return: The winner or NEUTRAL_PLAYER if nobody has won
    """

    # Loop through all columns
    for col in range(len(board)):
        # Get the entry of the first cell in the column
        winner = board[0][col]

        # Loop through all the rows
        for row in range(len(board)):
            cell = board[row][col]

            # If we haven't already found a blank cell this row
            # and if the current cell is not our current value,
            # then set it to be a NEUTRAL_PLAYER (not a winner)
            if winner != NEUTRAL_PLAYER and cell != winner:
                winner = NEUTRAL_PLAYER
                break

        # Return the player if they won
        if winner != NEUTRAL_PLAYER:
            return winner

    # If we make it this far, then we did not find a winner
    return NEUTRAL_PLAYER


def get_winner(board: List[List[str]]) -> chr:
    """
    Looks for a winner in the game
    :param board: The board to process
    :return: The winner or NEUTRAL_PLAYER if nobody has won
    """

    winners = [get_horizontal_winner(board),
               get_vertical_winner(board),
               get_diagonal_winner(board)]

    return next((winner for winner in winners if winner != NEUTRAL_PLAYER), NEUTRAL_PLAYER)


def play_game(board_size: int) -> None:
    """
    Plays the tic-tac-toe game
    :param board_size: The size of the board, or zero if it should be asked
    """

    # Set the board size based on if we got a valid size or not passed in
    board_size = board_size if board_size > 1 else get_board_size()

    board = []  # The board array
    players = ['X', 'O']  # What players we have
    current_player = -1  # The player who is currently playing (start at -1 because there is a +1 later on)
    number_of_moves = 0  # how many moves have happened
    has_winner = False  # indicates if we have found a winner
    last_move = None  # The last move that was played

    # Create the board
    for row in range(board_size):
        board.append([])
        for col in range(board_size):
            board[row].append(NEUTRAL_PLAYER)

    # While we haven't had too many moves
    while number_of_moves < board_size ** 2:
        current_player = (current_player + 1) % len(players)

        # Set what color we're printing
        if current_player == 0:
            set_print_color(Fore.GREEN)
        else:
            set_print_color(Fore.YELLOW)

        print_board(board, last_move)

        while True:
            move = ask_for_move(players[current_player])
            if validate_move(board, move):
                board[move[1] - 1][move[0] - 1] = players[current_player]
                number_of_moves = number_of_moves + 1
                last_move = move
                break

        winner = get_winner(board)
        if winner != NEUTRAL_PLAYER:
            has_winner = True
            print_board(board)
            print(f"Congratulations Player {winner}! You Won!")
            break

    # If we print anything pas this point, we don't want it colored for the player
    reset_print_color()

    # It's possible for the last move to win, so make sure we account for that
    if not has_winner and number_of_moves == board_size ** 2:
        print("Oh no! It was a tie!")


def print_board(board: List[List[str]], last_move: Tuple[int, int]=None) -> None:
    """
    Prints the Tic-tac-toe board
    :param board: The board to print
    :param last_move: The last move that was made, so that it can be highlighted
    """

    # Clear anything that's currently on the console
    # This only works for Windows
    os.system("cls")

    # Print the column numbers
    print("    ", end='')
    for i in range(len(board)):
        print(f" {i + 1}  ", end='')

    row_num = 0

    for row in board:
        # Increase the row number for printing
        row_num = row_num + 1

        # Make sure we move to the next line
        print("\n", end='')

        # Add the row number
        print(f" {row_num: >2} ", end='')

        col_num = 0

        # Print the row that has the actual cell contents
        for cell in row:
            col_num = col_num + 1

            if(last_move is not None and
                    last_move[1] == row_num and
                    last_move[0] == col_num):
                set_print_background(Back.WHITE)
                print(f" {cell} ", end='')
                set_print_background(Back.BLACK)
                print("|", end='')
            else:
                print(f" {cell} |", end='')

        # The line below the cells
        print("\b \n    ", end='')
        for i in range(len(row)):
            print("---+", end='')

        print("\b ", end='')

    # Don't you wish there was a comment explaining how this worked? :)
    print("\r", flush=True, end='')
    print("    " * (len(board) + 1), flush=True)


def set_print_background(background: str) -> None:
    """
    Sets the color and background that print() uses
    :param background: The foreground (text) color
    """
    print(background, end='')


def set_print_color(foreground: str) -> None:
    """
    Sets the color and background that print() uses
    :param foreground: The foreground (text) color
    """
    print(foreground, end='')


def reset_print_color() -> None:
    """
    Resets the color that print uses
    """
    print(Style.RESET_ALL)


def validate_move(board: List[List[str]], move: Tuple[int, int]) -> bool:
    """
    Validates the given move for the given board
    :param board: The board to check the move against
    :param move: The 1-based coordinates where the move is trying to be made
    :return: True if the move is valid, False if the move is invalid
    """

    if (move[0] > len(board) or move[0] < 1 or
            move[1] > len(board or move[1] < 1)):
        print("The given move was outside the bounds of the board. Please try again.")
        return False

    if board[move[1] - 1][move[0] - 1] != NEUTRAL_PLAYER:
        print("The given move has already been played. Please try again.")
        return False

    return True


if __name__ == "__main__":
    while True:
        if len(sys.argv) > 1 and re.match("^\d+$", sys.argv[1]) is not None:
            play_game(int(sys.argv[1]))
        else:
            play_game(0)

        answer = input("Do you want to play another game (y/n)? ").lower()
        while len(answer) < 1 or (answer[0] != "y" and answer[0] != "n"):
            print("Invalid answer given")
            answer = input("Do you want to play another game (y/n)? ").lower()

        if answer[0] != "y":
            break
