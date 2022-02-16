from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5 import uic
from suvat_lib2 import *
from email_validator import validate_email, EmailNotValidError
from signin_screen import SigninScreen
import string
# from error_popup import ErrorPopup
import sqlite3
import hashlib

ui = uic.loadUiType('create_account_screen.ui')[0]

'''
radio button -> student (mutually exclusive)
radio button -> teacher (mutually exclusive)
line edit -> email
line edit -> username
line edit -> password1
line edit -> password2
radio button -> show_password 
push button -> create_account
push button -> back
'''


class CreateAccountScreen(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)

        # hook up the buttons
        self.create_account.clicked.connect(self.validate_account)
        self.back.clicked.connect(self.load_signin)
        self.show_password.clicked.connect(self.toggle_password)
        self.details = {}
        self.conn = sqlite3.connect('database2.db', isolation_level=None)
        self.c = self.conn.cursor()
        # self.account_type = 'teacher'
        # self.student = False
        # self.teacher = False
        # self.email = ''\\\\\\\\
        # self.username = ''
        # self.password1 = ''
        # self.password2 = ''
        # self.valid_email = False
        # self.valid_password = False
        self.box = QMessageBox()
        self.box.setIcon(QMessageBox.Critical)

    def load_signin(self):
        pass

    # make sure that the account is valid
    def validate_account(self):
        # pull values from PyQt5
        self.student = self.qstudent.isChecked()
        self.teacher = self.qteacher.isChecked()
        self.email = self.qemail.text()
        self.username = self.qusername.text()
        self.password1 = self.qpassword1.text()
        self.password2 = self.qpassword2.text()
        self.name = self.qname.text()
        self.account_type = ''
        self.check_account_type()
        self.check_username()
        self.check_email()
        self.check_password()
        self.add_user()

    def check_account_type(self):
        if self.student:
            self.account_type = 'student'
        elif self.teacher:
            self.account_type = 'teacher'
        else:
            self.box.setWindowTitle('Error')
            self.box.setText('Select an account type')
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()
        self.details['account_type'] = self.account_type

    def check_email(self):
        try:
            valid = validate_email(self.email)
            # update with the normalized form
            self.email = valid.email
            print('valid email')
            self.details['email'] = self.email
        except EmailNotValidError as e:
            self.box.setWindowTitle('Error')
            self.box.setText('Invalid email')
            self.box.setInformativeText(str(e))
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()

    def check_username(self):
        self.details['username'] = self.username
        self.details['name'] = self.name

    def hash_password(self):
        self.password = hashlib.sha256(self.password1.encode()).hexdigest()
        print(self.password)

    def check_password(self):
        self.valid_password = False
        # check the 2 entered passwords are the same
        if self.password1 == self.password2:
            password = self.password1
            # check longer than 8 characters
            if len(password) >= 8:
                # check it has at least a special character
                if any(not letter.isalnum() and not letter.isspace() for letter in password):
                    # check it has at least a number
                    if any(letter.isdigit() for letter in password):
                        if any(letter.isupper() for letter in password):
                            self.valid_password = True
                            # hash the password using SHA hash
                            self.hash_password()
                            self.details['password'] = self.password
                        else:
                            error_message = 'password needs to have a capital letter'
                    else:
                        error_message = 'password needs to have a number'
                else:
                    error_message = 'password needs to have a special symbol'
            else:
                error_message = 'password has to be 8 or more characters'
        else:
            error_message = 'enter matching passwords'
        # display invalid password popout
        if not self.valid_password:
            self.box.setWindowTitle('Error')
            self.box.setText('Password error:')
            self.box.setIcon(QMessageBox.Critical)
            self.box.setInformativeText(error_message)
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()

    # when show_password button is pressed, run the function to change the password echo
    def toggle_password(self):
        if self.show_password.isChecked():
            self.qpassword1.setEchoMode(QLineEdit.EchoMode.Normal)
            self.qpassword2.setEchoMode(QLineEdit.EchoMode.Normal)

        else:
            self.qpassword1.setEchoMode(QLineEdit.EchoMode.Password)
            self.qpassword2.setEchoMode(QLineEdit.EchoMode.Password)

    def add_user(self):
        try:
            query = 'INSERT INTO users VALUES(null, :username, :email, ' \
                    ':password, :name)'
            print(self.details)
            self.c.execute(query, self.details)
            print('new user account created')
            # fetch the userid from the created account
            self.c.execute('SELECT userid FROM users WHERE username = ?', (self.details['username'],))
            userid = self.c.fetchall()[0][0]
            print(userid)
            if self.account_type == 'teacher':
                # and add to teachers table if a teacher
                self.c.execute('INSERT INTO teachers VALUES(null, ?)', (userid,))
            elif self.account_type == 'student':
                # and add to students table if a student
                # fixme didnt work for some reason
                self.c.execute('INSERT INTO students VALUES(null, ?, null)', (userid,))
            self.box.setWindowTitle('Error')
            self.box.setText('Continue to sign in')
            self.box.setIcon(QMessageBox.Information)
            self.box.setStandardButtons(QMessageBox.Yes)
            self.box.setDefaultButton(QMessageBox.Yes)
            self.box.exec()

        except sqlite3.IntegrityError as e:
            self.box.setWindowTitle('Error')
            self.box.setText('Your username or email already exists')
            self.box.setInformativeText(str(e))
            self.box.setIcon(QMessageBox.Critical)
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()
