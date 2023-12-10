import block, draw_block_diagram, get_imgs
from PIL.ImageQt import ImageQt

import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QFileDialog
from PyQt6.QtGui import QPixmap, QImage


class BlockDiagram(QWidget):
    def __init__(self, buffer):  # buffer - обьект BytesIO с картинкой
        super().__init__()
        uic.loadUi(r'gui/block_diagram.ui', self)

        self.show_block_diagram(buffer)

    def show_block_diagram(self, buffer):
        image_bytes = buffer.getvalue()

        qimage = QImage.fromData(image_bytes)

        pixmap = QPixmap.fromImage(qimage)

        self.BlockDiagramBase.setMinimumSize(pixmap.size())

        self.BlockDiagramBase.setPixmap(pixmap)


class CastomTabWidget(QWidget):
    def __init__(self, tabs):
        super().__init__()
        uic.loadUi(r'gui/tab_widget.ui', self)

        for img_bytes, name in tabs:
            self.tabWidget.addTab(BlockDiagram(img_bytes), f' {name} ')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'gui/gui.ui', self)  # Загружаем дизайн

        self.convert.clicked.connect(self.show_block_diagram)
        # self.show_block_diagram()

    def show_block_diagram(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Выберите файл", r"F:\programming projects\python projects\tusur_python_lesons", 'python (*.py);;Все файлы (*)')
        if not fname:
            return

        # fname = r'F:\programming projects\python projects\tusur_python_lesons\LAB 4\53.py'

        block_diagrams = get_imgs.get_imgs(fname)

        if len(block_diagrams) == 1:
            block_diagram = BlockDiagram(block_diagrams[0][0])

            self.space_for_block_diagram.addWidget(block_diagram)
            return

        castom_tab = CastomTabWidget(block_diagrams)
        self.space_for_block_diagram.addWidget(castom_tab)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec()
