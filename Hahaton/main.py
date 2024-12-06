from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import sys
import sqlite3
import pandas as pd
import openpyxl
from CollectedMaterials import Ui_CollectedMaterials
from AddForm import Ui_AddForm
from Redaction import Ui_Redaction
from DelForm import Ui_DelForm
from SelNote import Ui_SelNote
from GraphForm import Ui_GraphForm
from graph import show_graph

database = sqlite3.connect('db')
db_cursor = database.cursor()


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

        self.table_load()
        self.tableView.setColumnWidth(0, 110)
        self.tableView.setColumnWidth(1, 110)
        self.tableView.setColumnWidth(2, 110)
        self.tableView.setColumnWidth(3, 110)
        self.tableView.setColumnWidth(4, 110)
        self.tableView.verticalHeader().setVisible(False)
        self.redButton.clicked.connect(self.open_red_w)
        self.exportButton.clicked.connect(self.export)
        self.graphButton.clicked.connect(self.create_graph)

    def open_red_w(self):
        self.red_w = Redaction()

    def table_load(self):
        cmdata = db_cursor.execute('SELECT * FROM table1').fetchall()
        data = pd.DataFrame(cmdata,
                            columns=['Номер записи', 'Дата добычи', 'Тип урана', 'Точка сбора',
                                     'Масса руды (т)', 'Масса чистого\nурана (г)'])
        self.model = TableModel(data)
        self.tableView.setModel(self.model)

    def export(self):
        query = 'SELECT * FROM table1'
        df = pd.read_sql(query, database)
        df.to_excel('Данные о добыче урана.xlsx')

    def create_graph(self):
        self.gform = GraphForm()


class AddForm(QtWidgets.QWidget, Ui_AddForm):
    def __init__(self, notenum=0, date=0, utype=0, place=0, mass=0, umass=0, is_redaction=False):
        super(AddForm, self).__init__()
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.show()

        self.okButton.clicked.connect(self.commit_note)
        self.cancelButton.clicked.connect(self.close)
        self.is_redaction = is_redaction
        if self.is_redaction:
            self.notenum = notenum
            _translate = QtCore.QCoreApplication.translate
            self.setWindowTitle(_translate("AddForm", "Форма изменения"))
            self.label.setText(_translate("AddForm", "Измените данные"))
            self.dateEdit.setText(date)
            self.typeEdit.setText(utype)
            self.placeEdit.setText(place)
            self.massEdit.setText(str(mass))
            self.umassEdit.setText(str(umass))

    def commit_note(self):
        if self.is_redaction:
            rep_data = [self.notenum, self.dateEdit.text(), self.typeEdit.text(), self.placeEdit.text(),
                        self.massEdit.text(), self.umassEdit.text()]
            db_cursor.execute('REPLACE INTO table1 VALUES (?, ?, ?, ?, ?, ?)', rep_data)
        else:
            try:
                id_num = db_cursor.execute('SELECT * FROM table1 ORDER BY "Номер записи" DESC LIMIT 1').fetchall()[0][0] + 1
            except:
                id_num = 0
            add_data = [id_num, self.dateEdit.text(), self.typeEdit.text(), self.placeEdit.text(),
                        self.massEdit.text(), self.umassEdit.text()]
            db_cursor.execute('INSERT INTO table1 VALUES (?, ?, ?, ?, ?, ?)', add_data)
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
        self.changeButton.clicked.connect(self.change_form)
        self.delButton.clicked.connect(self.delete_form)
        self.cancelButton.clicked.connect(self.close)

    def open_form(self):
        self.form = AddForm()

    def change_form(self):
        self.form = SelNote()

    def delete_form(self):
        self.form = DelForm()


class DelForm(QtWidgets.QWidget, Ui_DelForm):
    def __init__(self):
        super(DelForm, self).__init__()
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.show()
        self.delButton.clicked.connect(self.delete_note)
        self.cancelButton.clicked.connect(self.close)

    def delete_note(self):
        db_cursor.execute('DELETE FROM table1 WHERE "Номер записи" = ' + str(self.lineNum.text()))
        database.commit()
        window.table_load()
        self.close()


class SelNote(QtWidgets.QWidget, Ui_SelNote):
    def __init__(self):
        super(SelNote, self).__init__()
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.show()
        self.okButton.clicked.connect(self.redact_form)
        self.cancelButton.clicked.connect(self.close)

    def redact_form(self):
        seldata = db_cursor.execute('SELECT * FROM table1 WHERE "Номер записи" = ' +
                                    str(self.lineNum.text())).fetchall()[0]
        self.form = AddForm(seldata[0], seldata[1], seldata[2], seldata[3], seldata[4], seldata[5], True)
        self.close()


class GraphForm(QtWidgets.QWidget, Ui_GraphForm):
    def __init__(self):
        super(GraphForm, self).__init__()
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.show()
        self.graph1Button.clicked.connect(self.create_graph)
        self.cancelButton.clicked.connect(self.close)

    def create_graph(self):
        umass_list = db_cursor.execute('SELECT "Масса чистого урана (г)" FROM table1').fetchall()
        show_graph(umass_list)
        self.close()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
