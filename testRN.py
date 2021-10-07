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

        def createCombobox(row):
            c = QComboBox()
            c.addItems(['1', '2', '3', '4', '5'])
            box = {
                'box': c,
                'index': row,
                'changed': lambda index: self.refreshCount(index, row)
            }
            c.currentIndexChanged[str].connect(
                box['changed'])
            return box

        self.data = np.array([1, 1, 1, 1, 1])
        self.combo_boxes = []
        self.rows_number = 6

        model = QtGui.QStandardItemModel(self.rows_number, 2)
        for row in range(self.rows_number):
            c = createCombobox(row)
            self.combo_boxes.append(c)
            item = QtGui.QStandardItem("1")
            model.setItem(row, 1, item)

        self.tableView = QTableView()
        self.tableView.setModel(model)
        self.setCentralWidget(self.tableView)

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
        y1 = y
        y = np.around(y, decimals=2)  # округление до двух знаков

        y = QtGui.QStandardItem(str(y))
        self.tableView.model().setItem(row_index, 1, y)
        if y1 < 0:
            # задание 1.8: окраска отрицательных значений в красный
            y.setBackground(QtGui.QColor('red'))
        elif y1 >= 0:
            # задание 1.8: окраска положительных значений в зеленый
            y.setBackground(QtGui.QColor('green'))

        

    


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
