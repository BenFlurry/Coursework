from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QStackedWidget
from PyQt5 import uic
from suvat_lib2 import *
from signin_screen import SigninScreen
from create_account_screen import CreateAccountScreen
import time
ui = uic.loadUiType('login_screen.ui')[0]

'''
push button -> signin
push button -> create_account
'''


class LoginScreen(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        # self.stack = QStackedWidget()
        self.setupUi(app_window)

        # self.signin.clicked.connect(self.load_signin)
        # self.create_account.clicked.connect(self.load_create_account)
        self.show()

    # def load_signin(self):
    #     self.signin_window = SigninScreen(self)
    #     self.close()
    #     self.show()


        # stack = QStackedWidget
        # stack.addWidget(signin_window.stackedWidget)
        # stack.setCurrentIndex(stack.currentIndex() +1)

    # def load_create_account(self):
    #     self.create_account_window = CreateAccountScreen(self)
    #     # self.show()
