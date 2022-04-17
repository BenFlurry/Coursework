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
import random

ui = uic.loadUiType('landing_page.ui')[0]

'''
velange_flashcard -> push button
suvat_flashcard -> push button
practice_flashcards -> push button
to_simulator -> push button
table -> table
logout -> push button
'''


class LandingPage(QMainWindow, ui):
    def __init__(self, app_window):
        super().__init__()
        self.setupUi(app_window)
        name = data_dict['name']
        name = name.split()[0]
        # name = 'Anshul'
        self.userid = data_dict['userid']
        # self.userid = 2
        self.welcome_label.setText(f'Welcome, {name}!')
        # connect to db
        self.conn = sqlite3.connect('database3.db', isolation_level=None)
        self.conn.row_factory = dict_factory
        self.c = self.conn.cursor()

        # add button handlers
        self.create_new_set.clicked.connect(self.create_new_set_clicked)
        self.edit_set.clicked.connect(self.edit_set_clicked)
        self.add_set.clicked.connect(self.add_new_set)
        self.search.clicked.connect(self.search_clicked)
        self.delete_button.clicked.connect(self.delete_clicked)
        self.load_sets_button.clicked.connect(self.load_sets)
        self.search_set_by_code.clicked.connect(self.search_set_by_code_clicked)
        self.practice_flashcards.clicked.connect(self.practice_flashcards_clicked)
        # load the sets
        self.load_sets()

        self.delete_type = 'sets'

        self.status = 'viewing sets'
        self.handle_buttons()
        self.error_message.setText('')

        self.set_doesnt_exist = True


    def practice_flashcards_clicked(self):
        # pull values from table
        rows = [index.row() for index in self.table.selectedIndexes()]
        rows = list(dict.fromkeys(rows))
        if len(rows) != 1:
            self.error_message.setText('Select 1 set of flashcards to practice at a time')
        else:
            setcode = self.table.item(int(rows[0]), 0).text()
            data_dict['setcode'] = setcode

    def search_set_by_code_clicked(self):
        if not self.set_doesnt_exist:
            self.error_message.setText('')

        self.status = 'entering code'
        self.handle_buttons()

    def delete_clicked(self):
        if self.delete_type == 'sets':
            rows = [index.row() for index in self.table.selectedIndexes()]
            # get rid of duplicate row indexes
            rows = list(dict.fromkeys(rows))
            print(f'{rows = }')
            # and add them to the list of students to be deleted
            for i in range(len(rows)):
                setcode = self.table.item(int(rows[i]), 0).text()

                self.c.execute('SELECT userid FROM sets WHERE setcode = ?', (setcode,))
                # if the owner of the set is the current user of the program allow deletion
                if data_dict['userid'] == self.c.fetchall()[0]['userid']:
                    self.c.execute('DELETE FROM sets WHERE setcode = ?', (setcode,))
                else:
                    self.error_message.setText("You can't edit a set that isn'y yours")

            # reload the table
            self.load_sets()

        elif self.delete_type == 'flashcards':
            rows = [index.row() for index in self.table.selectedIndexes()]
            # get rid of duplicate row indexes
            rows = list(dict.fromkeys(rows))
            print(f'{rows = }')
            # and add them to the list of students to be deleted
            for i in range(len(rows)):
                name = self.table.item(int(rows[i]), 0).text()
                self.c.execute('SELECT flashcardid, setid FROM flashcards WHERE name = ?', (name,))
                # check if the owner of the set is the one editing
                fetch = self.c.fetchall()[0]
                id = fetch['flashcardid']
                sid = fetch['setid']
                self.c.execute('SELECT userid FROM sets WHERE setid = ?', (sid,))
                if data_dict['userid'] == self.c.fetchall()[0]['userid']:
                    self.c.execute('DELETE FROM flashcards WHERE flashcardid = ?', (id,))
                else:
                    self.error_message.setText('Cannot edit a set that isnt yours')
            # reload the table
            self.userid = data_dict['userid']
            self.setid = sid
            self.load_flashcards()

    def search_clicked(self):
        self.error_message.setText('')
        self.delete_type = 'invalid'
        inp = self.input_line.text()
        valid = True
        if len(inp) != 4 or not inp.isupper():
            self.error_message.setText('Code has to be 4 uppercase letters')
            valid = False

        if inp and valid:
            self.status = 'using code'
            select = '''SELECT setcode, setname, username, name
                            FROM sets
                            INNER JOIN users
                            ON users.userid = sets.userid
                            WHERE setcode = ?'''
            self.c.execute(select, (inp,))
            rows = self.c.fetchall()
            if len(rows) == 0:
                self.set_doesnt_exist = True
                self.error_message.setText("A set doesn't exist with this code")
                self.search_set_by_code_clicked()
            else:
                # headings = ['Set Code', 'Set Name', 'Number Of Flashcards']
                headings = ['Set Code', 'Set Name', 'Username', 'Name']
                # load table
                self.load_table(headings, rows)
        elif not inp:
            self.status = 'viewing sets'
            self.load_sets()

        self.handle_buttons()
        self.input_line.setText('')


    def create_new_set_clicked(self):
        self.status = 'creating set'
        self.error_message.setText('')

        self.handle_buttons()

    def add_new_set(self):
        inp_set = self.input_line.text()
        if inp_set:
            # make a random 4 letter code
            code = ''.join([random.choice(string.ascii_uppercase) for _ in range(4)])
            insert = '''INSERT INTO sets
                    VALUES (null, ?, ?, ?)'''
            self.c.execute(insert, (code, inp_set, self.userid))
            self.load_sets()
        else:
            self.error_message.setText('Enter a name for the set')

    def load_flashcards(self):
        select = '''SELECT flashcardid, name, cardtype
                    FROM flashcards
                    WHERE setid = ?'''
        self.c.execute(select, (self.setid,))
        rows = self.c.fetchall()
        headings = ['Flashcard ID', 'Name of Card', 'Card Type']
        # load table
        self.load_table(headings, rows)

    def load_sets(self):
        self.error_message.setText('')

        # select = '''SELECT sets.setcode, sets.setname, count(*)
        #         FROM sets
        #         INNER JOIN flashcards
        #         ON flashcards.setid = sets.setid
        #         WHERE sets.userid = ?
        #         GROUP BY sets.setid'''
        self.status = 'viewing sets'
        self.delete_type = 'sets'

        select = '''SELECT setcode, setname
                FROM sets
                WHERE userid = ?'''
        self.c.execute(select, (self.userid,))
        rows = self.c.fetchall()

        # headings = ['Set Code', 'Set Name', 'Number Of Flashcards']
        headings = ['Set Code', 'Set Name']
        # load table
        self.load_table(headings, rows)
        self.handle_buttons()



    def load_table(self, headings, rows):
        # clear the pyqt table
        self.table.clear()
        # find the dimensions of the table
        self.table.setColumnCount(len(headings))
        self.table.setRowCount(len(rows))
        # set up the headings of the table
        self.table.setHorizontalHeaderLabels(headings)

        # iterating through the python table rows
        for rownum, row in enumerate(rows):
            # and columns, loading the table cell by cell
            for colnum, (col, value) in enumerate(row.items()):
                qtwi = QTableWidgetItem(str(value))
                self.table.setItem(rownum, colnum, qtwi)

        header = self.table.horizontalHeader()
        for i in range(len(headings)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def edit_set_clicked(self):
        self.delete_type = 'flashcard'
        self.error_message.setText('')
        rows = [index.row() for index in self.table.selectedIndexes()]
        # get rid of duplicate row indexes
        rows = list(dict.fromkeys(rows))
        if len(rows) != 1:
            self.error_message.setText('Select 1 flashcard set to view')

        else:
            rows = self.table.item(rows[0], 0).text()
            data_dict['setcode'] = rows
            print(f'{rows =}')
            try:
                select = '''SELECT flashcards.name, sets.setname, flashcards.cardtype
                        FROM flashcards
                        INNER JOIN sets
                        ON flashcards.setid = sets.setid
                        WHERE setcode = ?'''
                self.c.execute(select, (rows,))
                selected_rows = self.c.fetchall()
                print(f'{selected_rows = }')
                headings = ['Flashcard Name', 'Set Name', 'Card Type']
                self.load_table(headings, selected_rows)
                self.delete_type = 'flashcards'
                self.c.execute('SELECT setid FROM sets WHERE setcode = ?', (rows,))
                data_dict['setid'] = self.c.fetchall()[0]['setid']
                print(f'{data_dict = }')
                if self.status != 'using code':
                    self.status = 'viewing flashcards'

            except sqlite3.IntegrityError:
                self.error_message.setText('Issue with database')
        self.handle_buttons()

    '''
    velangle_flashcard
    suvat_flashcard
    practice_flashcards
    load_sets_button
    create_new_set
    edit_set
    search_set_by_code
    input_line
    search
    add_set
    delete_button
    to_simulator
    '''
    def handle_buttons(self):
        # triggered when loading sets
        if self.status == 'viewing sets':
            self.suvat_flashcard.setEnabled(False)
            self.velangle_flashcard.setEnabled(False)
            self.practice_flashcards.setEnabled(True)
            self.load_sets_button.setEnabled(True)
            self.create_new_set.setEnabled(True)
            self.edit_set.setEnabled(True)
            self.search_set_by_code.setEnabled(True)
            self.input_line.setHidden(True)
            self.search.setHidden(True)
            self.add_set.setHidden(True)
            self.delete_button.setEnabled(True)

        # set when edit is clicked but search by code is not
        elif self.status == 'viewing flashcards':
            self.suvat_flashcard.setEnabled(True)
            self.velangle_flashcard.setEnabled(True)
            self.practice_flashcards.setEnabled(True)
            self.load_sets_button.setEnabled(True)
            self.create_new_set.setEnabled(False)
            self.edit_set.setEnabled(False)
            self.search_set_by_code.setEnabled(False)
            self.input_line.setHidden(True)
            self.search.setHidden(True)
            self.add_set.setHidden(True)
            self.delete_button.setEnabled(True)

        # triggered when search set by code is clicked
        elif self.status == 'entering code':
            self.suvat_flashcard.setEnabled(False)
            self.velangle_flashcard.setEnabled(False)
            self.practice_flashcards.setEnabled(True)
            self.load_sets_button.setEnabled(True)
            self.create_new_set.setEnabled(False)
            self.edit_set.setEnabled(False)
            self.search_set_by_code.setEnabled(True)
            self.input_line.setHidden(False)
            self.search.setHidden(False)
            self.add_set.setHidden(True)
            self.delete_button.setEnabled(False)

        # triggered when search button is clicked
        elif self.status == 'using code':
            self.suvat_flashcard.setEnabled(False)
            self.velangle_flashcard.setEnabled(False)
            self.practice_flashcards.setEnabled(True)
            self.load_sets_button.setEnabled(True)
            self.create_new_set.setEnabled(False)
            self.edit_set.setEnabled(True)
            self.search_set_by_code.setEnabled(True)
            self.input_line.setHidden(False)
            self.search.setHidden(False)
            self.add_set.setHidden(True)
            self.delete_button.setEnabled(False)

        # triggered when create new set is clicked
        elif self.status == 'creating set':
            self.suvat_flashcard.setEnabled(False)
            self.velangle_flashcard.setEnabled(False)
            self.practice_flashcards.setEnabled(False)
            self.load_sets_button.setEnabled(True)
            self.create_new_set.setEnabled(False)
            self.edit_set.setEnabled(False)
            self.search_set_by_code.setEnabled(True)
            self.input_line.setHidden(False)
            self.search.setHidden(True)
            self.add_set.setHidden(False)
            self.delete_button.setEnabled(False)

    # todo have error message be hidden when a new button has been clicked




