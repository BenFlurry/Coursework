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

    def to_next_page(self, window_object, window_name):
        if window_name == 'login':
            window_object.create_account.clicked.connect(self.setup_create_account_screen)
            window_object.signin.clicked.connect(self.setup_signin_screen)

        elif window_name == 'create account':
            window_object.back.clicked.connect(self.setup_login_screen)

        elif window_name == 'signin':
            # todo need to make it so it only swaps screens if the password is valid
            # todo add another button which goes to the next page,
            window_object.to_teacher.clicked.connect(self.setup_teacher_landing)
            window_object.back.clicked.connect(self.setup_login_screen)

        elif window_name == 'teacher landing':
            window_object.logout.clicked.connect(self.setup_login_screen)

    def setup_login_screen(self):
        self.login_screen = LoginScreen(self)
        self.to_next_page(self.login_screen, 'login')

    def setup_create_account_screen(self):
        self.login_screen.close()
        self.create_account = CreateAccountScreen(self)
        self.to_next_page(self.create_account, 'create account')

    def setup_signin_screen(self):
        self.login_screen.close()
        self.signin_screen = SigninScreen(self)
        self.to_next_page(self.signin_screen, 'signin')

    def setup_teacher_landing(self):
        self.teacher_landing = TeacherLanding(self)
        self.signin_screen.close()
        self.to_next_page(self.teacher_landing, 'teacher landing')

    def setup_vel_angle_entry(self):
        self.calculate_velangle_window = CalculateVelAngleWindow(self)

    def setup_suvat_svt_entry(self):
        self.calculate_suvat_window = CalculateSuvatWindow(self)
