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
        # name = data_dict['name']
        # name = name.split()[0]
        name = 'Ben'
        # self.userid = data_dict['userid']
        self.userid = 1
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
        # load the sets
        self.load_sets()

        self.delete_type = 'invalid'

        self.status = 'viewing sets'
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
                    self.c.execute('DELETE FROM sets WHERE setname = ?', (setcode,))
                else:
                    self.error_message.setText("You can't edit a set that isn'y yours")

            # reload the table
            select = 'SELECT setid FROM sets WHERE setname = ?'
            self.c.execute(select, (setcode,))
            self.setid = self.c.fetchall()[0][0]
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

                id = self.c.fetchall()[0]['flashcardid']
                setid = id['setid']
                self.c.execute('SELECT userid FROM sets WHERE setid = ?', (setid,))
                if data_dict['userid'] == self.c.fetchall()[0]['userid']:
                    self.c.execute('DELETE FROM flashcards WHERE flashcardid = ?', (id,))
                else:
                    self.error_message.setText('Cannot edit a set that isnt yours')
            # reload the table
            self.userid = data_dict['userid']
            self.load_flashcards()

    def search_clicked(self):
        # todo hide buttons that arent relevant
        self.delete_type = 'invalid'
        if self.input_line.text():
            select = '''SELECT setcode, setname, username, name
                            FROM sets
                            INNER JOIN users
                            ON users.userid = sets.userid
                            WHERE setcode = ?'''
            self.c.execute(select, (self.input_line.text(),))
            rows = self.c.fetchall()

            # headings = ['Set Code', 'Set Name', 'Number Of Flashcards']
            headings = ['Set Code', 'Set Name', 'Username', 'Name']
            # load table
            self.load_table(headings, rows)
        else:
            self.load_sets()

    def create_new_set_clicked(self):
        # todo hide buttons that arent relevant
        pass

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
        # select = '''SELECT sets.setcode, sets.setname, count(*)
        #         FROM sets
        #         INNER JOIN flashcards
        #         ON flashcards.setid = sets.setid
        #         WHERE sets.userid = ?
        #         GROUP BY sets.setid'''
        select = '''SELECT setcode, setname
                FROM sets
                WHERE userid = ?'''
        self.c.execute(select, (self.userid,))
        rows = self.c.fetchall()

        # headings = ['Set Code', 'Set Name', 'Number Of Flashcards']
        headings = ['Set Code', 'Set Name']
        # load table
        self.load_table(headings, rows)

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
        rows = [index.row() for index in self.table.selectedIndexes()]
        # get rid of duplicate row indexes
        rows = list(dict.fromkeys(rows))
        if len(rows) != 1:
            self.error_message.setText('Select 1 row to edit')
        else:
            rows = self.table.item(rows[0], 0).text()
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

            except sqlite3.IntegrityError:
                self.error_message.setText('Issue with database')


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
            self.input_line.setHidden(False)
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
            self.delete_button.setEnabled(True)

        # triggered when search button is clicked
        elif self.status == 'using code':
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
            self.delete_button.setEnabled(True)

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





