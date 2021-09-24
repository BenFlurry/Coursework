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
        # y values
        sy = int(self.sy.text())
        uy = int(self.uy.text())
        vy = int(self.vy.text())
        ay = int(self.ay.text())
        ty = int(self.ty.text())
        suvat = [sy, uy, vy, ay, ty]
        # x values
        sx = int(self.sx.text())
        vx = int(self.vx.text())
        tx = int(self.tx.text())
        svt = [sx, vx, tx]
        # return valuables
        return suvat, svt

    def calculate_values(self):
        suvat, svt = self.pull_values()
        graph_main_suvat(suvat, svt)

