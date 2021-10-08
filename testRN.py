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
        # self.tableView.setEditTriggers(EnableEditTriggers)

        for row in range(self.rows_number):
            i = row
            self.tableView.setIndexWidget(
                self.tableView.model().index(row, 0), self.combo_boxes[row]['box'])

        self.tableView.model().dataChanged.connect(self.itemChanged)

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

        self.selected_cols = np.zeros((1, 2))

    def itemChanged(self, selected):

        try:
            y = float(selected.data())
            self.main_data[selected.column()-2][selected.row()] = y
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
        except:
            selected.model().item(selected.row(), selected.column()
                                  ).setData(str(self.main_data[selected.column()-2][selected.row()]))

        """
        try:
            y = float(selected.data())
            self.statusBar().showMessage('OK')
            if selected.column() >= 2:
                self.main_data[selected.column()-2][selected.row()] = y
                y = QtGui.QStandardItem(selected.data())
                #self.tableView.model().setItem(selected.row(), selected.column(), y)
        except:
            if selected.column() >= 2:
                y = self.main_data[selected.column()-2][selected.row()]
                y = QtGui.QStandardItem(str(y))
                self.tableView.model().setItem(selected.row(), selected.column(), y)
            else:
                y = 1
                y = QtGui.QStandardItem(str(y))
                self.tableView.model().setItem(selected.row(), selected.column(), y)
            self.statusBar().showMessage('ERROR')
        if float(selected.data()) < 0 and selected.column() >= 2:
            # задание 1.8: окраска отрицательных значений в красный
            y.setBackground(QtGui.QColor('red'))
        elif float(selected.data()) >= 0 and selected.column() >= 2:
            # задание 1.8: окраска положительных значений в зеленый
            y.setBackground(QtGui.QColor('green'))
            """

    def on_selectionChanged(self, selected):
        sc = self.selected_cols
        col = np.array([index.column() for index in selected.indexes()])
        if (len(col) == self.rows_number and np.mean(col, axis=0) == col[0] and sc[0][-1] != col[0] and col[0] >= 2):
            sc[0] = np.roll(sc[0], -1)
            sc[0][-1] = col[0]
            x = self.main_data[(int(sc[0][0])-2)]
            y = self.main_data[(int(sc[0][1])-2)]
            self.graphWidget.clear()
            self.main_text.setText(f"x:{x} \ny:{y}")
            self.graphWidget.plot(
                x, y, symbol='+', symbolSize=15, symbolBrush=('w'))

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
