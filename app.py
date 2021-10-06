from PyQt5.QtWidgets import QMainWindow, QLineEdit
import sys
from PyQt5 import uic

from suvatcalculator import CalculateSuvatWindow
from velanglecalculator import CalculateVelAngleWindow
from login_screen import LoginScreen
from create_account_screen import CreateAccountScreen
from signin_screen import SigninScreen


class App(QMainWindow):
    def __init__(self):
        # run the initialisation of the QMainWindow
        super().__init__()
        # create and load the suvat entry window and show it
        # self.setup_suvat_svt_entry()
        # self.setup_vel_angle_entry()
        # self.setup_login_screen()
        self.setup_create_account_screen()
        self.show()

        # set up event handlers


    def setup_vel_angle_entry(self):
        self.calculate_velangle_window = CalculateVelAngleWindow(self)

    def setup_suvat_svt_entry(self):
        self.calculate_suvat_window = CalculateSuvatWindow(self)

    def setup_login_screen(self):
        self.login_screen = LoginScreen(self)

    def setup_create_account_screen(self):
        self.create_account_window = CreateAccountScreen(self)

    def setup_signin_screen(self):
        self.signin_window = SigninScreen(self)


