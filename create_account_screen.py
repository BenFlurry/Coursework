from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib2 import *
from email_validator import validate_email, EmailNotValidError
from signin_screen import SigninScreen
import string

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

        self.create_account.clicked.connect(self.validate_account)
        self.back.clicked.connect(self.load_signin)
        self.account_type = 'teacher'
        self.student = False
        self.teacher = False
        self.email = ''
        self.username = ''
        self.password1 = ''
        self.password2 = ''
        self.valid_email = False
        self.valid_password = False

    def validate_account(self):
        # pull values from PyQt5
        self.student = self.inp_student.isChecked()
        self.teacher = self.inp_teacher.isChecked()
        self.email = self.inp_email.text()
        print('here')
        self.username = self.inp_username.text()
        self.password1 = self.inp_password1.text()
        self.password2 = self.inp_password2.text()

        print(f'student: {self.student}\n'
              f'teacher: {self.teacher}\n'
              f'email: {self.email}\n'
              f'username: {self.username}\n'
              f'password1: {self.password1}\n'
              f'password2: {self.password2}\n')

        self.check_account_type()
        self.check_username()
        self.check_email()
        self.check_password()
        # check what account type it is

    def check_account_type(self):
        if self.student:
            self.account_type == 'student'
        elif self.teacher:
            self.account_type == 'teacher'
        else:
            # create dialogue screen saying to select account
            pass

    def check_username(self):
        # query database and check username not taken
        pass

    def check_email(self):
        try:
            valid = validate_email(self.email)
            # update with the normalized form
            self.email = valid.email
        except EmailNotValidError as e:
            # need to create dialogue screen saying invalid email
            print(str(e))

    def check_password(self):
        # check the 2 entered passwords are the same
        if self.password1 == self.password2:
            password = self.password1
            # check longer than 8 characters
            if len(password) >= 8:
                # check it has at least a special character
                if any(not letter.isalnum() and not letter.isspace() for letter in password):
                    # check it has at least a number
                    if any(letter.isdigit() for letter in password):
                        self.valid_password = True
                        print('valid password')
                    else:
                        print('password needs to have a number')
                else:
                    print('password needs to have a special symbol')
            else:
                print('password has to be 8 or more characters')
        else:
            print('enter matching passwords')

    def load_signin(self):
        self.signin_window = SigninScreen(self)
