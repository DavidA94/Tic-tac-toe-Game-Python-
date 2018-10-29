__author__ = "David Antonucci"
__version__ = "1.0.0"

import re
import sys
from console_game import get_board_size, ask_for_move
from console_helper import ConsoleHelper
from enums import MoveError
from tic_tac_toe import TicTacToe

if __name__ == "__main__":
    while True:

        game = None

        if len(sys.argv) > 1 and re.match("^\d+$", sys.argv[1]) is not None:
            game = TicTacToe(int(sys.argv[1]))
        else:
            size = get_board_size()
            game = TicTacToe(size)

        while not game.is_board_full() and not game.is_winner():
            ConsoleHelper.set_print_foreground(game.get_current_player_color())
            game.print_board_to_console()

            while True:
                # Convert to 0-based
                move = ask_for_move(game.get_current_player())
                response = game.make_move((move[0] - 1, move[1] - 1))

                if response == MoveError.OUT_OF_RANGE:
                    print("The given move was outside the bounds of the board. Please try again.")
                elif response == MoveError.TAKEN:
                    print("The given move has already been played. Please try again.")
                else:
                    break

        if game.is_winner():
            game.print_board_to_console()
            print(f"Congratulations Player {game.get_winner()}! You Won!")
        else:
            ConsoleHelper.reset_all_colors()
            game.print_board_to_console(enable_colorization=False)
            print("Oh no! It was a tie!")

        ConsoleHelper.reset_all_colors()

        answer = input("Do you want to play another game (y/n)? ").lower()
        while len(answer) < 1 or (answer[0] != "y" and answer[0] != "n"):
            print("Invalid answer given")
            answer = input("Do you want to play another game (y/n)? ").lower()

        if answer[0] != "y":
            break
