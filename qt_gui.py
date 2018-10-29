__author__ = "David Antonucci"
__version__ = "1.0.0"

import PyQt5.Qt as Qt
from enums import Color, MoveError
from game_cell import GameCell
from PyQt5.QtGui import QColor, QIcon, QPaintEvent
from PyQt5.QtWidgets import *
from tic_tac_toe import TicTacToe
from typing import List, Tuple, Dict


class QtGui(QWidget):
    _game_board_grid: QGridLayout
    _board_cells: List[QLabel]
    _has_game_started: bool
    _board_size_input: QSpinBox
    _first_cell: QLabel
    _player_prompt: QLabel

    _GAME_BOARD_SPACING: int = 5
    _GAME_BOARD_CELL_SIZE: int = 75
    _COLOR_TABLE: Dict[Color, QColor] = {
        Color.BLACK: Qt.QColor(0, 0, 0),
        Color.WHITE: Qt.QColor(255, 255, 255),
        Color.RED: Qt.QColor(255, 0, 0),
        Color.GREEN: Qt.QColor(0, 200, 0),
        Color.BLUE: Qt.QColor(0, 0, 255),
        Color.YELLOW: Qt.QColor(140, 140, 30),
    }

    def __init__(self, board_size: int=3):
        # noinspection PyArgumentList
        super().__init__()

        self._board_cells = []  # The game cells (needed so we can delete or update them)
        self._board_size = board_size  # The size of the board (used for easily restarting the game)
        self._board_size_input = None  # The input that holds how big the board is supposed to be
        self._first_cell = None  # The first cell in the grid (used for drawing things correctly)
        self._game = TicTacToe(board_size)  # The game engine
        self._game_board_grid = None  # The grid that holds the _board_cells (needed so new cells can be added)
        self._player_prompt = None  # The label that holds the prompt for whose turn it is, or who won

        self._has_game_started = False  # Indicates if the game has started (needed for a warning prompt)

        # Setup the UI
        self._initUI()

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Does custom line painting
        :param event: The paint event information
        """

        # Get the coordinate of the top-left corner of the top-left cell
        x = self._first_cell.pos().x()
        y = self._first_cell.pos().y()

        # Start the painter
        qp = Qt.QPainter()
        qp.begin(self)

        # Setup the original horizontal and vertical line start points
        horizontal_x_pos = x
        horizontal_y_pos = y + self._GAME_BOARD_CELL_SIZE
        vertical_x_pos = x + self._GAME_BOARD_CELL_SIZE
        vertical_y_pos = y

        # Setup some shorthands
        board_size = self._board_size
        long_size = (self._GAME_BOARD_SPACING * (board_size - 1)) + (self._GAME_BOARD_CELL_SIZE * board_size)

        # Draw each horizontal and vertical line
        for cross in range(board_size - 1):
            qp.fillRect(horizontal_x_pos, horizontal_y_pos, long_size, self._GAME_BOARD_SPACING, Qt.QColor(0, 0, 0))
            qp.fillRect(vertical_x_pos, vertical_y_pos, self._GAME_BOARD_SPACING, long_size, Qt.QColor(0, 0, 0))

            horizontal_y_pos = horizontal_y_pos + self._GAME_BOARD_CELL_SIZE + self._GAME_BOARD_SPACING
            vertical_x_pos = vertical_x_pos + self._GAME_BOARD_CELL_SIZE + self._GAME_BOARD_SPACING

        # If we have a winner, then draw the line that crosses the n-in-a-row
        if self._game.is_winner():
            cell_size = self._GAME_BOARD_CELL_SIZE  # shorthand

            (begin_x, begin_y), (end_x, end_y) = self._game.get_win_edges()

            # Figure out where we're starting, and where we're ending.
            # For the end coordinates, we need to add the final cell, if the direction we're going is not zero
            # (otherwise we'd get an angled line)
            x_start = x + (begin_x * (cell_size + self._GAME_BOARD_SPACING))
            y_start = y + (begin_y * (cell_size + self._GAME_BOARD_SPACING))
            x_end = x + (end_x * (cell_size + self._GAME_BOARD_SPACING)) + (cell_size if end_x > 0 else 0)
            y_end = y + (end_y * (cell_size + self._GAME_BOARD_SPACING)) + (cell_size if end_y > 0 else 0)

            # Shift half a cell for horizontal and vertical (so they're in the middle), and push all the way
            # to the right if we have a win from the top right to the bottom left
            if begin_x == end_x:  # Vertical win
                x_start = x_end = x_start + (self._GAME_BOARD_CELL_SIZE / 2)
            elif begin_y == end_y:  # Horizontal win
                y_start = y_end = y_start + (self._GAME_BOARD_CELL_SIZE / 2)
            elif begin_x == end_y:  # Top right to bottom left
                x_start = x_start + cell_size

            # Set the pen to be thick, and the color of the winner, then draw it
            qp.setPen(Qt.QPen(self._COLOR_TABLE[self._game.get_current_player_color()], self._GAME_BOARD_SPACING))
            qp.drawLine(x_start, y_start, x_end, y_end)

        # Finalize the drawing
        qp.end()

    def _add_game_board_cells(self) -> None:
        """
        Adds the game cells to the GUI
        """

        # We're using a giant font on this one
        board_font = Qt.QFont("sans serif", 45)
        self._first_cell = None

        # Make sure we delete any old cells
        for cell in self._board_cells:
            cell.deleteLater()

        # And then remove what we'd stored previously
        self._board_cells.clear()

        # Add all the cells, and set them up for the game play
        for row_num in range(self._board_size):
            for col_num in range(self._board_size):
                cell = GameCell(TicTacToe.NEUTRAL_PLAYER)
                cell.setFont(board_font)
                cell.setAlignment(Qt.Qt.AlignCenter)
                cell.setFixedHeight(self._GAME_BOARD_CELL_SIZE)
                cell.setFixedWidth(self._GAME_BOARD_CELL_SIZE)
                cell.set_mouse_press_event(self._cell_clicked, (row_num, col_num))
                self._board_cells.append(cell)

                # noinspection PyArgumentList
                # +1 here because we have a spacer (see initUI())
                self._game_board_grid.addWidget(cell, row_num, col_num + 1)

                if self._first_cell is None:
                    self._first_cell = cell

    def _ask_yes_no(self, question: str, question_title: str) -> bool:
        """
        Asks a yes or no question to the user
        :param question: The question to ask the user
        :param question_title: The title for the message box that is asking the question
        :return: True if the Yes button is clicked
        """

        box = QMessageBox()
        answer = box.question(self, question_title, question, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        return answer == QMessageBox.Yes

    def _cell_clicked(self, cell_coordinates: Tuple[int, int]) -> None:
        """
        Fires when a game cell is clicked
        :param cell_coordinates: The coordinates of the cell that was clicked
        :return:
        """

        # Figure out who is playing, and their color
        current_player = self._game.get_current_player()
        color = self._COLOR_TABLE[self._game.get_current_player_color()]

        # We need to reverse the coordinates so they're in (x, y), not (y, x)
        reversed_coordinates = (cell_coordinates[1], cell_coordinates[0])

        # If the move is valid, then update everything accordingly
        if self._game.make_move(reversed_coordinates) == MoveError.OKAY:
            self._has_game_started = True
            cell_index = (cell_coordinates[0] * self._game.get_board_size()) + cell_coordinates[1]
            self._board_cells[cell_index].setText(current_player)
            self._board_cells[cell_index].setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()})")

        # Update for what's going on next
        self._update_player_prompt()

        # If we finished the game
        if self._game.is_winner() or self._game.is_board_full():
            # If the move got a winner, then force the entire thing to redraw so the win-line will be fully drawn
            self.repaint()

            # Ask if they user wants to play another game
            if self._ask_yes_no("Do you want to play another game?", "Play Again?"):
                self._restart_game()

    @Qt.pyqtSlot(name="change size")
    def _change_size(self) -> None:
        """
        The event handler for when the Set Board Size button is clicked
        """

        # Get the value from the input box
        new_size = self._board_size_input.value()

        # Don't do anything if nothing has changed
        if new_size == self._game.get_board_size():
            return

        # If the game has already started, warn the user that it will be restarted
        if (self._has_game_started and
                not self._ask_yes_no("This action will start a new game. Do you wish to proceed?", "Restart Game?")):
            return

        # Save the size and restart the game
        self._board_size = new_size
        self._restart_game()

        # We need to update the cells and size, since things have changed
        self._add_game_board_cells()
        self.setFixedSize(self.sizeHint())

    # noinspection PyPep8Naming
    def _initUI(self) -> None:
        """
        Initializes the GUI elements
        """

        self.setWindowTitle("Tic-Tac-Toe")
        self.setWindowIcon(QIcon('icon.ico'))

        # The default font for most stuff
        font = Qt.QFont("sans-serif", 10)

        # We're going to use a vertical box layout (vertical stack panel), with a margin of 10 on each side
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSizeConstraint(Qt.QLayout.SetFixedSize)  # This makes the window shrink when we change the size
        self.setLayout(main_layout)

        # Setup the board info grid (make sure there are no margins)
        game_info_grid = QGridLayout()
        game_info_grid.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(game_info_grid)

        # The label that says that the board size box is for
        board_size_input = QLabel("Game Board Size: ")
        board_size_input.setFont(font)
        # noinspection PyArgumentList
        game_info_grid.addWidget(board_size_input, 0, 0)

        # The board size input box (Limit from 2 to 10, and start with a default of the board size)
        self._board_size_input = QSpinBox()
        board_size_input = self._board_size_input  # Shorthand
        board_size_input.setFont(font)
        board_size_input.setMinimum(2)
        board_size_input.setMaximum(10)
        board_size_input.setValue(self._board_size)

        # This makes the height not be stretched
        size_policy = board_size_input.sizePolicy()
        size_policy.setVerticalStretch(1)
        board_size_input.setSizePolicy(size_policy)

        # noinspection PyArgumentList
        game_info_grid.addWidget(board_size_input, 0, 1)

        # The button that needs to be clicked in order to change the size
        board_size_button = QPushButton("Set Board Size")
        # noinspection PyUnresolvedReferences
        board_size_button.clicked.connect(self._change_size)
        # noinspection PyArgumentList
        game_info_grid.addWidget(board_size_button, 0, 2)

        # The prompt for the player so they can tell what's going on
        self._player_prompt = QLabel()
        self._player_prompt.setFont(Qt.QFont("sans serif", 14, 5))
        self._player_prompt.setContentsMargins(10, 10, 0, 10)
        self._update_player_prompt()
        # noinspection PyArgumentList
        game_info_grid.addWidget(self._player_prompt, 1, 0, 1, 3)

        # Setup the game board
        self._game_board_grid = QGridLayout()
        self._game_board_grid.setSpacing(self._GAME_BOARD_SPACING)

        # This section below fixes a visual bug when the grid is only 2x2. The bug is that the
        # cells have extra spacing to spread out, which makes then not fit correctly within the
        # lines that are drawn. So, here we are adding some empty widgets that are the preferred
        # widgets to expand, when needed, therefore making there just be whitespace rather than
        # there being the visual bug. They are set at columns 0 and 11, and have a row-span of
        # two, since that is the only board size that has the issue.

        # noinspection PyArgumentList
        empty_left = QWidget()
        # noinspection PyArgumentList
        empty_right = QWidget()
        empty_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        empty_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # noinspection PyArgumentList
        self._game_board_grid.addWidget(empty_left, 0, 0, 2, 1)
        # noinspection PyArgumentList
        self._game_board_grid.addWidget(empty_left, 0, 11, 2, 1)

        self._add_game_board_cells()

        main_layout.addLayout(self._game_board_grid)

        self.show()
        self.setFixedSize(self.size())

    def _restart_game(self) -> None:
        """
        Restarts the game, and all variables associated with it
        """

        self._game = TicTacToe(self._board_size)
        self._has_game_started = False
        self._update_player_prompt()

        for cell in self._board_cells:
            cell.setText(TicTacToe.NEUTRAL_PLAYER)

    def _update_player_prompt(self) -> None:
        """
        Updates what the player prompt says, based on the state of the game
        """

        # Get the current player's color, but use black if we have a tie message to print
        color = self._COLOR_TABLE[self._game.get_current_player_color()]
        if self._game.is_board_full() and not self._game.is_winner():
            color = self._COLOR_TABLE[Color.BLACK]

        # Update the color
        self._player_prompt.setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()})")

        # Update the text
        if self._game.is_winner():
            self._player_prompt.setText(f"Player {self._game.get_winner()} won!")
        elif self._game.is_board_full():
            self._player_prompt.setText("Oh no! It was a tie!")
        else:
            self._player_prompt.setText(f"Waiting for Player {self._game.get_current_player()}")
