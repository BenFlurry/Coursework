from PyQt5.QtWidgets import QMainWindow, QHeaderView, QPushButton, QLineEdit, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from suvat_lib import *
from email_validator import validate_email, EmailNotValidError
from signin_screen import SigninScreen
import string
# from error_popup import ErrorPopup
import sqlite3
from data import data_dict
from dictionary_factory import *
from suvat_lib import *

ui = uic.loadUiType('practice_suvat_flashcards.ui')[0]

'''
check_correct -> push button
show_graph -> push button
suvat display -> labels
test code -> CNKQ
'''




class PracticeSuvatFlashcards(QMainWindow, ui):
    def __init__(self, appwindow):
        super().__init__()
        self.setupUi(appwindow)
        # initialise the popout box
        self.box = QMessageBox()
        self.box.setIcon(QMessageBox.Information)
        # add button handlers
        self.check_correct.clicked.connect(self.check_correct_clicked)
        self.show_graph.clicked.connect(self.show_graph_clicked)
        self.box.buttonClicked.connect(self.handle_popout)
        self.next_card.clicked.connect(self.next_card_clicked)
        self.prev_card.clicked.connect(self.prev_card_clicked)
        # connect to db
        self.conn = sqlite3.connect('database3.db', isolation_level=None)
        self.conn.row_factory = dict_factory
        self.c = self.conn.cursor()
        # set flashcard index to 0
        self.index = 0
        # make dict to convert form sql stored to displayable variable names
        self.check_var_dict = {'sy': 'Vertical Displacement',
                               'uy': 'Vertical Initial Velocity',
                               'vy': 'Vertical Final Velocity',
                               'ay': 'Vertical Acceleration',
                               't': 'Time',
                               'sx': 'Horizontal Displacement',
                               'vx': 'Horizontal Velocity'}
        # load flashcard values
        self.load_set()

    def load_set(self):
        print(f'{type(data_dict["setcode"]) = }')
        # pull values from db
        select = '''select flashcardid, name, setcode, setname
                        from flashcards
                        inner join sets 
                        on flashcards.setid = sets.setid
                        where sets.setcode = ?
                '''
        self.c.execute(select, (data_dict['setcode'],))
        self.flashcards_pulled = self.c.fetchall()
        self.set_name.setText(f'Set name: {self.flashcards_pulled[0]["setname"]}')
        self.set_code.setText(f'Set code: {self.flashcards_pulled[0]["setcode"]}')
        self.num_of_cards = len(self.flashcards_pulled)
        print(f'{len(self.flashcards_pulled) = }')
        print(f'{self.flashcards_pulled = }')
        self.load_values()

    def load_values(self):
        print(f'here {self.index = }')
        self.answer_input.setText('')
        self.error_message.setText('')
        select = '''select sy, uy, vy, ay, t, sx, vx, h, showgraph, checkvar, checkval1, checkval2
                from suvatcards
                where flashcardid = ?'''
        print(f'{self.flashcards_pulled[self.index] = }')
        self.c.execute(select, (self.flashcards_pulled[self.index]['flashcardid'],))
        flashcard = self.c.fetchall()[0]
        flashcard = list(flashcard.values())
        var_name = self.check_var_dict[flashcard[9]]
        self.target_variable.setText(f'Variable to find: {var_name}')
        print(f'{flashcard = }')
        self.flash = flashcard
        # convert to suvat, svt, h
        self.suvat = flashcard[0:5]
        self.svt = flashcard[5:7] + [flashcard[4]]
        # svt = flashcard[5:7]
        self.h = flashcard[7]
        self.target_var = flashcard[9]
        # output them to the user
        self.qsuvat = [self.sy, self.uy, self.vy, self.ay, self.ty]
        self.qsvt = [self.sx, self.vx, self.tx]
        self.qh = [self.height]
        for i in range(5):
            self.qsuvat[i].setText(self.suvat[i])
        for i in range(3):
            self.qsvt[i].setText(self.svt[i])

        self.height.setText(self.h)
        self.question_name.setText(f'Flashcard Name: {self.flashcards_pulled[self.index]["name"]}')

    def check_correct_clicked(self):
        check_value = self.answer_input.text()
        if ',' in check_value:
            check_value = list(check_value.split(','))

        if check_value != '':
            try:
                if type(check_value) == list:
                    if len(check_value) == 2:
                        check_value[0] = float(check_value[0])
                        check_value[1] = float(check_value[1])
                        check_value = tuple(check_value)
                    else:
                        self.error_message.setText('Enter 1 or 2 values')
                else:
                    check_value = float(check_value)
            except ValueError:
                self.error_message.setText('Enter a number for answer')

        else:
            self.error_message.setText('Enter a value')
        #
        # if type(check_value) == list:
        #     if self.flash[10] == check_value[0] and self.flash[11] == check_value[1]:
        #         verified = True, (self.flash[10], self.flash[11])
        #     elif self.flash[10] == check_value[1] and self.flash[11] == check_value[0]:
        #         correct = True, (self.flash[11], self.flash[10])
        #     else:
        #         correct = False, (self.flash[10], self.flash[11])
        # else:
        #     if self.flash[10] == check_value:
        #         correct = True, (check_value,)
        #     else:
        #         correct = False, (self.flash[10])
        #
        vars = self.suvat + self.svt
        for i in range(len(vars)):
            if vars[i] is None:
                vars[i] = ''
        self.suvat = vars[0:5]
        self.svt = vars[5:8]

        self.verified = verify_suvat(self.suvat, self.svt, self.h, self.target_var, check_value)
        print(f'{self.verified = }')
        print(f'{check_value = }')
        if len(self.verified[1]) == 2:
            self.answer = str(f'{self.verified[1][0]}, {self.verified[1][1]}')
        else:
            self.answer = str(self.verified[1][0])

        if self.verified[0] is True:
            self.box.setWindowTitle('Correct!')
            self.box.setText('Correct!')
            self.box.setInformativeText('')
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()
        else:
            self.box.setWindowTitle('Incorrect')
            self.box.setText('Incorrect')
            self.box.setInformativeText('Shall I tell you the answer?')
            self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.box.setDefaultButton(QMessageBox.No)
            self.box.exec()

    def handle_popout(self, button_name):
        button_name = button_name.text()
        if button_name == '&Yes':
            # they want to see the value -> show it in the text box
            print('here')
            self.answer_input.setText(self.answer)

    def show_graph_clicked(self):
        value = graph_main_suvat(self.suvat, self.svt, self.h)
        print(f'{value = }')
        if value != False:
            self.error_message.setText("Can't display graph")

    def next_card_clicked(self):
        if self.index <= self.num_of_cards - 2:
            self.index += 1
            print(f'{self.index = }')
            self.load_values()

    def prev_card_clicked(self):
        if self.index >= 1:
            self.index -= 1
            print(f'{self.index = }')
            self.load_values()
