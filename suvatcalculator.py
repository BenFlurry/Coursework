from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
import sys
from suvat_lib2 import *

ui = uic.loadUiType('suvatcalculator.ui')[0]

class CalculateSuvatWindow(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        # set up application
        self.setupUi(app_window)
        # run calculate function when button clicked
        self.calculate_btn.clicked.connect(self.calculate_values)

    def pull_values(self):
        # pull values from PyQt
        self.start_height = self.sh.text()
        self.values_suvat = [self.sy.text(), self.uy.text(), self.vy.text(), self.ay.text(), self.ty.text()]
        self.values_svt = [self.sx.text(), self.vx.text(), self.tx.text()]


    def calculate_values(self):
        # take pulled values
        self.pull_values()
        # run the main function from suvat library
        graph_main_suvat(self.values_suvat, self.values_svt, self.start_height)


