__author__ = "David Antonucci"
__version__ = "1.0.0"

import PyQt5.Qt as Qt
from typing import Callable, Tuple
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel, QWidget


class GameCell(QLabel):
    _coordinates: Tuple[int, int]
    _mousePressEventMethod: Callable[[Tuple[int, int]], None]

    def __init__(self, parent):
        QLabel.__init__(self, parent)

        self._coordinates = None
        self._mousePressEventMethod = None

    def set_mouse_press_event(self, method, coordinates: Tuple[int, int]):
        self._mousePressEventMethod = method
        self._coordinates = coordinates

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.Qt.LeftButton:
            event.accept()
            self._mousePressEventMethod(self._coordinates)
        else:
            return QWidget.mousePressEvent(self, event)
