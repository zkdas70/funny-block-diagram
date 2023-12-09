import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)  # Загружаем дизайн
        self.show_block_diagram()

    def show_block_diagram(self):
        pixmap = QPixmap(r'sum(s).png')
        self.block_diagram.setMinimumSize(pixmap.size())
        self.block_diagram.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    app.exec()
