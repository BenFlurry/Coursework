from functools import partial

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
        # set current screen to login
        self.current_screen = 'login'
        # load the login screen
        self.setup_login_screen()
        self.show()

    def popup_status(self, button_name):
        button_name = button_name.text()
        print(button_name)
        if self.current_screen == 'signin':
            if button_name == '&Yes':
                self.setup_teacher_landing()

        # todo add the other screens that require a popout button checking here
        elif self.current_screen == 'teacher landing':
            if button_name == '&Yes':
                self.setup_login_screen()

    # todo might have to pass in the dimensions of the previous window so window size is maintained through windows
    # set up event handlers
    def setup_signin_screen(self):
        self.current_screen = 'signin'
        self.login_screen.close()
        self.signin_screen = SigninScreen(self)
        self.signin_screen.box.buttonClicked.connect(self.popup_status)
        self.signin_screen.back.clicked.connect(self.setup_login_screen)

    def setup_login_screen(self):
        self.current_screen = 'login'
        self.login_screen = LoginScreen(self)
        self.login_screen.create_account.clicked.connect(self.setup_create_account_screen)
        self.login_screen.signin.clicked.connect(self.setup_signin_screen)

    def setup_create_account_screen(self):
        self.current_screen = 'create account'
        self.login_screen.close()
        self.create_account = CreateAccountScreen(self)
        self.create_account.back.clicked.connect(self.setup_login_screen)

    def setup_teacher_landing(self):
        self.current_screen = 'teacher landing'
        self.signin_screen.close()
        self.teacher_landing = TeacherLanding(self)
        self.teacher_landing.box.buttonClicked.connect(self.popup_status)

    # todo when loading the simulator, load both windows and have a toggle button which hides or shows the
    #  velangle/suvat windows
    def setup_vel_angle_entry(self):
        self.current_screen = 'velangle sim'
        self.calculate_velangle_window = CalculateVelAngleWindow(self)

    def setup_suvat_svt_entry(self):
        self.current_screen = 'suvat sim'
        self.calculate_suvat_window = CalculateSuvatWindow(self)
