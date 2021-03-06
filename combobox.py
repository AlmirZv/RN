import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QMainWindow, QPushButton, QMessageBox, QApplication, QTableView, QTableWidget, QTableWidgetItem, QMenu, QAction
from PyQt5.QtCore import Qt, QModelIndex

import numpy as np

import h5py


import pyqtgraph as pg


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.data = np.array([1, 1, 1, 1, 1])
        model = QtGui.QStandardItemModel(5, 2)
        for row in range(5):
            item = QtGui.QStandardItem("1")
            model.setItem(row, 1, item)

        self.tableView = QTableView()
        self.tableView.setModel(model)
        self.setCentralWidget(self.tableView)

        self.c0 = QComboBox(self)
        self.c0.addItems(['1', '2', '3', '4', '5', ])
        i = self.tableView.model().index(0, 0)
        self.tableView.setIndexWidget(i, self.c0)
        self.c0.currentIndexChanged[str].connect(self.def1)

        self.c1 = QComboBox(self)
        self.c1.addItems(['1', '2', '3', '4', '5', ])
        i = self.tableView.model().index(1, 0)
        self.tableView.setIndexWidget(i, self.c1)
        self.c1.currentIndexChanged[str].connect(self.def1)

        self.c2 = QComboBox(self)
        self.c2.addItems(['1', '2', '3', '4', '5', ])
        i = self.tableView.model().index(2, 0)
        self.tableView.setIndexWidget(i, self.c2)
        self.c2.currentIndexChanged[str].connect(self.def3)

        self.c3 = QComboBox(self)
        self.c3.addItems(['1', '2', '3', '4', '5', ])
        i = self.tableView.model().index(3, 0)
        self.tableView.setIndexWidget(i, self.c3)
        self.c3.currentIndexChanged[str].connect(self.def4)

        self.c4 = QComboBox(self)
        self.c4.addItems(['1', '2', '3', '4', '5', ])
        i = self.tableView.model().index(4, 0)
        self.tableView.setIndexWidget(i, self.c4)
        self.c4.currentIndexChanged[str].connect(self.def5)

    def def1(self, value):
        print(self.tableView.selectionModel())

    def def2(self, value):
        print(value)

    def def3(self, value):
        print(value)

    def def4(self, value):
        print(value)

    def def5(self, value):
        print(value)

    def refreshCount1(self, value):
        print(value)

        """self.c1.currentIndexChanged[int].connect(self.refreshCount1)
        self.c0.activated[str].connect(self.refreshCount1)
        self.tableView.clicked.connect(self.clickedSlot)"""

    def clickedSlot(self, index):
        print("Column is " + str(index.column()))
        print("Row is " + str(index.row()))
        # ?????????????? ???????????? ?????????????????? ???2

    def refreshCount1(self, value):
        print(self.c0)
        #print(self.c.currentText(), self.c.currentData())
        print(value)
        data = self.data
        z2 = []

        # print(value)
        for n in range(0, 5):
            index = self.tableView.model().index(n, 0)
            # self.tableView.ite
            # print(index)
            #value = self.c.itemText(int(value))

    def refreshCount2(self, value):
        data = self.data
        z2 = []
        # print(value)
        for n in range(0, 5):
            index = self.tableView.model().index(n, 0)
            # print(index)
            #value = self.c.itemText(int(value))
            """z = value
            z = int(self.table.indexWidget(n, 0).currentText())
            # print(z)
            z2.append(z)

            if data[n] != z:
                # ?????????????? ?????????????? ?????????? * ???? ?????????????????? ???????????????? ???? (-1,1)
                y = np.power(int(z), 2)*np.pi*np.random.uniform(-1, 1)
                y1 = y
                y = np.around(y, decimals=2)  # ???????????????????? ???? ???????? ????????????

                y = QtGui.QStandardItem(str(y))
                self.tableView.model().setItem(n, 1, y)
                if y1 < 0:
                    # ?????????????? 1.8: ?????????????? ?????????????????????????? ???????????????? ?? ??????????????
                    y.setBackground(QtGui.QColor('red'))
                elif y1 >= 0:
                    # ?????????????? 1.8: ?????????????? ?????????????????????????? ???????????????? ?? ??????????????
                    y.setBackground(QtGui.QColor('green'))
        z2 = np.array(z2)

        self.data = z2"""


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
