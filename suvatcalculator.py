from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from suvat_lib import *
import sqlite3

ui = uic.loadUiType('suvatcalculator.ui')[0]


class CalculateSuvatWindow(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        # set up application
        self.setupUi(app_window)
        # run calculate function when button clicked
        self.calculate_btn.clicked.connect(self.calculate_values)
        self.conn = sqlite3.connect('database2.db', isolation_level=None)
        self.c = self.conn.cursor()

    def pull_values(self):
        # pull values from PyQt
        self.start_height = self.sh.text()
        self.values_suvat = [self.sy.text(), self.uy.text(), self.vy.text(), self.ay.text(), self.ty.text()]
        self.values_svt = [self.sx.text(), self.vx.text(), self.tx.text()]

    def calculate_values(self):
        # take pulled values
        self.pull_values()
        # iterate through values, if '', leave else change to integer
        for i in range(len(self.values_suvat)):
            if not self.values_suvat[i] == '':
                self.values_suvat[i] = int(self.values_suvat[i])

        for i in range(len(self.values_svt)):
            if not self.values_svt[i] == '':
                self.values_svt[i] = int(self.values_svt[i])

        if self.start_height != '':
            self.start_height = int(self.start_height)
        elif self.start_height == '':
            self.start_height = 0

        # make sure t values are the same
        ty = self.ty.text()
        tx = self.tx.text()
        if tx != '' and ty == '':
            self.values_suvat[4] = tx
        elif ty != '' and tx == '':
            self.values_svt[2] = ty

            # todo error messages in suvat

        # run the main function from suvat library
        graph_main_suvat(self.values_suvat, self.values_svt, self.start_height)

