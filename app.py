from PyQt5.QtWidgets import QMainWindow, QLineEdit, QStackedWidget
import sys
from PyQt5 import uic
from teacher_landing import TeacherLanding
from suvatcalculator import CalculateSuvatWindow
from velanglecalculator import CalculateVelAngleWindow
from login_screen import LoginScreen
from signin_screen import SigninScreen
from create_account_screen import CreateAccountScreen


class App(QMainWindow):
    def __init__(self):
        # run the initialisation of the QMainWindow
        super().__init__()
        # create and load the suvat entry window and show it
        # self.setup_suvat_svt_entry()
        # self.setup_vel_angle_entry()
        self.setup_login_screen()
        # self.setup_teacher_landing()
        self.show()

        # set up event handlers

    # todo get this sorted copying jackson
    # todo based off of the input window name, add the handlers for that window using if statements
    def to_next_page(self, window):
        window.create_account.clicked.connect(self.setup_create_account_screen)
        window.signin.clicked.connect(self.setup_login_screen)

    def setup_login_screen(self):
        self.login_screen = LoginScreen(self)
        self.to_next_page(self.login_screen)

    def setup_create_account_screen(self):
        self.login_screen.close()
        self.create_account = CreateAccountScreen(self)


    def setup_signin_screen(self):
        self.login_screen.close()
        self.signin_screen = SigninScreen(self)

    def setup_teacher_landing(self):
        self.teacher_landing = TeacherLanding(self)

    def setup_vel_angle_entry(self):
        self.calculate_velangle_window = CalculateVelAngleWindow(self)

    def setup_suvat_svt_entry(self):
        self.calculate_suvat_window = CalculateSuvatWindow(self)
