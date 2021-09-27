from PyQt5.QtWidgets import QMainWindow, QLineEdit
import sys
from PyQt5 import uic

from suvatcalculator import CalculateSuvatWindow


class App(QMainWindow):
    def __init__(self):
        # run the initialisation of the QMainWindow
        super().__init__()
        # create and load the suvat entry window and show it
        self.setup_suvat_svt_entry()
        self.show()

        # set up event handlers

    def setup_suvat_svt_entry(self):
        self.calculate_suvat_window = CalculateSuvatWindow(self)

