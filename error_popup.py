from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
ui = uic.loadUiType('error_popup.ui')[0]

'''
text edit -> error_message
'''

class ErrorPopup(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)
        self.error_message.setPlainText('')


    def set_error_message(self, error_message):
        self.error_message.setPlainText(error_message)
