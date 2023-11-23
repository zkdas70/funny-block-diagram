import sys
import sqlite3
import os

import json

from sys import platform

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPixmap, QImage, QFont
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog

from ui import Ui_MainWindow

DRAW_TEXT = 2  # константы для скорости и мегньшего обьема конфиг файла
NAME = 8
CITI = 16
EDUCATIONAL_INSTITUTION = 32
PLASE = 64
TEXT = 128
DRAW_IMG = 4


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.username = '%Username%'
        if platform == 'win32':
            self.username = os.environ['Username']
        self.image = QImage(4160, 3120, QImage.Format_RGB32)  # дикое разрешение для высокого качества раб. области
        self.mouse_pos = 4161, 3121  # за экраном
        self.is_paint = False
        self.is_nev_background = True  # | проверка надоли загрузить фон с диска
        self.background_img = None  # |    для оптимизации здесь храниться фон
        self.is_preview = False  # |       проверка на рижим превью
        self.preview_information = None, None
        self.BTNName.clicked.connect(self.preview_name)  # старт превью
        self.BTNNameSettings.clicked.connect(self.name_settings)
        self.name_font_size = 50
        self.before_name = ''
        self.after_name = ''
        self.BTNCiti.clicked.connect(self.preview_citi)  # старт превью
        self.BTNCitiSettings.clicked.connect(self.citi_settings)
        self.citi_font_size = 50
        self.before_citi = ''
        self.after_citi = ''
        self.BTNEducationalInstitution.clicked.connect(self.preview_educational_institution)  # старт превью
        self.BTNEducationalInstitutionSettings.clicked.connect(self.educational_institution_settings)
        self.educational_institution_font_size = 50
        self.before_educational_institution = ''
        self.after_educational_institution = ''
        self.BTNPlase.clicked.connect(self.preview_plase)  # старт превью
        self.BTNPlaseSettings.clicked.connect(self.plase_settings)
        self.plase_font_size = 50
        self.before_plase = 'за место'
        self.after_plase = ''
        self.BTNText.clicked.connect(self.preview_text)  # старт превью
        self.BTNTextSettings.clicked.connect(self.text_settings)
        self.text_font_size = 50
        self.BTNInsertBackground.clicked.connect(self.insert_background)
        self.config_cart = ()  # картеж из картежей со кординатами всех обектов # при запуске
        self.ctrl_z = (self.config_cart,)
        self.names_cart = ('Ф.И.О', 'Город', ' Уч. Завидение', 'X',)  # NAME, CITI, EDUCATIONAL_INSTITUTION, PLASE
        self.draw()
        self.createDiplomasSQL.triggered.connect(self.saver_scl)
        self.createDiplomasCSV.triggered.connect(self.saver_csv)
        self.configSave.triggered.connect(self.config_save)
        self.configUpload.triggered.connect(self.config_upload)
        self.SQLUpdate.triggered.connect(self.sql_update)
        self.SQLCreate.triggered.connect(self.sql_create)

    def config_master(self, type, *additional_information):  # additional_information список всех остальных данных
        if type == DRAW_TEXT:
            if additional_information[0] == TEXT:
                self.config_cart = (*self.config_cart, (type, additional_information[0], self.mouse_pos[0],
                                                        self.mouse_pos[1], additional_information[3],
                                                        additional_information[4]))
            elif additional_information[0] in (NAME, CITI, EDUCATIONAL_INSTITUTION, PLASE):
                self.config_cart = (*self.config_cart, (type, additional_information[0], self.mouse_pos[0],
                                                        self.mouse_pos[1], additional_information[3],
                                                        str(additional_information[4])))
            self.ctrl_z = (*self.ctrl_z, self.config_cart)
        elif type == DRAW_IMG:
            if len(self.config_cart) > 0 and self.config_cart[0][0] == DRAW_IMG:
                self.config_cart = ((type, additional_information[0]), *self.config_cart[1:])
                self.is_nev_background = True
            else:
                self.config_cart = ((type, additional_information[0]), *self.config_cart)
            self.ctrl_z = (*self.ctrl_z, self.config_cart)
        if len(self.ctrl_z) > 20:
            self.ctrl_z = self.ctrl_z[-20:]
        self.is_preview = False
        self.draw()
        self.repaint()
        self.mouse_pos = 4161, 3121  # за экраном

    def config_reader(self, qp):
        for config_object in self.config_cart:
            if config_object[0] == DRAW_TEXT:
                if config_object[1] == NAME and self.names_cart[0] not in (None, ''):
                    self.draw_text(qp, config_object[2], config_object[3], config_object[4],
                                   config_object[5].replace('{{V}}', self.names_cart[0]))
                elif config_object[1] == CITI and self.names_cart[1] not in (None, ''):
                    self.draw_text(qp, config_object[2], config_object[3], config_object[4],
                                   config_object[5].replace('{{V}}', self.names_cart[1]))
                elif config_object[1] == EDUCATIONAL_INSTITUTION and self.names_cart[2] not in (None, ''):
                    self.draw_text(qp, config_object[2], config_object[3], config_object[4],
                                   config_object[5].replace('{{V}}', self.names_cart[2]))
                elif config_object[1] == PLASE and self.names_cart[3] not in (None, ''):
                    self.draw_text(qp, config_object[2], config_object[3], config_object[4],
                                   config_object[5].replace('{{V}}', self.names_cart[3]))
                elif config_object[1] == TEXT:
                    self.draw_text(qp, config_object[2], config_object[3], config_object[4], config_object[5])
            elif config_object[0] == DRAW_IMG:
                self.draw_background(qp, config_object[1])
            else:
                pass

    def mouseMoveEvent(self, a0):
        self.repaint()
        height = self.height()  # 600
        width = self.width()  # 800
        if self.is_preview:
            self.mouse_pos = int(a0.x() / width * 4160), int(a0.y() / height * 3120)
            self.draw()
            self.repaint()

    def mouseDoubleClickEvent(self, a0):
        if self.is_preview and a0.button() == Qt.LeftButton:
            font_size = 50
            if self.preview_information[1] == NAME:
                font_size = self.name_font_size
            elif self.preview_information[1] == CITI:
                font_size = self.citi_font_size
            elif self.preview_information[1] == EDUCATIONAL_INSTITUTION:
                font_size = self.educational_institution_font_size
            elif self.preview_information[1] == PLASE:
                font_size = self.plase_font_size
            elif self.preview_information[1] == TEXT:
                font_size = self.text_font_size
            self.config_master(DRAW_TEXT, self.preview_information[1], self.mouse_pos[0], self.mouse_pos[1],
                               font_size, self.preview_information[0])

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key_Escape:
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121
        if a0.modifiers() == Qt.ControlModifier:
            if a0.key() == Qt.Key_Z and len(self.ctrl_z) >= 2:
                self.config_cart = self.ctrl_z[-2]
                self.ctrl_z = self.ctrl_z[:-1]
                self.is_preview = False
                if len(self.config_cart) > 0 and self.config_cart[0][0] != DRAW_IMG or len(self.config_cart) == 0:
                    self.is_nev_background = True
                self.draw()
                self.repaint()
                self.mouse_pos = 4161, 3121

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def draw(self):
        painter = QPainter(self.image)
        painter.begin(self)
        self.draw_canvas(painter)
        self.config_reader(painter)
        if self.is_preview:
            font_size = 50
            number_value = -2
            if self.preview_information[1] == NAME:
                font_size = self.name_font_size
                number_value = 0
            elif self.preview_information[1] == CITI:
                font_size = self.citi_font_size
                number_value = 1
            elif self.preview_information[1] == EDUCATIONAL_INSTITUTION:
                font_size = self.educational_institution_font_size
                number_value = 2
            elif self.preview_information[1] == PLASE:
                font_size = self.plase_font_size
                number_value = 3
            elif self.preview_information[1] == TEXT:
                font_size = self.text_font_size
                number_value = -1
            if number_value == -1:
                self.draw_text(painter, self.mouse_pos[0], self.mouse_pos[1], font_size, self.preview_information[0])
            elif 0 <= number_value <= 3:
                self.draw_text(painter, self.mouse_pos[0], self.mouse_pos[1], font_size,
                               str(self.preview_information[0]).replace('{{V}}', self.names_cart[number_value]))
            else:
                self.draw_text(painter, self.mouse_pos[0], self.mouse_pos[1], 50, 'ERROR')
            self.hint(painter)
        self.update()
        self.repaint()
        painter.end()

    def hint(self, qp):
        self.draw_text(qp, 3140, 1990, 50, 'Зажмите ЛКМ и перетащите')
        self.draw_text(qp, 3140, 2075, 50, 'текст.')
        self.draw_text(qp, 3140, 2245, 50, 'Чтобы сохранить позицию')
        self.draw_text(qp, 3140, 2330, 50, 'текста двойной клик по ЛКМ.')

    def draw_canvas(self, qp):  # создание рамки вокруг холста (вынесенно для удобства)
        qp.setBrush(QColor(Qt.white))
        qp.drawRect(0, 0, 4160, 3120)
        qp.setPen(Qt.gray)
        qp.setBrush(QColor(Qt.gray))
        qp.drawRect(792, 112, 2124, 2994)
        qp.setBrush(QColor(Qt.white))
        qp.drawRect(799, 119, 2102, 2972)

    def insert_background(self):
        self.is_preview = False
        self.draw()
        self.repaint()
        self.mouse_pos = 4161, 3121  # за экраном
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                            fr'C:\Users\{self.username}\Pictures',
                                            '(*.png *.xpm *.jpg *.bmp *.jpeg *.pbm)')[0]
        if fname != '':
            self.config_master(DRAW_IMG, fname)

    def draw_background(self, qp, nane):
        if self.is_nev_background:
            qpix = QPixmap()
            qpix.load(nane)
            img = qpix.toImage()
            img = img.scaled(2101, 2971)
            self.is_nev_background = False
            self.background_img = img
        img = self.background_img
        qp.drawImage(800, 120, img)

    def draw_text(self, qp, x, y, h, text):
        qp.setPen(QColor(Qt.black))
        qp.setFont(QFont('Calibri', h))
        qp.drawText(x, y, text)

    def preview_name(self):
        test = f'{self.before_name} {{{{V}}}} {self.after_name}'
        self.preview(test, NAME)

    def name_settings(self):
        setting, ok_pressed = QInputDialog.getItem(
            self, 'Выберите функцию', 'Настроить:',
            ('размер текста', 'текст до {Ф.И.О.}', 'текст после {Ф.И.О.}'), 0, False)
        if setting == 'размер текста' and ok_pressed:
            font_size, ok_pressed = QInputDialog.getInt(
                self, 'размер текста', 'выбирите размер текста.',
                self.name_font_size, 20, 500, 2)
            self.name_font_size = font_size
        elif setting == 'текст до {Ф.И.О.}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст до {{Ф.И.О.}}\n'
                                                    f'({self.before_name})')
            self.before_name = text.strip()
        elif setting == 'текст после {Ф.И.О.}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст после {{Ф.И.О.}}\n'
                                                    f'({self.after_name})')
            self.after_name = text.strip()
        if not ok_pressed:
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121  # за экраном

    def preview_citi(self):
        test = f'{self.before_citi} {{{{V}}}} {self.after_citi}'
        self.preview(test, CITI)

    def citi_settings(self):
        setting, ok_pressed = QInputDialog.getItem(
            self, 'Выберите функцию', 'Настроить:',
            ('размер текста', 'текст до {Город}', '{Город} текст после'), 0, False)
        if not ok_pressed:
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121  # за экраном
        if setting == 'размер текста' and ok_pressed:
            font_size, ok_pressed = QInputDialog.getInt(
                self, 'размер текста', 'выбирите размер текста.',
                self.citi_font_size, 20, 500, 2)
            self.citi_font_size = font_size
        elif setting == 'текст до {Город}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст до {{Город}}\n'
                                                    f'({self.before_citi})')
            self.before_citi = text.strip()
        elif setting == 'текст после {Город}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст после {{Город}}\n'
                                                    f'({self.after_citi})')
            self.after_citi = text.strip()

    def preview_educational_institution(self):
        test = f'{self.before_educational_institution} {{{{V}}}} {self.after_educational_institution}'
        self.preview(test, EDUCATIONAL_INSTITUTION)

    def educational_institution_settings(self):
        setting, ok_pressed = QInputDialog.getItem(
            self, 'Выберите функцию', 'Настроить:',
            ('размер текста', 'текст до {Уч. Завидение}', '{Уч. Завидение} текст после'), 0, False)
        if setting == 'размер текста' and ok_pressed:
            font_size, ok_pressed = QInputDialog.getInt(
                self, 'размер текста', 'выбирите размер текста.',
                self.educational_institution_font_size, 20, 500, 2)
            self.educational_institution_font_size = font_size
        elif setting == 'текст до {Уч. Завидение}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст до {{Уч. Завидение}}\n'
                                                    f'({self.before_educational_institution})\n')
            self.before_educational_institution = text.strip()
        elif setting == 'текст после {Уч. Завидение}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст после {{Уч. Завидение}}\n'
                                                    f'({self.after_educational_institution})')
            self.after_educational_institution = text.strip()
        if not ok_pressed:
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121  # за экраном

    def preview_plase(self):
        test = f'{self.before_plase} {{{{V}}}} {self.after_plase}'
        self.preview(test, PLASE)

    def plase_settings(self):
        setting, ok_pressed = QInputDialog.getItem(
            self, 'Выберите функцию', 'Настроить:',
            ('размер текста', 'текст до {место X}', '{место X} текст после'), 0, False)
        if setting == 'размер текста' and ok_pressed:
            font_size, ok_pressed = QInputDialog.getInt(
                self, 'размер текста', 'выбирите размер текста.',
                self.plase_font_size, 20, 500, 2)
            self.plase_font_size = font_size
        elif setting == 'текст до {место X}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст до {{X}}'
                                                    f'\n({self.before_plase})')
            self.before_plase = text.strip()
        elif setting == 'текст после {место X}' and ok_pressed:
            text, ok_pressed = QInputDialog.getText(self, 'Введите текст',
                                                    f'Введите текст после {{X}}'
                                                    f'\n({self.after_plase})')
            self.after_plase = text.strip()
        if not ok_pressed:
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121  # за экраном

    def preview_text(self):
        text, ok_pressed = QInputDialog.getText(self, 'Введите текст', 'Введите текст')
        if ok_pressed:
            self.preview(text.strip(), TEXT)

    def text_settings(self):
        setting, ok_pressed = QInputDialog.getItem(
            self, 'Выберите функцию', 'Настроить:',
            ('размер текста',), 1, False)
        if setting == 'размер текста' and ok_pressed:
            font_size, ok_pressed = QInputDialog.getInt(
                self, 'размер текста', 'выбирите размер текста.',
                self.text_font_size, 20, 500, 2)
            self.text_font_size = font_size
        if not ok_pressed:
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121  # за экраном

    def preview(self, text, type):
        self.is_preview = True
        self.draw()
        self.update()
        self.preview_information = (text, type)

    def save(self, fname):
        self.draw()
        self.repaint()
        img = self.image.copy(800, 120, 2100, 2970)  # сохранение рабочей области
        img.save(fname)

    def saver_scl(self):
        file_name_sql = QFileDialog.getOpenFileName(self, 'Выберите базу данных',
                                                    fr'C:\Users\{self.username}\Documents',
                                                    '*')[0]
        if file_name_sql == '':
            return
        directory_name = QFileDialog.getSaveFileName(self, 'Выберете папку сохранения и имена файлов',
                                                     fr'C:\Users\{self.username}\Pictures',
                                                     'Image(*.png);;Image(*.jpg)')
        if directory_name == '':
            return
        file_format = directory_name[1][7:-1]
        directory_name = directory_name[0][:-4]
        if os.path.isfile(directory_name):
            os.remove(directory_name)
        os.mkdir(directory_name)
        file_names = directory_name.split('/')[-1]
        result = self.sql_reader(file_name_sql)
        file_naber = 0
        for names_cart in result:
            self.names_cart = (str(names_cart[0]), str(names_cart[1]), str(names_cart[2]), str(names_cart[3]))
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121  # за экраном
            end_fname = rf'{directory_name}\{file_names}_{file_naber}{file_format}'
            self.save(end_fname)
            file_naber += 1
        self.names_cart = ('Ф.И.О', 'Город', ' Уч. Завидение', 'X',)
        self.draw()
        self.repaint()

    def get_data_csv(self):
        file_name_csv = QFileDialog.getOpenFileName(self, 'Выберите CSV файл',
                                                    fr'C:\Users\{self.username}\Documents',
                                                    '*')[0]
        if file_name_csv == '':
            return
        csv_format, ok_pressed = QInputDialog.getItem(
            self, 'Выберите формат CSV', 'Выберите формат CSV (разделитель элементов списка)',
            ('windows', 'linux', 'свой'), 0, False)
        if not ok_pressed:
            return
        separator_list_items = None
        if csv_format == 'свой':
            separator_list_items, ok_pressed = \
                QInputDialog.getText(self, 'Введите разделитель элементов списка',
                                     'Введите разделитель элементов списка')
        elif csv_format == 'windows':
            separator_list_items = ';'
        elif csv_format == 'linux':
            separator_list_items = ','
        else:
            ok_pressed = False
        if not ok_pressed:
            return
        values, genres = self.csv_reader(separator_list_items, file_name_csv)
        if genres == ['NAME', 'CITI', 'EDUCATIONAL_INSTITUTION', 'PLASE']:
            return values

    def saver_csv(self):
        directory_name = QFileDialog.getSaveFileName(self, 'Выберете папку сохранения и имена файлов',
                                                     fr'C:\Users\{self.username}\Pictures',
                                                     'Image(*.png);;Image(*.jpg)')
        values = self.get_data_csv()
        if values == None:
            return
        file_format = directory_name[1][7:-1]
        directory_name = directory_name[0][:-4]
        if os.path.isfile(directory_name):
            os.remove(directory_name)
        os.mkdir(directory_name)
        file_names = directory_name.split('/')[-1]
        if directory_name == '':
            return
        file_naber = 0
        for names_cart in values:
            self.names_cart = names_cart
            self.draw()
            self.repaint()
            end_fname = rf'{directory_name}\{file_names}_{file_naber}{file_format}'
            self.save(end_fname)
            file_naber += 1
        self.names_cart = ('Ф.И.О', 'Город', ' Уч. Завидение', 'X',)
        self.draw()
        self.repaint()

    def config_save(self):
        file_name = QFileDialog.getSaveFileName(self, 'Выберете папку сохранения и имена файлов',
                                                fr'C:\Users\{self.username}\Documents',
                                                'config(*.config)')
        file_name = file_name[0]
        if file_name != '':
            with open(file_name, 'w') as write_file:
                json.dump(self.config_cart, write_file)
                write_file.close()

    def config_upload(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберите config файл',
                                            fr'C:\Users\{self.username}\Documents',
                                            'config(*.config);;*')[0]
        if fname != '':
            with open(rf'{fname}', 'r') as read_file:
                self.config_cart = json.load(read_file)
                read_file.close()
            self.is_preview = False
            self.draw()
            self.repaint()
            self.mouse_pos = 4161, 3121  # за экраном

    def csv_reader(self, separator_list_items, fname):
        values = []
        file = open(fname, encoding='utf8')
        for number, line in enumerate(file):
            values.append(str(line).replace('\n', '').split(separator_list_items))
        genres = values[0]
        values = values[1:]
        file.close()
        return values, genres

    def sql_reader(self, file_nane_sql):
        connect = sqlite3.connect(file_nane_sql)
        cursor = connect.cursor()
        result = cursor.execute('''
                        SELECT
                            data.NAME,
                            citi.CITI,
                            educational_institution.EDUCATIONAL_INSTITUTION,
                            data.PLASE
                        FROM
                            data
                        INNER JOIN citi ON citi.ID = data.CITI
                        INNER JOIN educational_institution ON educational_institution.ID = data.EDUCATIONAL_INSTITUTION
                        ''').fetchall()
        connect.close()
        return result

    def sql_master_update(self, file_nane_sql, values):
        for value in values:
            connect = sqlite3.connect(file_nane_sql)
            cursor = connect.cursor()
            cursor.execute(f'''
                   INSERT INTO citi(CITI) 
                   SELECT'{value[1]}' 
                   WHERE NOT EXISTS(SELECT 1 FROM citi WHERE CITI = '{value[1]}')
                   ''').fetchall()
            connect.commit()
            cursor.execute(f'''
                   INSERT INTO educational_institution(EDUCATIONAL_INSTITUTION) 
                   SELECT'{value[2]}' 
                   WHERE NOT EXISTS(SELECT 1 FROM educational_institution WHERE EDUCATIONAL_INSTITUTION = '{value[2]}')
                   ''').fetchall()
            connect.commit()
            cursor.execute(f'''
                   INSERT INTO data(NAME, CITI, EDUCATIONAL_INSTITUTION, PLASE) VALUES('{value[0]}', 
                    (SELECT ID FROM citi WHERE CITI = '{value[1]}'),
                    (SELECT ID FROM educational_institution WHERE EDUCATIONAL_INSTITUTION = '{value[2]}'),
                    {int(value[3])})
                   ''').fetchall()
            connect.commit()
            connect.close()

    def sql_create(self):
        values = self.get_data_csv()
        if values == None:
            return
        file_nane_sql = QFileDialog.getSaveFileName(self, 'Выберете папку сохранения и имя базы дданных',
                                                    fr'C:\Users\{self.username}\Documents\BD',
                                                    '*')[0]
        if file_nane_sql == '':
            return
        if os.path.isfile(file_nane_sql):
            os.remove(file_nane_sql)
        connect = sqlite3.connect(file_nane_sql)
        cursor = connect.cursor()
        cursor.execute(f'''
               CREATE TABLE data (
                   ID                      INTEGER PRIMARY KEY AUTOINCREMENT
                                                   UNIQUE
                                                   NOT NULL,
                   NAME                    TEXT,
                   CITI                    INT     REFERENCES citi (ID) ON DELETE SET NULL
                                                                        ON UPDATE RESTRICT,
                   EDUCATIONAL_INSTITUTION INT     REFERENCES educational_institution (ID) ON DELETE SET NULL
                                                                                           ON UPDATE CASCADE,
                   PLASE                   INT
               );
               ''').fetchall()
        cursor.execute('''
               CREATE TABLE citi (
                          ID   INTEGER PRIMARY KEY AUTOINCREMENT
                                       UNIQUE
                                       NOT NULL,
                          CITI TEXT    NOT NULL
                                       UNIQUE
                      );
               ''')
        cursor.execute('''
               CREATE TABLE educational_institution (
                   ID                      INTEGER PRIMARY KEY AUTOINCREMENT
                                                   NOT NULL
                                                   UNIQUE,
                   EDUCATIONAL_INSTITUTION TEXT    NOT NULL
                                                   UNIQUE
               );
               ''')
        connect.commit()
        connect.close()
        self.sql_master_update(file_nane_sql, values)

    def sql_update(self):
        values = self.get_data_csv()
        if values == None:
            return
        file_name_sql = QFileDialog.getOpenFileName(self, 'Выберите базу данных',
                                                    fr'C:\Users\{self.username}\Documents',
                                                    '*')[0]
        if file_name_sql == '':
            return
        self.sql_master_update(file_name_sql, values)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
