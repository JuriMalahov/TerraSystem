import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import sys
import sqlite3
import pandas as pd
from CollectedMaterials import Ui_CollectedMaterials

database = sqlite3.connect('db')
db_cursor = database.cursor()
#db_cursor.execute('INSERT INTO table1 VALUES (3, 1, "abc", 123)')
cmdata = db_cursor.execute('SELECT * FROM table1').fetchall()
#database.commit()
# print(db_cursor.execute('SELECT * FROM table1').fetchall()[1][2])

# print(db_cursor.execute('SELECT * FROM table1').fetchall())
# pyuic5 CollectedMaterials.ui -o CollectedMaterials.py


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data


    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow, Ui_CollectedMaterials):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setFixedSize(960, 540)

        data = pd.DataFrame(cmdata, columns=['Номер записи', 'Тип урана', 'Точка сбора', 'Масса собранного \nматериала (кг)'])
        self.model = TableModel(data)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 100)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
