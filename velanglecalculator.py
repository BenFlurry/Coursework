from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib import *

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
                       self.y_coord.text()]

    def calculate_values(self):
        # take pulled values
        self.pull_values()
        # check we can run the main function, create an array where 1 means value and 0 means missing value
        value_exists = []
        for i in range(len(self.values)):
            # if the value exists, append 1, else append 0
            if self.values[i] == '':
                value_exists.append(0)
            else:
                value_exists.append(1)
                self.values[i] = float(self.values[i])

        # unpack the list
        vel, ang, acc, sh, x, y = self.values

        if sh == '':
            sh = 0
            value_exists[3] = 1

        print(self.values)

        # if there are the correct permutations of values, run the main velangle function
        if value_exists == [1, 0, 1, 1, 1, 1] or value_exists == [1, 1, 1, 1, 0, 0]:
            graph_main_velangle(vel, ang, acc, sh, x, y)


'''
need to change the style of matplotlib graph
'''
