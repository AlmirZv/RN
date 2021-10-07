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
            c.setCurrentIndex(row)
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

        for row in range(self.rows_number):
            i = row
            self.tableView.setIndexWidget(
                self.tableView.model().index(row, 0), self.combo_boxes[row]['box'])

    # Функция кнопки пересчета №2

    def refreshCount(self, value, row_index):
        print("--------------------------")
        print(row_index, " Row, Value is - ", value)
        print("--------------------------")
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
            print("--------------------------")
            print(self.data)
            print(data2)
            print("--------------------------")
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
                print("--------------------------")
                print(self.main_data)
                print(np.shape(self.main_data))
                print("--------------------------")
                print(self.data)
                print(data2)
                print("--------------------------")
            else:
                print(all(self.data != data2))
        print(perv_stolb)
        """data2 = self.data2
        data2[row_index] = y1
        print(data2)
        print("--------------------------")
        print(self.data)
        if all(self.data != data2) == True:
            self.data = data2
            print("--------------------------")
            print(self.data)
            print(data2)
            print("--------------------------")
        else:
            print(all(self.data != data2))
        for n in range(0, self.rows_number):
            print("--------------------------")
            # print(self.combo_boxes[n]['box'].currentText())
            #data2[n] = float(self.tableView.model().item(n, 1).text())
            print(data2)
            #print(self.tableView.model().item(n, 1).text(), "!=", self.data[n])
            print(self.data)"""

    def changeTable(self, perv_stolb2, data2):
        print("============================================")
        print(perv_stolb2)
        print(data2)
        print("main_data_new:")
        print(self.main_data)
        print("============================================")
        new_row = len(self.main_data[0])
        new_col = int(self.tableView.model().columnCount())
        #model = QtGui.QStandardItemModel(new_row, new_col)
        #self.tableView.model().insertColumns(self.iCols, len(self.main_data))
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

            """y = np.power(int(value), 2)*np.pi*np.random.uniform(-1, 1)
            y = np.around(y, decimals=2)  # округление до двух знаков
            y1 = y

            y = QtGui.QStandardItem(str(y))
            self.tableView.model().setItem(row_index, 1, y)
            if y1 < 0:
                # задание 1.8: окраска отрицательных значений в красный
                y.setBackground(QtGui.QColor('red'))
            elif y1 >= 0:
                # задание 1.8: окраска положительных значений в зеленый
                y.setBackground(QtGui.QColor('green'))"""


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
