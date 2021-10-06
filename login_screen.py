from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib2 import *
from signin_screen import SigninScreen
from create_account_screen import CreateAccountScreen
ui = uic.loadUiType('login_screen.ui')[0]

'''
push button -> signin
push button -> create_account
'''


class LoginScreen(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)

        self.signin.clicked.connect(self.load_signin)
        self.create_account.clicked.connect(self.load_create_account)

    def load_signin(self):
        self.signin_window = SigninScreen(self)

    def load_create_account(self):
        self.create_account_window = CreateAccountScreen(self)
