from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5 import uic
from suvat_lib import *
from email_validator import validate_email, EmailNotValidError
from signin_screen import SigninScreen
import string
# from error_popup import ErrorPopup
import sqlite3

ui = uic.loadUiType('landing_page.ui')[0]

'''
velange_flashcard -> push button
suvat_flashcard -> push button
practice_flashcards -> push button
to_simulator -> push button
table -> table
logouut -> push button
'''


class LandingPage(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)
