from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox, QApplication, QTableWidgetItem
from PyQt5 import uic, QtWidgets
from suvat_lib2 import *
import sqlite3
import hashlib
import sys
from data import Data
from dictionary_factory import *
ui = uic.loadUiType('teacher_landing.ui')[0]

'''
push button -> set_homework
push button -> view_homework
push button -> manage_class
push button -> new_class
push button -> to_simulator
push button -> logout
push button -> save_changes
push button -> delete_class
push button -> view_class
table -> table
line edit -> input1
plain text edit -> input2
label -> label1
'''

class TeacherLanding(QMainWindow, ui):
    def __init__(self, app):
        super().__init__()
        self.setupUi(app)
        # self.set_homework.clicked.connect()
        # self.view_homework.clicked.connect()
        self.manage_class.clicked.connect(self.edit_class)
        self.new_class.clicked.connect(self.create_new_class)
        # self.to_simulator.clicked.connect()
        # self.logout.clicked.connect()
        self.save_changes.clicked.connect(self.save)
        self.view_class.clicked.connect(self.show_class)

        self.label1.setHidden(True)
        self.input1.setHidden(True)
        self.input2.setHidden(True)
        self.save_changes.setHidden(True)
        self.view_class.setHidden(True)
        self.delete_class.setHidden(True)
        self.state = ''
        self.show()

        self.classname = ''

        self.creating_class = False
        self.editing_class = False

        self.conn = sqlite3.connect('database2.db', isolation_level=None)
        self.conn.row_factory = dict_factory
        self.c = self.conn.cursor()
        self.load_table()

        self.data = Data()

    def create_new_class(self):
        self.creating_class = True
        self.label1.setText('enter class name: ')
        self.label1.setHidden(False)
        self.input1.setHidden(False)
        self.save_changes.setText('Create Class')
        self.save_changes.setHidden(False)

    def edit_class(self):
        self.editing_class = True
        self.label1.setText("enter each student name on a new line")
        self.label1.setHidden(False)
        self.input2.setHidden(False)
        self.save_changes.setHidden(False)
        self.save_changes.setText('Add students to class')
        self.view_class.setHidden(False)
        self.delete_class.setHidden(False)

    def load_table(self):
        # selects everything in the database
        select = 'SELECT * FROM classes'
        self.c.execute(select)
        rows = self.c.fetchall()
        # add the headings
        headings = ["classid", "teacherid", "classname"]
        # clear the pyqt table
        self.table.clear()
        # find the dimensions of the table
        self.table.setColumnCount(len(headings))
        self.table.setRowCount(len(rows))
        # set up the headings of the table
        self.table.setHorizontalHeaderLabels(headings)

        # iterating through the python table rows
        for rownum, row in enumerate(rows):
            # need to convert row from tuple to dictionary to work
            for colnum, (col, value) in enumerate(row.items()):
                qtwi = QTableWidgetItem(str(value))
                self.table.setItem(rownum, colnum, qtwi)

    def show_class(self):
        rows = [index.row() for index in self.table.selectedIndexes()]
        # take the classid value in the table from the selected rows
        classid = int(self.table.item(int(rows[0]), 0).text())
        print(f'{classid = }')
        select = 'SELECT name, username, email FROM users INNER JOIN students ON users.userid = students.userid WHERE classid = ?'
        self.c.execute(select, (classid,))
        rows = self.c.fetchall()
        # add the headings
        headings = ["name", "username", "email"]
        # clear the pyqt table
        self.table.clear()
        # find the dimensions of the table
        self.table.setColumnCount(len(headings))
        self.table.setRowCount(len(rows))
        # set up the headings of the table
        self.table.setHorizontalHeaderLabels(headings)

        # iterating through the python table rows
        for rownum, row in enumerate(rows):
            # need to convert row from tuple to dictionary to work
            for colnum, (col, value) in enumerate(row.items()):
                qtwi = QTableWidgetItem(str(value))
                self.table.setItem(rownum, colnum, qtwi)

    def class_creation(self):
        try:
            teacherid = self.data.get_teacherid()
            # take the classname from pyqt
            # take a selection of the class which is highlighted on the table widget
            self.classname = self.input1.text()
            # insert the class name with the teacher id into the classes table
            self.c.execute('INSERT INTO classes(classid, teacherid, classname) VALUES(null, ?, ?)',
                           (teacherid, self.classname))
            print('executed')
            # hide the widgets which are no longer needed
            self.label1.setHidden(True)
            self.input1.setHidden(True)
            self.edit_class()
        except Exception as e:
            print(e)

    def class_editing(self):
        try:
            # take the inputted names
            names = self.input2.toPlainText()
            # create a list splitting the string of names at the new line char, then remove start and end whitespace
            names = [word.lstrip().rstrip() for word in names.split('\n')]

            # pull the indexes of the selected rows in the pyqt table
            rows = [index.row() for index in self.table.selectedIndexes()]
            # take the classid value in the table from the selected rows
            classid = int(self.table.item(int(rows[0]), 0).text())

            # for each name being added to the class
            for name in names:
                # find their userid from the users table corresponding to their name
                self.c.execute('SELECT userid FROM users WHERE name = ?', (name,))
                uid = self.c.fetchall()[0]
                # take the userid out of the dictionary
                userid = uid['userid']
                print(f'{userid = }, {type(userid)}')
                # update the students table adding their class
                self.c.execute('UPDATE students SET classid = ? WHERE userid = ?', (classid, userid))

        except Exception as e:
            print(e)

    def save(self):
        if self.creating_class:
            self.class_creation()

        if self.editing_class:
            self.class_editing()



