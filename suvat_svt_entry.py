from PyQt5.QtWidgets import QMainWindow, QLineEdit
import sys
from PyQt5 import uic

ui = uic.loadUiType('suvat_svt_entry.ui')[0]
class SuvatEntryWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi()


