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
from suvat_flashcard import CreateSuvatFlashcard
from landing_page import LandingPage


class App(QMainWindow):
    def __init__(self):
        # run the initialisation of the QMainWindow
        super().__init__()
        # list of all the open screens, so when another screen is open the previous ones can be closed
        self.open_screens = []
        # set current screen to login

        # load the login screen
        # self.setup_teacher_landing()
        # self.setup_suvat_svt_entry()
        # self.setup_login_screen()
        self.setup_landing_page()
        # self.setup_create_suvat_flashcard()
        self.show()

    def popup_status(self, button_name):
        button_name = button_name.text()
        print(button_name)
        if self.current_screen == 'signin':
            if button_name == '&Yes':
                self.setup_teacher_landing()

        elif self.current_screen == 'teacher landing':
            if button_name == '&Yes':
                self.setup_login_screen()

        elif self.current_screen == 'create account':
            if button_name == '&Yes':
                self.setup_signin_screen()

    # closes any currently opened screens
    def close_screens(self):
        for i in range(len(self.open_screens)):
            self.open_screens[i].close()
            self.open_screens.pop(i)

    # set up event handlers
    def setup_signin_screen(self):
        self.current_screen = 'signin'
        self.close_screens()
        self.signin_screen = SigninScreen(self)
        self.open_screens.append(self.signin_screen)
        self.signin_screen.box.buttonClicked.connect(self.popup_status)
        self.signin_screen.back.clicked.connect(self.setup_login_screen)

    def setup_login_screen(self):
        self.current_screen = 'login'
        self.login_screen = LoginScreen(self)
        # open and close screens
        self.close_screens()
        self.open_screens.append(self.login_screen)
        # add button handlers
        self.login_screen.create_account.clicked.connect(self.setup_create_account_screen)
        self.login_screen.signin.clicked.connect(self.setup_signin_screen)

    def setup_create_account_screen(self):
        self.current_screen = 'create account'
        self.create_account = CreateAccountScreen(self)
        # open and close screens
        self.close_screens()
        self.open_screens.append(self.create_account)
        # add button handlers
        self.create_account.back.clicked.connect(self.setup_login_screen)
        self.create_account.box.buttonClicked.connect(self.popup_status)

    def setup_teacher_landing(self):
        self.current_screen = 'teacher landing'
        self.teacher_landing = TeacherLanding(self)
        # open and close screens
        self.close_screens()
        self.open_screens.append(self.teacher_landing)
        # add button handlers
        self.teacher_landing.box.buttonClicked.connect(self.popup_status)
        self.teacher_landing.to_simulator.clicked.connect(self.setup_vel_angle_entry)

    def setup_vel_angle_entry(self):
        self.current_screen = 'velangle sim'
        self.velangle_window = CalculateVelAngleWindow(self)
        # open and close screens
        self.close_screens()
        self.open_screens.append(self.velangle_window)
        # add button handlers
        self.velangle_window.back.clicked.connect(self.setup_landing_page)
        self.velangle_window.to_suvat.clicked.connect(self.setup_suvat_svt_entry)

    def setup_suvat_svt_entry(self):
        self.current_screen = 'suvat sim'
        self.suvat_window = CalculateSuvatWindow(self)
        # open screens
        self.close_screens()
        self.open_screens.append(self.suvat_window)
        # add button handlers
        self.suvat_window.back.clicked.connect(self.setup_landing_page)
        self.suvat_window.to_velangle.clicked.connect(self.setup_vel_angle_entry)

    def setup_landing_page(self):
        self.current_screen = 'landing'
        self.landing_page = LandingPage(self)
        self.close_screens()
        self.open_screens.append(self.landing_page)
        self.landing_page.suvat_flashcard.clicked.connect(self.setup_create_suvat_flashcard)
        self.landing_page.logout.clicked.connect(self.setup_login_screen)
        self.landing_page.to_simulator.clicked.connect(self.setup_suvat_svt_entry)

    def setup_create_suvat_flashcard(self):
        self.current_screen = 'create suvat flashcard'
        self.create_suvat_flashcard = CreateSuvatFlashcard(self)
        self.close_screens()
        self.open_screens.append(self.create_suvat_flashcard)
        self.create_suvat_flashcard.back.clicked.connect(self.setup_landing_page)



