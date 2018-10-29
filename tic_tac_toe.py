__author__ = "David Antonucci"
__version__ = "1.0.0"

import os
from console_helper import ConsoleHelper
from typing import List, Tuple, Dict
from enums import Color, MoveError


class TicTacToe:
    NEUTRAL_PLAYER: chr = ' '

    _board_size: int
    _board: List[List[chr]]
    _current_player: int
    _last_move: Tuple[int, int]
    _number_of_moves: int
    _players: List[chr]
    _player_colors: Dict[int, Color]
    _winner: chr
    _win_edges: Tuple[Tuple[int, int], Tuple[int, int]]

    def __init__(self, board_size: int):

        self._board = []
        self._board_size = board_size
        self._current_player = 0
        self._last_move = None
        self._number_of_moves = 0
        self._players = ['X', 'O']
        self._player_colors = {0: Color.GREEN, 1: Color.YELLOW}
        self._winner = self.NEUTRAL_PLAYER
        self._win_edges = ((0, 0), (0, 0))

        for row in range(self._board_size):
            self._board.append([])
            for col in range(self._board_size):
                self._board[row].append(self.NEUTRAL_PLAYER)

    def is_board_full(self):
        return self._number_of_moves == self._board_size ** 2

    def is_winner(self):
        """
        Checks if somebody has won the game
        :return: True if there is a winner
        """
        return self._winner != self.NEUTRAL_PLAYER

    def get_board(self) -> Tuple[Tuple[chr]]:
        """
        Gets the current game board
        """
        # If we return the list, then the caller could modify the board,
        # so we want to convert it to a tuple so it's immutable
        return tuple(tuple(row) for row in self._board)

    def get_board_size(self) -> int:
        return self._board_size

    def get_current_player(self) -> chr:
        """
        Gets the player whose move is being waited for
        :return: The character that represents the player whose move is being waited for
        """
        return self._players[self._current_player]

    def get_current_player_color(self) -> Color:
        return self._player_colors[self._current_player]

    def get_winner(self) -> chr:
        """
        Gets the winner of the game, if there is one.
        :return: The winner of the game, if there is one, otherwise TickTacToe.self.NEUTRAL_PLAYER 
        """
        return self._winner

    def get_win_edges(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Gets the edges of the win, such as ((0, 0), (2, 2)) would represent a win from the top left to the bottom right
        """
        return self._win_edges

    def make_move(self, move: Tuple[int, int]) -> MoveError:
        """
        Makes the given move on the board
        :param move: The 0-based coordinates where the move is trying to be made
        :return: A MoveError that gives the status of the attempted move
        """

        # Make sure our move is going to be valid
        if self.is_winner():
            return MoveError.GAME_WON

        elif move[0] >= self._board_size or move[0] < 0 or move[1] >= self._board_size or move[1] < 0:
            return MoveError.OUT_OF_RANGE

        elif self._board[move[1]][move[0]] != self.NEUTRAL_PLAYER:
            return MoveError.TAKEN

        # If we make it to here, then it is valid to make the move
        self._board[move[1]][move[0]] = self._players[self._current_player]
        self._number_of_moves = self._number_of_moves + 1
        self._last_move = move

        self._check_for_winner()

        # Only change who the player is if we didn't get a winner,
        # otherwise the final board's color will be wrong
        if not self.is_winner():
            self._current_player = (self._current_player + 1) % len(self._players)

        return MoveError.OKAY

    def print_board_to_console(self, enable_colorization: bool=True, clear_screen: bool=True) -> None:
        """
        Prints the board to the console
        :param enable_colorization: Indicates if the board will be colored (Only works correctly with a black console)
        :param clear_screen: Indicates if the screen should be cleared before drawing the board (Windows only)
        """

        # If we're clearing the console, then do it (Windows only)
        if clear_screen:
            os.system("cls")

        if enable_colorization:
            ConsoleHelper.set_print_foreground(self.get_current_player_color())

        # Print the column numbers
        print("    ", end='')
        for i in range(self._board_size):
            print(f" {i + 1}  ", end='')

        for row_num, row in enumerate(self._board):

            # Make sure we move to the next line
            print("\n", end='')

            # Add the row number
            print(f" {row_num + 1: >2} ", end='')

            # Print the row that has the actual cell contents
            for col_num, cell in enumerate(row):

                if (enable_colorization and
                        self._last_move is not None and
                        self._last_move[1] == row_num and
                        self._last_move[0] == col_num):
                    ConsoleHelper.set_print_background(Color.WHITE)
                    print(f" {cell} ", end='')
                    ConsoleHelper.revert_print_background()
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
        print("    " * (self._board_size + 1), flush=True)

        if enable_colorization:
            ConsoleHelper.revert_print_foreground()

    def _check_for_winner(self):
        # Short circuiting!
        self._get_horizontal_winner() or self._get_vertical_winner() or self._get_diagonal_winner()

    def _get_diagonal_winner(self) -> bool:
        """
        Checks both diagonals for a winner. If one is found, self._winner will be set.
        :return: True if there is a winner
        """

        # Works basically the same as the horizontal and vertical checks. See there for comments

        backward_winner = self._board[0][-0]  # top left to bottom right
        forward_winner = self._board[0][-1]  # top right to bottom left

        # Loop through the diagonals one time, and keep track of if everything stays the same
        for diagonal in range(self._board_size):
            if backward_winner != self.NEUTRAL_PLAYER and self._board[diagonal][diagonal] != backward_winner:
                backward_winner = self.NEUTRAL_PLAYER

            # Python array shenanigans
            if forward_winner != self.NEUTRAL_PLAYER and self._board[diagonal][-diagonal - 1] != forward_winner:
                forward_winner = self.NEUTRAL_PLAYER

        # If we had a winner, then return that winner, otherwise, return the self.NEUTRAL_PLAYER
        if backward_winner != self.NEUTRAL_PLAYER:
            self._winner = backward_winner
            self._win_edges = ((0, 0), (self._board_size - 1, self._board_size - 1))
            return True

        if forward_winner != self.NEUTRAL_PLAYER:
            self._winner = forward_winner
            self._win_edges = ((self._board_size - 1, 0), (0, self._board_size - 1))
            return True

        return False

    def _get_horizontal_winner(self) -> bool:
        """
        Checks all horizontal rows for a winner. If one is found, self._winner will be set.
        :return: True if there is a winner
        """

        # Loop through all the rows
        for row_num, row in enumerate(self._board):
            # Get the entry of the first cell in the row
            winner = row[0]

            # Loop through each cell in a given row
            for cell in row:

                # If we haven't already found a blank cell this row
                # and if the current cell is not our current value,
                # then set it to be a self.NEUTRAL_PLAYER (not a winner)
                if winner != self.NEUTRAL_PLAYER and cell != winner:
                    winner = self.NEUTRAL_PLAYER
                    break

            # Set the winning player if anybody won
            if winner != self.NEUTRAL_PLAYER:
                self._winner = winner
                self._win_edges = ((0, row_num), (self._board_size - 1, row_num))
                return True

        # If we make it this far, then we did not find a winner
        return False

    def _get_vertical_winner(self) -> bool:
        """
        Checks all vertical rows for a winner. If one is found, self._winner will be set.
        :return: True if there is a winner
        """

        # Loop through all columns
        for col in range(self._board_size):
            # Get the entry of the first cell in the column
            winner = self._board[0][col]

            # Loop through all the rows
            for row in range(self._board_size):
                cell = self._board[row][col]

                # If we haven't already found a blank cell this row
                # and if the current cell is not our current value,
                # then set it to be a self.NEUTRAL_PLAYER (not a winner)
                if (winner != self.NEUTRAL_PLAYER and cell != winner) or cell == self.NEUTRAL_PLAYER:
                    winner = self.NEUTRAL_PLAYER
                    break

            # Set the winning player if anybody won
            if winner != self.NEUTRAL_PLAYER:
                self._winner = winner
                self._win_edges = ((col, 0), (col, self._board_size - 1))
                return True

        # If we make it this far, then we did not find a winner
        return False
