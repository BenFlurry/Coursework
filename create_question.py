from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5 import uic
from suvat_lib import *
import sqlite3

ui = uic.loadUiType('create_question.ui')[0]

'''
inp_(suvat variable name) -> line edit
inp_check_variable -> combo box
graph_on -> radio button
suvat_question -> radio button
velangle_question -> radio button
check_valid_quesiton -> push button
add_question -> push button
'''


class CreateQuestion(QMainWindow, ui):
    def __init__(self, app_window):
        # load UI
        super().__init__()
        self.setupUi(app_window)

        # connect to SQL db
        self.conn = sqlite3.connect('database2.db', isolation_level=None)
        self.c = self.conn.cursor()
        # button handlers
        self.check_valid_question.clicked.connect(self.check_valid)
        # initialise popout box
        self.box = QMessageBox()
        self.box.setIcon(QMessageBox.Critical)
        self.box.buttonClicked.connect(self.handle_box)


    def check_valid(self):
        suvat = [self.inp_sy.text(),
                 self.inp_uy.text(),
                 self.inp_vy.text(),
                 self.inp_ay.text(),
                 self.inp_ty.text()]

        svt = [self.inp_sx.text(),
               self.inp_vx.text(),
               self.inp_tx.text()]

        h = self.inp_height.text()

        variable_dict = {'Vertical Displacement': 'sy',
                         'Vertical Initial Velocity': 'uy',
                         'Vertical Final Velocity': 'vy',
                         'Vertical Acceleration': 'ay',
                         'Time': 't',
                         'Horizontal Displacement': 'sx',
                         'Horizontal Velocity': 'vx',
                         'Choose Target Variable': 'none'}

        check_variable = variable_dict[self.inp_check_variable.currentText()]

        message = ''
        valid_input = True
        # todo copy this into the suvat sim screen
        if check_variable != 'none':
            # if 2 values of t entered, they must be equal
            if suvat[4] == '' or svt[2] == '' or (suvat[4] == svt[2] and suvat[4] != '' and svt[2] != ''):
                # change t to int
                if suvat[4] != '':
                    suvat[4] = float(suvat[4])
                else:
                    suvat[4] = svt[2]

                if svt[2] != '':
                    svt[2] = float(svt[2])
                else:
                    svt[2] = suvat[4]
                # find the check value

                variable_list = list(variable_dict.values())
                variable_list.remove('none')
                index = variable_list.index(check_variable)
                if index <= 4:
                    check_value = float(suvat[index])
                elif 5 <= index <= 7:
                    check_value = float(svt[index - 5])

                # check t > 0
                if type(suvat[4]) != float or (suvat[4] > 0 and svt[2] > 0):
                    variables = suvat + svt + [h]
                    # check numbers have been entered
                    for i in range(9):
                        if variables[i] != '':
                            try:
                                float(variables[i])
                            except ValueError:
                                message = 'Input variables as numbers'
                                valid_input = False
                else:
                    message = 'Check time inputs. time must be greater than or equal to 0'
                    valid_input = False
            else:
                message = 'Check time inputs. If 2 are entered, they must be equal'
                valid_input = False

        else:
            message = 'Choose a target variable'
            valid_input = False

        if valid_input:
            verified = verify_suvat(suvat, svt, h, check_variable, check_value)
        # if input is incorrect
        if valid_input is False:
            self.box.setIcon(QMessageBox.Critical)
            self.box.setWindowTitle('Error')
            self.box.setText(message)
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)

        # if it is not solveable
        elif verified[0] == 'Invalid':
            self.box.setIcon(QMessageBox.Critical)
            self.box.setWindowTitle('Error')
            self.box.setText('Not enough information given')
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)

        # if valid, but the question may be wrong
        elif verified[0] is False:
            self.box.setIcon(QMessageBox.Question)
            self.box.setWindowTitle('Invalid Answer')
            # todo make it so different lengths can still have both values shown
            self.box.setText(f'Change {verified[1][len(verified[1]) - 1]} to answer value?')
            self.box.setInformativeText(f'The answer you entered ({check_value}) does not equal the calculated answer {verified[1][len(verified[1]) - 1]}')
            self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.box.setDefaultButton(QMessageBox.Yes)

        # output success
        else:
            self.box.setIcon(QMessageBox.Information)
            self.box.setWindowTitle('Valid')
            self.box.setText('Valid Question')
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)

        self.box.exec()

        self.check_variable = check_variable
        self.check_value = check_value
        self.suvat = suvat
        self.svt = svt
        self.h = h
        self.verified = verified

    # todo make check var/val global, if yes, change them to calculated
    def handle_box(self, button_name):
        button_name = button_name.text()
        print(button_name)
        if button_name == '&Yes':
            pass

    def save_question(self):
        pass



