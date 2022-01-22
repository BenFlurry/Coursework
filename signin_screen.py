from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib2 import *
import sqlite3
import hashlib
ui = uic.loadUiType('signin_screen.ui')[0]

'''
radio button -> student (mutually exclusive)
radio button -> teacher (mutually exclusive)
line edit -> username
line edit -> password
push button -> sign_in
push button -> back
'''


class SigninScreen(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)

        self.sign_in.clicked.connect(self.signin)
        self.conn = sqlite3.connect('database.db', isolation_level=None)
        self.c = self.conn.cursor()
        self.valid = False

    def signin(self):
        if self.student.isChecked():
            self.account_type = 'student'
        elif self.teacher.isChecked():
            self.account_type = 'teacher'
        else:
            pass
            # popup saying select account
        self.un = self.username.text()
        self.pw = self.password.text()

        self.check_un_pw()

    def check_un_pw(self):
        # first we have to hash the password
        self.pw = hashlib.sha256(self.password1.encode()).hexdigest()
        query = 'SELECT username, password FROM users WHERE username = ? and password = ?'
        self.c.execute(query, (self.un, self.pw))
        sql_return = self.c.fetchall()
        if sql_return:
            pass





