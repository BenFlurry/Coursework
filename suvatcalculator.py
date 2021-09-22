from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
import sys

ui = uic.loadUiType('suvatcalculator.ui')[0]

class CalculateSuvatWindow(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        # set up application
        self.setupUi(app_window)





