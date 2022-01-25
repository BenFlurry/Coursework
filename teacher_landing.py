from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox, QApplication
from PyQt5 import uic
from suvat_lib2 import *
import sqlite3
import hashlib
import sys
from data import Data
ui = uic.loadUiType('teacher_landing.ui')[0]

'''
push button -> set_homework
push button -> view_homework
push button -> manage_class
push button -> new_class
push button -> to_simulator
push button -> logout
push button -> save_changes
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

        self.label1.setHidden(True)
        self.input1.setHidden(True)
        self.input2.setHidden(True)
        self.save_changes.setHidden(True)
        self.state = ''
        self.show()

        self.creating_class = False
        self.editing_class = False

        self.conn = sqlite3.connect('database2.db', isolation_level=None)
        self.c = self.conn.cursor()

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



    def save(self):
        if self.creating_class:
            try:
                teacherid = 1
                # take the classname from pyqt
                classname = self.input1.text()
                # insert the class name with the teacher id into the classes table
                self.c.execute('INSERT INTO classes(classid, teacherid, classname) VALUES(null, ?, ?)', (teacherid, classname))
                print('executed')
                # hide the widgets which are no longer needed
                self.label1.setHidden(True)
                self.input1.setHidden(True)
                self.edit_class
            except sqlite3.IntegrityError as e:
                print(e)

        if self.editing_class:
            try:
                # take the inputted names
                names = self.input2.toPlainText()
                print(names)
                # create a list splitting the string of names at the new line char, then remove start and end whitespace
                names = [word.lstrip().rstrip() for word in names.split('\n')]
                print(names)
            except Exception as e:
                print(e)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = StudentLanding()
#     sys.exit(app.exec_())


