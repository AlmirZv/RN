import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAbstractItemView, QComboBox, QMainWindow, QPushButton, QMessageBox, QApplication, QTableView, QTableWidget, QTableWidgetItem, QMenu, QAction
from PyQt5.QtCore import Qt, QModelIndex

import numpy as np

import h5py


import pyqtgraph as pg


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.setGeometry(300, 100, 520, 620)
        self.setWindowTitle('RN задание')

        def createCombobox(row):
            c = QComboBox()
            c.addItems(['1', '2', '3', '4', '5'])
            box = {
                'box': c,
                'index': row,
                'changed': lambda index: self.refreshCount(index, row)
            }
            if row < 5:
                c.setCurrentIndex(row)
            else:
                c.setCurrentIndex(4)
            c.currentIndexChanged[str].connect(
                box['changed'])
            return box

        self.data = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        self.combo_boxes = []
        self.rows_number = 5
        self.main_data = 0

        model = QtGui.QStandardItemModel(self.rows_number, 2)
        for row in range(self.rows_number):
            c = createCombobox(row)
            self.combo_boxes.append(c)
            item = QtGui.QStandardItem("1")
            model.setItem(row, 1, item)

        self.tableView = QTableView()
        self.tableView.setModel(model)
        self.setCentralWidget(self.tableView)
        self.iCols = int(self.tableView.model().columnCount())
        self.iRows = int(self.tableView.model().rowCount())
        self.RowHeight = int(self.tableView.rowHeight(0))

        for row in range(self.rows_number):
            i = row
            self.tableView.setIndexWidget(
                self.tableView.model().index(row, 0), self.combo_boxes[row]['box'])

        # График
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.resize(490, 325)
        self.oy = ((self.iRows+1)*self.RowHeight+5)
        self.graphWidget.move(15, self.oy)

        # selected cols
        self.tableView.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        self.xo = []
        self.yo = []

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText(f"x: {self.xo} \ny: {self.yo}")
        # установка положения текста
        self.main_text.move(15, self.oy+330)
        self.main_text.setGeometry(15, self.oy+300, 500, 90)
        # self.main_text.adjustSize()  # корректировка текста с размером окна

    def on_selectionChanged(self, selected):
        z = 0
        x = []
        for index in selected.indexes():
            r = int(index.row())
            c = int(index.column())
            if index.data() == None:
                pass
            else:
                d = float(index.data())
                z += 1
                print("row-", r, ",col-", c, ",data-", d)
                x.append(d)
            if z == self.iRows:
                if self.xo == []:
                    self.xo = x
                    self.main_text.setText(f"x:{self.xo} \ny:{self.yo}")
                elif self.yo == []:
                    self.yo = x
                    self.graphWidget.clear()
                    self.graphWidget.plot(
                        self.xo, self.yo, symbol='+', symbolSize=15, symbolBrush=('w'))
                    self.main_text.setText(f"x:{self.xo} \ny:{self.yo}")

                elif self.xo != [] and self.yo != []:
                    self.xo = self.yo
                    self.yo = x
                    self.graphWidget.clear()
                    self.graphWidget.plot(
                        self.xo, self.yo, symbol='+', symbolSize=15, symbolBrush=('w'))
                    self.main_text.setText(f"x:{self.xo} \ny:{self.yo}")
                print("x", self.xo)
                print("y", self.yo)

    # Функция кнопки пересчета №2

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

        data2 = self.data.copy()
        perv_stolb = []
        for n in range(0, self.rows_number):
            perv_stolb.append(self.combo_boxes[n]['box'].currentText())
            data2[n] = float(self.tableView.model().item(n, 1).text())
            if all(self.data != data2) == True:
                self.data = data2
                data2 = data2.reshape(1, self.rows_number)
                if type(self.main_data) != np.ndarray:
                    perv_stolb2 = np.array(perv_stolb, dtype=float)
                    self.main_data = perv_stolb2.copy().reshape(1, self.rows_number)
                    self.main_data = np.concatenate(
                        [self.main_data, data2], dtype=float)

                    self.changeTable(perv_stolb2, data2)
                else:
                    perv_stolb2 = np.array(perv_stolb, dtype=float).reshape(
                        1, self.rows_number)
                    self.main_data = np.concatenate(
                        [self.main_data, perv_stolb2], dtype=float)
                    self.main_data = np.concatenate(
                        [self.main_data, data2], dtype=float)
                    self.changeTable(perv_stolb2[0], data2)

    def changeTable(self, perv_stolb2, data2):
        new_col = int(self.tableView.model().columnCount())
        for row in range(self.rows_number):
            self.tableView.model().setItem(
                row, (new_col), QtGui.QStandardItem(str(perv_stolb2[row])))

            x = float(data2[0][row])
            x1 = x
            x = QtGui.QStandardItem(str(x))
            self.tableView.model().setItem(row, (new_col+1), x)
            if x1 < 0:
                # задание 1.8: окраска отрицательных значений в красный
                x.setBackground(QtGui.QColor('red'))
            elif x1 >= 0:
                # задание 1.8: окраска положительных значений в зеленый
                x.setBackground(QtGui.QColor('green'))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
