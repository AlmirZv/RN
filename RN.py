import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QTableView, QMenu, QAction

import numpy as np

import h5py

import pyqtgraph as pg


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self._createActions()  # создание действий для меню
        self._createMenuBar()  # создание меню
        self._connectActions()  # подключение сигналов к пунктам меню

        self.setGeometry(300, 100, 520, 620)  # установка формы окна
        self.setWindowTitle('RN задание')  # установка заголовка окна

        # функция для создания комбобоксов(выпадающего списка чисел от 1 до 5) для каждой строки
        def createCombobox(row):
            c = QComboBox()
            c.addItems(['1', '2', '3', '4', '5'])
            box = {
                'box': c,
                'index': row,
                'changed': lambda index: self.refreshCount(index, row)
            }  # словарь комбобоксов содержит объект комбобокса, строку нахождения в таблице, и сигнал функции для перерасчета

            c.currentIndexChanged[str].connect(
                box['changed'])  # Вызов сигнала при изменении значения комбобокса
            return box

        self.combo_boxes = []
        self.rows_number = 5

        model = QtGui.QStandardItemModel(self.rows_number, 2)
        # раскладка объектов комбобокса по строкам модели таблицы
        for row in range(self.rows_number):
            c = createCombobox(row)
            self.combo_boxes.append(c)
            item = QtGui.QStandardItem("1")
            model.setItem(row, 1, item)

        self.tableView = QTableView()  # создание таблицы
        self.tableView.setModel(model)  # задание модели таблицы
        # установка таблицы центральным виджетом окна
        self.setCentralWidget(self.tableView)

        # раскладка объектов комбобокса по строкам таблицы
        for row in range(self.rows_number):
            self.tableView.setIndexWidget(
                self.tableView.model().index(row, 0), self.combo_boxes[row]['box'])

        self.tableView.model().dataChanged.connect(
            self.itemChanged)  # сигнал проверки измении таблицы

        self.iCols = int(self.tableView.model().columnCount()
                         )  # счет строк таблицы
        self.iRows = int(self.tableView.model().rowCount()
                         )  # счет колонн таблицы
        self.RowHeight = int(self.tableView.rowHeight(0)
                             )  # высота строк таблицы

        # массив для хранения всех данных таблицы
        self.main_data = np.ones((self.iCols, self.iRows))

        # График
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.resize(490, 325)
        self.graphy = ((self.iRows+1)*self.RowHeight+20)
        self.graphWidget.move(15, self.graphy)

        # сигнал выбранных элементов, для получения выбранных столбов
        self.tableView.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        # осевые координаты для постройки графика:
        self.xo = []
        self.yo = []

        self._text = QtWidgets.QLabel(self)  # текст с координатами под график
        self._text.setText(f"x: {self.xo} \ny: {self.yo}")
        # установка положения текста
        self._text.setGeometry(15, self.graphy+300, 500, 90)

        # массив для хранения выбранных столбцов
        self.selected_cols = np.zeros((1, 2))

    # функция, сигнал для получения выбранных столбцов и для постройки графика по данным
    def on_selectionChanged(self, selected):
        sc = self.selected_cols
        # список индексов выделенных ячеек
        col = np.array([index.column() for index in selected.indexes()])
        # отсеивание повторного выбора столбцов
        if (len(col) == self.rows_number and np.mean(col, axis=0) == col[0] and sc[0][-1] != col[0] and col[0] >= 2):
            sc[0] = np.roll(sc[0], -1)
            sc[0][-1] = col[0]  # замена выбранных столбцов новыми
            x = self.main_data[int(sc[0][0])]  # ось х
            y = self.main_data[int(sc[0][1])]  # ось у
            self.graphWidget.clear()  # очистка старого графика
            self._text.setText(f"x:{x} \ny:{y}")
            self.graphWidget.plot(
                x, y, symbol='+', symbolSize=15, symbolBrush=('w'))  # постройка графика

    # Функция кнопки перерасчета
    def refreshCount(self, value, row_index):
        # формула площади круга * на рандомное значение от (-1,1)
        y = np.power(int(value), 2)*np.pi*np.random.uniform(-1, 1)
        y = np.around(y, decimals=2)  # округление до двух знаков
        y1 = y
        y = QtGui.QStandardItem(str(y))
        self.tableView.model().setItem(row_index, 1, y)
        if y1 < 0:
            # задание 1.8: окраска отрицательных значений в красный
            y.setBackground(QtGui.QColor('red'))
        elif y1 >= 0:
            # задание 1.8: окраска положительных значений в зеленый
            y.setBackground(QtGui.QColor('green'))

        # сигнал для пункта задания №5, при изменении всех ячеек комбобоксов вызывается сигнал и данные записываются в массив, данные аблицы обновляются
        # копия второго столбца таблицы для сравнения
        data2 = self.main_data[1].copy()
        for n in range(0, self.rows_number):
            # получение значений с комбобоксов
            self.main_data[0][n] = self.combo_boxes[n]['box'].currentText()
            # установка новых значений 2 столбца для сравнения
            data2[n] = float(self.tableView.model().item(n, 1).text())
            # сравнение новых значений со старыми, если все изменены, то  поступает сигнал для сохранения новых данных
            if all(self.main_data[1] != data2) == True:
                self.main_data[1] = data2
                data2 = data2.reshape(1, self.rows_number)
                self.main_data = np.concatenate(
                    [self.main_data, np.array([self.main_data[0]])], dtype=float)  # запись первого столбца в массив базы данных
                self.main_data = np.concatenate(
                    [self.main_data, data2], dtype=float)  # запись второго столбца в массив базы данных
                self.changeTable()  # сам сигнал

    # сигнал автоматического добавления новых данных в базу
    def changeTable(self):

        new_col = int(self.tableView.model().columnCount())
        for row in range(self.rows_number):
            self.tableView.model().setItem(
                row, (new_col), QtGui.QStandardItem(str(self.main_data[0][row])))  # добавление значений в таблицу 1 столбец
            self.tableView.model().setItem(
                row, (new_col+1), QtGui.QStandardItem(str(float(self.main_data[1][row]))))  # добавление значений в таблицу 2 столбец

    # контроль изменений в таблице, защита от записи не цифровых значений
    def itemChanged(self, selected):
        if selected.column() >= 1:
            try:
                y = float(selected.data())
                if selected.column() >= 2:
                    self.main_data[selected.column()][selected.row()] = y
                    selected.model().item(selected.row(), selected.column()
                                          ).setData(str(y))
                    if y < 0 and selected.column() >= 2:
                        # задание 1.8: окраска отрицательных значений в красный
                        selected.model().item(selected.row(), selected.column()
                                              ).setBackground(QtGui.QColor('red'))
                    elif y >= 0 and selected.column() >= 2:
                        # задание 1.8: окраска положительных значений в зеленый
                        selected.model().item(selected.row(), selected.column()
                                              ).setBackground(QtGui.QColor('green'))
                else:
                    if y < 0:
                        # задание 1.8: окраска отрицательных значений в красный
                        selected.model().item(selected.row(), selected.column()
                                              ).setBackground(QtGui.QColor('red'))
                    elif y >= 0:
                        # задание 1.8: окраска положительных значений в зеленый
                        selected.model().item(selected.row(), selected.column()
                                              ).setBackground(QtGui.QColor('green'))
            except:
                self.statusBar().setStyleSheet("color : red")
                self.statusBar().showMessage("Вводить можно только цифровые значения", 5000)
                y = self.main_data[selected.column()][selected.row()]
                y = QtGui.QStandardItem(str(y))
                self.tableView.model().setItem(selected.row(), selected.column(), y)

    # создание меню
    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = QMenu("Файл", self)  # добавление в меню пункта "Файл"
        menuBar.addMenu(fileMenu)
        # создание подменю "открыть файл"
        openmenu = fileMenu.addMenu('Открыть файл')
        openmenu.addAction(self.openAction)
        openmenu.addAction(self.openh5Action)
        # подменю "сохранить как"
        savemenu = fileMenu.addMenu('Сохранить как')
        savemenu.addAction(self.saveAction)
        savemenu.addAction(self.saveh5Action)
        fileMenu.addAction(self.exitAction)

    # создание действий для меню
    def _createActions(self):
        self.openAction = QAction("Открыть txt", self)
        self.openh5Action = QAction("Открыть hdf5")
        self.saveAction = QAction("Сохранить txt", self)
        self.saveh5Action = QAction("Сохранить hdf", self)
        self.exitAction = QAction("Закрыть", self)

    # подключение сигналов к пунктам меню
    def _connectActions(self):
        # Подключение сигналов к пункту "файл"
        self.openAction.triggered.connect(self.openFile)
        self.openh5Action.triggered.connect(self.openh5File)
        self.saveAction.triggered.connect(self.saveFile)
        self.saveh5Action.triggered.connect(self.saveh5File)
        self.exitAction.triggered.connect(self.close)

    # задание1.7: Пункт открыть файл .txt
    def openFile(self):
        try:
            b = np.loadtxt('dataRNZakiryanov.txt')
            self.main_data = np.concatenate([self.main_data, b])
            bc = 0
            rows = self.rows_number
            count = int(self.tableView.model().columnCount())
            for c in range(count, count+len(b)):
                for r in range(rows):
                    x2 = QtGui.QStandardItem(str(b[bc][r]))
                    if float(b[bc][r]) < 0:
                        x2.setBackground(QtGui.QColor('red'))
                    elif float(b[bc][r]) >= 0:
                        x2.setBackground(QtGui.QColor('green'))
                    self.tableView.model().setItem(r, c, x2)
                bc += 1
        except:
            self.statusBar().setStyleSheet("color : red")
            self.statusBar().showMessage("Такого файла не существует!!!", 5000)

    # задание1.7: Пункт открыть файл .hdf5
    def openh5File(self):
        try:
            with h5py.File('dataRNZakiryanov.hdf5', 'r') as f:
                data = f['dataset_01'][:]
            b = data
            self.main_data = np.concatenate([self.main_data, b])
            bc = 0
            count = int(self.tableView.model().columnCount())
            for c in range(count, count+len(b)):
                for r in range(0, 5):
                    x2 = QtGui.QStandardItem(str(b[bc][r]))
                    if (c) % 2 != 0:
                        pass
                    else:
                        if float(b[bc][r]) < 0:
                            x2.setBackground(QtGui.QColor('red'))
                        elif float(b[bc][r]) >= 0:
                            x2.setBackground(QtGui.QColor('green'))
                    self.tableView.model().setItem(r, c, x2)
                bc += 1
        except:
            self.statusBar().setStyleSheet("color : red")
            self.statusBar().showMessage("Такого файла не существует!!!", 5000)

    # задание1.7: Пункт сохранить как .txt
    def saveFile(self):
        main_data = np.delete(self.main_data, [0, 1], 0)
        np.savetxt('dataRNZakiryanov.txt', main_data, fmt='%s')

    # задание1.7: Пункт сохранить как .hdf5
    def saveh5File(self):
        main_data = np.delete(self.main_data, [0, 1], 0)
        count = int(self.tableView.model().columnCount())
        with h5py.File('dataRNZakiryanov.hdf5', 'w') as f:
            dset = f.create_dataset(
                "dataset_01", main_data.shape, dtype='f', data=main_data)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
