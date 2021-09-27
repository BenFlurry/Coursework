from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib2 import *

ui = uic.loadUiType('velanglecalculator.ui')[0]


class CalculateVelAngleWindow(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        # setup UI
        self.setupUi(app_window)
        # run calculate function when button clicked
        self.calculate_btn.clicked.connect(self.calculate_values)

    def pull_values(self):
        # pull values from PyQt
        self.values = [self.velocity.text(),
                       self.angle.text(),
                       self.acceleration.text(),
                       self.start_height.text(),
                       self.x_coord.text(),
                       self.x_coord.text()]

    def calculate_values(self):
        # take pulled values
        self.pull_values()
        # check we can run the main function, create an array where 1 means value and 0 means missing value
        value_exists = []
        for value in self.values:
            # if the value exists, append 1, else append 0
            if value == '':
                value_exists.append(0)
            else:
                value_exists.append(1)

        # unpack the list
        vel, ang, acc, sh, x, y = self.values

        # if there are the correct permuations of values, run the main velangle function
        if value_exists == [0, 0, 0, 0, 1, 1] or value_exists == [1, 1, 1, 1, 0, 0]:
            graph_main_velangle(vel, ang, acc, sh, x, y)

'''
have it so values are int unless '' before entering into the library
'''
