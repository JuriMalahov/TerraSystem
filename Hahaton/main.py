import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import sys
import sqlite3
import pandas as pd
from CollectedMaterials import Ui_CollectedMaterials
from AddForm import Ui_AddForm
from Redaction import Ui_Redaction

database = sqlite3.connect('db')
db_cursor = database.cursor()
#db_cursor.execute('INSERT INTO table1 VALUES (3, 1, "abc", 123)')
#cmdata = db_cursor.execute('SELECT * FROM table1').fetchall()
#database.commit()
# print(db_cursor.execute('SELECT * FROM table1').fetchall()[1][2])
#try:
#    print(db_cursor.execute('SELECT * FROM table1 ORDER BY "Номер записи" DESC LIMIT 1').fetchall()[0][0])
#except:
#    print(0)
# print(db_cursor.execute('SELECT * FROM table1').fetchall())
# pyuic5 CollectedMaterials.ui -o CollectedMaterials.py
# pyuic5 AddForm.ui -o AddForm.py
# pyuic5 Redaction.ui -o Redaction.py


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

        #data = pd.DataFrame(cmdata, columns=['Номер записи', 'Тип урана', 'Точка сбора', 'Масса собранного \nматериала (кг)'])
        #self.model = TableModel(data)
        #self.tableView.setModel(self.model)
        self.table_load()
        self.tableView.setColumnWidth(0, 110)
        self.tableView.setColumnWidth(1, 110)
        self.tableView.setColumnWidth(2, 110)
        self.tableView.setColumnWidth(3, 149)
        self.tableView.verticalHeader().setVisible(False)
        self.redButton.clicked.connect(self.open_red_w)

    def open_red_w(self):
        self.red_w = Redaction()

    def table_load(self):
        cmdata = db_cursor.execute('SELECT * FROM table1').fetchall()
        data = pd.DataFrame(cmdata,
                            columns=['Номер записи', 'Тип урана', 'Точка сбора', 'Масса собранного \nматериала (кг)'])
        self.model = TableModel(data)
        self.tableView.setModel(self.model)


class AddForm(QtWidgets.QWidget, Ui_AddForm):
    def __init__(self):
        super(AddForm, self).__init__()
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.show()

        self.okButton.clicked.connect(self.commit_note)
        self.cancelButton.clicked.connect(self.close)

    def commit_note(self):
        try:
            id_num = db_cursor.execute('SELECT * FROM table1 ORDER BY "Номер записи" DESC LIMIT 1').fetchall()[0][0] + 1
        except:
            id_num = 0
        add_data = [id_num, self.typeEdit.text(), self.placeEdit.text(), self.massEdit.text()]
        db_cursor.execute('INSERT INTO table1 VALUES (?, ?, ?, ?)', add_data)
        database.commit()
        window.table_load()
        self.close()


class Redaction(QtWidgets.QWidget, Ui_Redaction):
    def __init__(self):
        super(Redaction, self).__init__()
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.show()
        self.addButton.clicked.connect(self.open_form)
        self.cancelButton.clicked.connect(self.close)

    def open_form(self):
        self.form = AddForm()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
