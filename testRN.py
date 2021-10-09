import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QTableView, QTableWidgetItem, QMenu, QAction

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

        self.combo_boxes = []
        self.rows_number = 5

        model = QtGui.QStandardItemModel(self.rows_number, 2)
        for row in range(self.rows_number):
            c = createCombobox(row)
            self.combo_boxes.append(c)
            item = QtGui.QStandardItem("1")
            model.setItem(row, 1, item)

        self.tableView = QTableView()
        self.tableView.setModel(model)
        self.setCentralWidget(self.tableView)
        #

        self.iCols = int(self.tableView.model().columnCount())
        self.iRows = int(self.tableView.model().rowCount())
        self.RowHeight = int(self.tableView.rowHeight(0))

        # self.tableView.setEditTriggers(EnableEditTriggers)

        for row in range(self.rows_number):
            i = row
            self.tableView.setIndexWidget(
                self.tableView.model().index(row, 0), self.combo_boxes[row]['box'])

        self.tableView.model().dataChanged.connect(self.itemChanged)

        self.data = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        self.main_data = np.ones((self.iCols, self.iRows))

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

        data2 = self.main_data[1].copy()
        for n in range(0, self.rows_number):
            self.main_data[0][n] = self.combo_boxes[n]['box'].currentText()
            data2[n] = float(self.tableView.model().item(n, 1).text())
            if all(self.main_data[1] != data2) == True:
                self.main_data[1] = data2
                data2 = data2.reshape(1, self.rows_number)
                self.main_data = np.concatenate(
                    [self.main_data, np.array([self.main_data[0]])], dtype=float)
                self.main_data = np.concatenate(
                    [self.main_data, data2], dtype=float)
                self.changeTable()

    def changeTable(self):

        new_col = int(self.tableView.model().columnCount())
        for row in range(self.rows_number):
            self.tableView.model().setItem(
                row, (new_col), QtGui.QStandardItem(str(self.main_data[0][row])))
            self.tableView.model().setItem(
                row, (new_col+1), QtGui.QStandardItem(str(float(self.main_data[1][row]))))

    def itemChanged(self, selected):
        if selected.column() >= 1:
            try:
                y = float(selected.data())
                self.main_data[selected.column()][selected.row()] = y
                selected.model().item(selected.row(), selected.column()
                                      ).setData(str(y))
                if y < 0:
                    # задание 1.8: окраска отрицательных значений в красный
                    selected.model().item(selected.row(), selected.column()
                                          ).setBackground(QtGui.QColor('red'))
                elif y >= 0:
                    # задание 1.8: окраска положительных значений в зеленый
                    selected.model().item(selected.row(), selected.column()
                                          ).setBackground(QtGui.QColor('green'))
            except:
                self.statusBar().showMessage("Вводить можно только цифровые значения")
                y = self.main_data[selected.column()][selected.row()]
                y = QtGui.QStandardItem(str(y))
                self.tableView.model().setItem(selected.row(), selected.column(), y)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
