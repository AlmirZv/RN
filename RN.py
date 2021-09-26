import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox, QApplication, QTableWidget, QTableWidgetItem, QMenu, QAction
from PyQt5.QtCore import Qt

import numpy as np

import h5py


import pyqtgraph as pg


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self._createActions()
        self._createMenuBar()
        self._connectActions()

        # Установка текста таблицы
        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Таблица с числами")
        self.main_text.move(200, 20)  # установка положения текста
        self.main_text.adjustSize()  # корректировка текста с размером окна

        self.initUI()

        # задание 1.1: Таблица с числами
        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setColumnCount(3)     # Устанавливаем три колонки
        self.table.setRowCount(5)        # и 5 строк в таблице

        # Установка положения таблицы х=10, у=35 и размеры w=500, h=185
        self.table.setGeometry(10, 35, 500, 185)

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(
            ["Значения", "Значения", "Пересчет"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.table.horizontalHeaderItem(1).setToolTip("Column 2 ")

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignRight)

        # задание 1.3: создание столбца в таблице в котором все значения выбираются из выпадающего списка чисел от 1 до 5
        row = 0
        for n in range(0, 5):
            # меню для выбора
            combo = QtWidgets.QComboBox()  # виджет для создания выпадающего списка значений
            combo.addItem("1")
            combo.addItem("2")
            combo.addItem("3")
            combo.addItem("4")
            combo.addItem("5")

            # заполняем строки
            self.table.setCellWidget(row, 0, combo)
            row += 1

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        # задание 1.5 Кнопка сохранения данных(для накопления значений из другого столбца)
        self.btn_save = QPushButton('Запомнить значения', self)
        self.btn_save.setGeometry(10, 225, 120, 30)
        self.btn_save.clicked.connect(self.saveClicked)

        # задание 1.4: Кнопка пересчета(расчет по формуле определения площади круга по радиусу)
        self.btn_recount = QPushButton('Пересчет', self)
        self.btn_recount.setGeometry(140, 225, 70, 30)
        self.btn_recount.clicked.connect(self.refreshCount)

        # задание 1.4: Кнопка пересчета №2(расчет рандомных чисел)
        self.btn_recount2 = QPushButton('Пересчет №2', self)
        self.btn_recount2.setGeometry(220, 225, 100, 30)
        self.btn_recount2.clicked.connect(self.refreshCount2)

        # Таблица выбранных строк для графика
        self.table.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        self.graphtable = QTableWidget(self)  # Создаём таблицу
        self.graphtable.setColumnCount(5)     # Устанавливаем  колонки
        self.graphtable.setRowCount(2)        # и строки в таблице

        self.graphtable.setGeometry(10, 260, 500, 90)

        # Устанавливаем заголовки таблицы
        self.graphtable.setVerticalHeaderLabels(
            ["x", "y"])

        # делаем ресайз колонок по содержимому
        self.graphtable.resizeColumnsToContents()

        # График
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.resize(400, 250)
        self.graphWidget.move(10, 360)

    # создание меню
    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = QMenu("Файл", self)  # добавление в меню пункта "Файл"
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        # создание подменю "открыть файл"
        openmenu = fileMenu.addMenu('Открыть файл')
        openmenu.addAction(self.openAction)
        openmenu.addAction(self.openh5Action)
        # подменю "сохранить как"
        savemenu = fileMenu.addMenu('Сохранить как')
        savemenu.addAction(self.saveAction)
        savemenu.addAction(self.saveh5Action)
        fileMenu.addAction(self.exitAction)
        # подменю "помощь"
        helpMenu = menuBar.addMenu("Помощь")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    # создание действий для меню
    def _createActions(self):
        self.newAction = QAction(self)
        self.newAction.setText("Новый")
        self.openAction = QAction("Открыть txt", self)
        self.openh5Action = QAction("Открыть hdf5")
        self.saveAction = QAction("Сохранить txt", self)
        self.saveh5Action = QAction("Сохранить hdf", self)
        self.exitAction = QAction("Закрыть", self)
        self.helpContentAction = QAction("Задание", self)
        self.aboutAction = QAction("Автор", self)

    # подключение сигналов к пунктам меню
    def _connectActions(self):
        # Подключение сигналов к пункту "файл"
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.openh5Action.triggered.connect(self.openh5File)
        self.saveAction.triggered.connect(self.saveFile)
        self.saveh5Action.triggered.connect(self.saveh5File)
        self.exitAction.triggered.connect(self.close)

        # Подключение сигналов к пункту "Помощь"
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)

    # Функция для очистки всех данных с окна
    def newFile(self):
        count = self.table.columnCount()
        for col in range(3, count):
            self.table.removeColumn(3)
        self.graphtable.clear()
        self.graphWidget.clear()

    # задание1.7: Пункт открыть файл .txt
    def openFile(self):
        b = np.loadtxt('data.txt')
        bc = 0
        count = self.table.columnCount()
        self.table.setColumnCount(len(b)+count)
        self.table.resizeColumnsToContents()
        for c in range(count, count+len(b)):
            for r in range(0, 5):
                x2 = QTableWidgetItem(str(b[bc][r]))
                if (c) % 2 != 0:
                    pass
                else:
                    if float(b[bc][r]) < 0:
                        x2.setBackground(QtGui.QColor('red'))
                    elif float(b[bc][r]) >= 0:
                        x2.setBackground(QtGui.QColor('green'))
                self.table.setItem(r, c, x2)
            bc += 1

    # задание1.7: Пункт открыть файл .hdf5
    def openh5File(self):
        with h5py.File('data2.hdf5', 'r') as f:
            data = f['dataset_01'][:]
        b = data
        bc = 0
        count = self.table.columnCount()
        self.table.setColumnCount(len(b)+count)
        self.table.resizeColumnsToContents()
        for c in range(count, count+len(b)):
            for r in range(0, 5):
                x2 = QTableWidgetItem(str(b[bc][r]))
                if (c) % 2 != 0:
                    pass
                else:
                    if float(b[bc][r]) < 0:
                        x2.setBackground(QtGui.QColor('red'))
                    elif float(b[bc][r]) >= 0:
                        x2.setBackground(QtGui.QColor('green'))
                self.table.setItem(r, c, x2)
            bc += 1

    # задание1.7: Пункт сохранить как .txt
    def saveFile(self):
        count = self.table.columnCount()
        v = []
        for c in range(3, count):
            b = []
            for r in range(0, 5):
                a = self.table.item(r, c).text()
                b.append(a)
            v.append(b)
        np.savetxt('data.txt', v, fmt='%s')

    # задание1.7: Пункт сохранить как .hdf5
    def saveh5File(self):
        count = self.table.columnCount()
        v = []
        for c in range(3, count):
            b = []
            for r in range(0, 5):
                a = self.table.item(r, c).text()
                b.append(a)
            v.append(b)
        with h5py.File('data2.hdf5', 'w') as f:
            dset = f.create_dataset(
                "dataset_01", ((count-3), 5), dtype='f', data=v)

    # Пункт "Задание"
    def helpContent(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("""Задание 1. Окно с таблицей и графиком.

1.       Окно должно содержать таблицу (QTableView) с числами и график под таблицей.

2.       Все данные внутри должны храниться в двумерном numpy-массиве.

3.       Один из столбцов должен позволять редактировать числа только из выпадающего списка чисел от 1 до 5.

4.       Значения в одном из столбцов должны пересчитываться из значений в этой же строчке в другом столбце (нужен сигнал, на который все могут подписаться).

5.       Значения в одном из столбцов должны содержать накопленные значения из другого столбца (нужен сигнал, на который все могут подписаться).

6.       При выборе двух столбцов должен отображаться график (желательно в pyqtgraph) зависимости второго выбранного столбца от первого.

7.       Нужны кнопки для сохранения массива в текстовый файл или в hdf, загрузки его из текстового файла или hdf, для изменения размера массива и заполнения его (кроме особенных ячеек, которые пересчитываются) случайными значениями.

8.       В одном из столбцов ячейки должны заливаться красным или зеленым цветом в зависимости от того, положительные они или отрицательные.

9.       Факультативно: Второй вариант той же самой программы - когда данные внутри не хранятся в промежуточном numpy-массиве, и работа идет непосредственно с датасетом из hdf-файла БЕЗ кеширования из пункта 2.

10.   Код должен быть тщательно прокомментирован (самодокументированный код мы не допускаем: комментарии описывают, что и зачем происходит, а не как)

11.   Код, работающий с numpy должен быть по возможности векторизован, никаких циклов для подсчета суммы""")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    # Пункт Автор
    def about(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("""Автор: Закирьянов Альмир
        
Работа: Задание на  Собеседование РН-БашНИПИнефть""")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    # Пункт сохранить только через виджет QFileDialog. Не успел реализовать
    """def saveInput(self):

        name = QtWidgets.QFileDialog.getSaveFileName(
            Window, "Save File", '/', '.txt')[0]
        file = open(name, 'w')
        text = self.lineEdit.text()
        file.write(text)
        file.close()"""

    # Функция кнопки сохранения данных
    def saveClicked(self):
        count = self.table.columnCount()
        self.table.setColumnCount(count+2)
        self.table.resizeColumnsToContents()
        for n in range(0, 5):
            # сохранение значения
            z = str(self.table.cellWidget(n, 0).currentText())
            z2 = QTableWidgetItem(z)
            self.table.setItem(n, count, z2)

            # сохранение пересчета
            if self.table.item(n, 2) == None:
                x2 = QTableWidgetItem(0)
                self.table.setItem(n, count+1, x2)
            else:
                x = str(self.table.item(n, 2).text())
                x2 = QTableWidgetItem(x)
                if float(x) < 0:
                    x2.setBackground(QtGui.QColor('red'))
                elif float(x) >= 0:
                    x2.setBackground(QtGui.QColor('green'))
                self.table.setItem(n, count+1, x2)

    # Функция кнопки пересчета
    def refreshCount(self):
        for n in range(0, 5):
            # получение значения с n строки и 0 столбца
            z = str(self.table.cellWidget(n, 0).currentText())
            z2 = QTableWidgetItem(z)
            self.table.setItem(n, 1, z2)

            y = np.power(int(z), 2)*np.pi  # формула площади круга
            y = np.around(y, decimals=2)  # округление до двух знаков

            y = QTableWidgetItem(str(y))
            self.table.setItem(n, 2, y)
            if np.power(int(z), 2)*np.pi < 0:
                y.setBackground(QtGui.QColor('red'))
            elif np.power(int(z), 2)*np.pi >= 0:
                y.setBackground(QtGui.QColor('green'))

    # Функция кнопки пересчета №2
    def refreshCount2(self):
        for n in range(0, 5):
            z = str(self.table.cellWidget(n, 0).currentText())
            z2 = QTableWidgetItem(z)
            self.table.setItem(n, 1, z2)

            # формула площади круга * на рандомное значение от (-1,1)
            y = np.power(int(z), 2)*np.pi*np.random.uniform(-1, 1)
            y1 = y
            y = np.around(y, decimals=2)  # округление до двух знаков

            y = QTableWidgetItem(str(y))
            self.table.setItem(n, 2, y)
            if y1 < 0:
                # задание 1.8: окраска отрицательных значений в красный
                y.setBackground(QtGui.QColor('red'))
            elif y1 >= 0:
                # задание 1.8: окраска положительных значений в зеленый
                y.setBackground(QtGui.QColor('green'))

    # задание 1.6: функция для выбора значений из выделенных столбцов
    def on_selectionChanged(self, selected):
        for index in selected.indexes():
            r = int(index.row())
            c = int(index.column())
            table = self.table
            graphtable = self.graphtable

            if graphtable.item(1, r) == None:
                if table.item(r, c) == None:
                    pass
                else:
                    y_item = str(table.item(r, c).text())
                    graphtable.setItem(1, r, QTableWidgetItem(y_item))
            else:
                if table.item(r, c) == None:
                    pass
                else:
                    x_item = str(graphtable.item(1, r).text())
                    graphtable.setItem(0, r, QTableWidgetItem(x_item))

                    y_item = str(table.item(r, c).text())
                    graphtable.setItem(1, r, QTableWidgetItem(y_item))

        if self.graphtable.item(0, 0) == None:
            pass
        else:
            if float(self.graphtable.item(0, 0).text()) != None:
                self.graphWidget.clear()
                x = []
                y = []
                for i in range(0, 5):
                    # сбор данных с таблицы
                    x.append(float(self.graphtable.item(0, i).text()))
                    y.append(float(self.graphtable.item(1, i).text()))

                self.graphWidget.plot(x, y)
            else:
                pass

    # Утановка положения и размеров главного окна, + титул(название окна)
    def initUI(self):

        self.setGeometry(300, 100, 520, 620)
        self.setWindowTitle('RN задание')

    # кнопка закрыть окно
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Выход',
                                     "Вы уверены что хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Загрузка приложения(запуск окна)
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
