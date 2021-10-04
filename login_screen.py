from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib2 import *
ui = uic.loadUiType('login_screen.ui')[0]

class LoginScreen(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)

        self.signin.clicked.connect(self.load_signin)
        self.create_account.clicked.connect(self.load_create_account)

    def load_signin(self):
        pass

    def load_create_account(self):
        pass
