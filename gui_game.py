__author__ = "David Antonucci"
__version__ = "1.0.0"

import re
import sys
from PyQt5.QtWidgets import *
from qt_gui import QtGui

if __name__ == "__main__":
    board_size = 3

    if len(sys.argv) > 1 and re.match("^\d+$", sys.argv[1]) is not None:
        board_size = int(sys.argv[1])

    app = QApplication(sys.argv)
    gui = QtGui(board_size)
    sys.exit(app.exec_())
