from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5 import uic
from suvat_lib2 import *
import sqlite3
import hashlib
ui = uic.loadUiType('signin_screen.ui')[0]

'''
radio button -> student (mutually exclusive)
radio button -> teacher (mutually exclusive)
radio button -> guest (mutually exclusive)
line edit -> username
line edit -> password
push button -> sign_in
push button -> back
radio button -> show_password
'''


class SigninScreen(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)

        self.sign_in.clicked.connect(self.signin)
        self.show_password.clicked.connect(self.toggle_password)
        self.conn = sqlite3.connect('database.db', isolation_level=None)
        self.c = self.conn.cursor()
        self.valid = False

        self.box = QMessageBox()

    def signin(self):
        if self.student.isChecked():
            self.account_type = 'student'
        elif self.teacher.isChecked():
            self.account_type = 'teacher'
        elif self.guest.isChecked():
            self.account_type = 'guest'
        else:
            self.box.setWindowTitle('Error')
            self.box.setText('Select an account type')
            self.box.setIcon(QMessageBox.Critical)
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()
            # popup saying select an account
        self.un = self.username.text()
        self.pw = self.password.text()
        print(f'{self.account_type=}\n'
              f'{self.un=}\n'
              f'{self.pw=}')
        self.check_un_pw()

    def check_un_pw(self):
        # first check if there is a matching email or password in the database
        self.c.execute('SELECT * FROM users WHERE username = ? or email = ?', (self.un, self.un))
        user = self.c.fetchall()
        print(user)
        self.box.setIcon(QMessageBox.Critical)
        # if the email doesnt exist, then the account username and email is incorrect
        if len(user) != 0:
            user = user[0]
            # to check the password, we need to first hash it
            self.pw = hashlib.sha256(self.pw.encode()).hexdigest()
            # check if the password is correct
            if self.pw == user[3]:
                if self.account_type == user[4]:
                    msg = 'Valid account, welcome to the program'
                    self.box.setIcon(QMessageBox.Information)
                else:
                    msg = 'The user does not exist for this account type'
            else:
                msg = 'Invalid password'
        else:
            msg = 'Invalid username or email'
        print(msg)
        self.box.setWindowTitle('Error')
        self.box.setText(msg)
        self.box.setIcon(QMessageBox.Critical)
        self.box.setStandardButtons(QMessageBox.Ok)
        self.box.setDefaultButton(QMessageBox.Ok)
        self.box.exec()

    def toggle_password(self):
        if self.show_password.isChecked():
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)




