from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib2 import *
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
