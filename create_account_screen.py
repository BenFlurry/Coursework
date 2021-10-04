from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib2 import *
from email_validator import validate_email, EmailNotValidError
ui = uic.loadUiType('create_account_screen.ui')[0]
from signin_screen import SigninScreen

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

    def validate_account(self):
        # pull values from PyQt5
        self.student = self.student.isChecked()
        self.teacher = self.teacher.isChecked()
        self.email = self.email.text()
        self.username = self.username.text()
        self.password1 = self.password1.text()
        self.password2 = self.password2.text()

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
        # use string manipulation to make sure in correct form
        pass


    def load_signin(self):
        self.signin_window = SigninScreen(self)
