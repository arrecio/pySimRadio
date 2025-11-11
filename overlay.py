import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QLabel, QAction
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QColor, QPixmap, QIcon
from pathlib import Path
import random

BAR_WIDTH = 8
OVERLAY_WIDTH = 140
OVERLAY_HEIGHT = 100
WAITING_COLOR = QColor(255,0,0)
LISTENING_COLOR = QColor(0,255,0)

class Icon(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        hotkeyAction = QAction("Set Hotkey", self)
        hotkeyAction.triggered.connect(self.setHotkey)
        self.addAction(hotkeyAction)
        self.__color = WAITING_COLOR
        self.__listening = False
        self.__sizes = [10,20,35,25,45,90]
        self.__timer = QTimer()
        self.__timer.setInterval(64)
        self.__timer.timeout.connect(self.update)
        self.__timer.start()

    def setHotkey(self, event):
        print("To implement")

    def update(self):
        if self.__listening:
            for i in range(0, len(self.__sizes)):
                self.__sizes[i] = random.randint(0,90)
        else:
            self.__sizes = [10,20,35,25,45,90]
        self.repaint()

    def onListening(self):
        self.__color = LISTENING_COLOR
        self.__listening = True

    def onWaiting(self):
        self.__color = WAITING_COLOR
        self.__listening = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        sizes = self.__sizes
        for i in range(0, len(sizes)):
            painter.fillRect(QtCore.QRect(i*(BAR_WIDTH+2), int(50-sizes[i]/2), BAR_WIDTH, sizes[i]), QBrush(self.__color))
        for i in range(0, len(sizes)-1):
            painter.fillRect(QtCore.QRect((i+len(sizes))*(BAR_WIDTH+2), int(50-sizes[len(sizes)-2-i]/2), BAR_WIDTH, sizes[len(sizes)-2-i]), QBrush(self.__color))

#embed window
class Window(QMainWindow):

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPos() - self._dragPosition)
            event.accept()

class Overlay():
    def __init__(self):
        super().__init__()
        self.__window = Window()
        self.__window.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.__window.setGeometry(QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,
            Qt.AlignmentFlag.AlignCenter,
            QSize(OVERLAY_WIDTH, OVERLAY_HEIGHT),
            QApplication.instance().primaryScreen().availableGeometry(),
        ))
        self.__window.setStyleSheet("background:transparent;")
        self.__window.setStyleSheet("QLineEdit QMenu::item {color: rgb(0, 0, 255);}")
        self.__window.setAttribute(Qt.WA_TranslucentBackground)

        self.__icon = Icon(self.__window)
        self.__icon.resize(OVERLAY_WIDTH, OVERLAY_HEIGHT)

        self.__window.show()

    def listeningMode(self):
        self.__icon.onListening()

    def waitingMode(self):
        self.__icon.onWaiting()
