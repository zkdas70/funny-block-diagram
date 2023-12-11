import get_imgs

import sys

from PyQt6 import uic, QtGui  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
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

        self.block_diagrams = None
        self.castom_tab = None

        self.convert.clicked.connect(self.show_block_diagram)
        self.copy.clicked.connect(self.copy_image)
        self.save.clicked.connect(self.save_image)
        # self.show_block_diagram()

    def copy_image(self):
        if self.block_diagrams:
            image_imdex = 0
            if self.castom_tab:
                image_imdex = self.castom_tab.tabWidget.currentIndex()
            qimage = QImage.fromData(self.block_diagrams[image_imdex][0].getvalue())
            clipboard = QApplication.clipboard()
            clipboard.setImage(qimage)

    def save_image(self):
        if self.block_diagrams:
            image_imdex = 0
            if self.castom_tab:
                image_imdex = self.castom_tab.tabWidget.currentIndex()

            fname, _ = QFileDialog.getSaveFileName(self, "Save F:xile",
                                                   "/home/jana/untitled.png",
                                                   "Images (*.png *.xpm *.jpg)")

            if not fname:
                return

            with open(fname, 'wb') as f:
                f.write(self.block_diagrams[image_imdex][0].getvalue())

    def show_block_diagram(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Выберите файл",
                                               r"F:\programming projects\python projects\tusur_python_lesons",
                                               'python (*.py);;Все файлы (*)')

        # fname = r'F:\programming projects\python projects\tusur_python_lesons\LAB 4\53.py'
        if not fname:
            return

        while self.space_for_block_diagram.count():
            item = self.space_for_block_diagram.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                del item

        self.block_diagrams = get_imgs.get_imgs(fname)

        self.castom_tab = None

        if len(self.block_diagrams) == 1:
            block_diagram = BlockDiagram(self.block_diagrams[0][0])

            self.space_for_block_diagram.addWidget(block_diagram)
            return

        self.castom_tab = CastomTabWidget(self.block_diagrams)
        self.space_for_block_diagram.addWidget(self.castom_tab)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('gui/icom.png'))

    ex = MainWindow()
    ex.setWindowIcon(QtGui.QIcon('gui/icom.png'))
    ex.show()
    app.exec()
