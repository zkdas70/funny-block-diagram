import block, draw_block_diagram
from PIL.ImageQt import ImageQt

import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QFileDialog
from PyQt6.QtGui import QPixmap


class BlockDiagram(QWidget):
    def __init__(self, image):
        super().__init__()
        uic.loadUi(r'gui/block_diagram.ui', self)

        self.show_block_diagram(image)

    def show_block_diagram(self, image):
        pixmap = QPixmap.fromImage(image)

        self.BlockDiagramBase.setMinimumSize(pixmap.size())

        self.BlockDiagramBase.setPixmap(pixmap)



class CastomTabWidget(QWidget):
    def __init__(self, tabs):
        super().__init__()
        uic.loadUi(r'gui/tab_widget.ui', self)

        for item in tabs:
            self.tabWidget.addTab(BlockDiagram(item[0]), f' {item[1]} ')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'gui/gui.ui', self)  # Загружаем дизайн

        # self.convert.clicked.connect(self.show_block_diagram)
        self.show_block_diagram()

    def show_block_diagram(self):
        # fname = QFileDialog.getOpenFileName(
        #     self, 'Выбрать файл с кодом', '',
        #     'python (*.py);;Все файлы (*)')[0]

        fname = r'F:\programming projects\python projects\tusur_python_lesons\LAB 4\53.py'
        blocks_images = []

        with open(fname) as f:
            file_code = f.readlines()

        decodet_file_code = block.Block().decoder(file_code)

        image = draw_block_diagram.PaintBlock().type_defld_code(decodet_file_code[0])

        if len(decodet_file_code[1]) == 0:
            image = BlockDiagram((ImageQt(image)))
            image.show()
            self.gridLayout.addWidget(image)
            return

        blocks_images.append((ImageQt(image), 'основной код программы'))

        for i in range(len(decodet_file_code[1])):
            image = draw_block_diagram.draw_block_diagram([decodet_file_code[1][i]])

            blocks_images.append((ImageQt(image), decodet_file_code[1][i]['item']))
        castom_tab = CastomTabWidget(blocks_images)
        self.gridLayout.addWidget(castom_tab)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec()

