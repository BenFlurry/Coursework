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
        self.add_question.clicked.connect(self.save_question_clicked)
        # initialise popout box
        self.box = QMessageBox()
        self.box.setIcon(QMessageBox.Critical)
        self.box.buttonClicked.connect(self.handle_box)

        self.variable_dict = {'Vertical Displacement': 'sy',
                              'Vertical Initial Velocity': 'uy',
                              'Vertical Final Velocity': 'vy',
                              'Vertical Acceleration': 'ay',
                              'Time': 't',
                              'Horizontal Displacement': 'sx',
                              'Horizontal Velocity': 'vx',
                              'Choose Target Variable': 'none'}

        self.variable_list = list(self.variable_dict.values())
        self.status = 'checking'
        self.add_question.setHidden(True)

    def check_valid(self):
        self.status = 'checking'
        suvat = [self.inp_sy.text(),
                 self.inp_uy.text(),
                 self.inp_vy.text(),
                 self.inp_ay.text(),
                 self.inp_ty.text()]

        svt = [self.inp_sx.text(),
               self.inp_vx.text(),
               self.inp_tx.text()]

        h = self.inp_height.text()

        message = ''
        valid_input = True
        # todo copy this into the suvat sim screen
        if self.inp_check_variable.currentText() != 'Choose Target Variable':
            # set the check variable
            check_variable = self.variable_dict[self.inp_check_variable.currentText()]
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

                index = self.variable_list.index(check_variable)
                if index <= 4:
                    if suvat[index] == '':
                        message = 'enter a value for the target variable'
                        valid_input = False
                    else:
                        check_value = float(suvat[index])
                elif 5 <= index <= 7:
                    if svt[index-5] == '':
                        message = 'enter a value for the target variable'
                        valid_input = False
                    else:
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


        if h != '':
            h = float(h)

        self.valid_question = False

        if valid_input:
            verified = verify_suvat(suvat, svt, h, check_variable, check_value)
            if verified[0] == 'invalid':
                valid_input = False
                message = 'could not calculate target variable with given inputs'

        # if input is incorrect
        if valid_input is False:
            self.box.setIcon(QMessageBox.Critical)
            self.box.setWindowTitle('Error')
            self.box.setText(message)
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.add_question.setHidden(True)

        # if it is not solveable
        elif verified[0] == 'Invalid':
            self.box.setIcon(QMessageBox.Critical)
            self.box.setWindowTitle('Error')
            self.box.setText('Not enough information given')
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.add_question.setHidden(True)

        # if valid, but the question may be wrong
        elif verified[0] is False:
            self.box.setIcon(QMessageBox.Question)
            self.box.setWindowTitle('Invalid Answer')
            self.box.setText(f'Change "{verified[1][0] if len(verified[1]) == 1 else verified[1]}" to answer value?')
            self.box.setInformativeText(
                f'The answer you entered "{check_value}" does not equal the calculated answer "{verified[1][0] if len(verified[1]) == 1 else verified[1]}"')
            self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.box.setDefaultButton(QMessageBox.Yes)
            self.check_var = check_variable
            self.check_val = check_value
            self.suvat_values = suvat
            self.svt_values = svt
            self.h_val = h
            self.calculated_val = verified

        # output success
        else:
            self.box.setInformativeText('')
            self.box.setIcon(QMessageBox.Information)
            self.box.setWindowTitle('Valid')
            self.box.setText('Valid Question')
            self.box.setStandardButtons(QMessageBox.Yes)
            self.box.setDefaultButton(QMessageBox.Yes)
            self.add_question.setHidden(False)
            self.check_var = check_variable
            self.check_val = check_value
            self.suvat_values = suvat
            self.svt_values = svt
            self.h_val = h
            self.calculated_val = verified

        self.box.exec()

    def handle_box(self, button_name):
        button_name = button_name.text()
        # if the user wants to change the value of the answer to the calculated answer
        if button_name == '&Yes' and self.status == 'checking':
            # set question satus to valid
            # change check_value to the calculated one
            self.add_question.setHidden(False)
            # if len(self.calculated_val[1] == 2):
            #     self.check_value = self.calculated_val[1]
            # else:
            #     self.check_value = self.calculated_val[1][0]

            self.update_ui_values()

            # todo make a status for editing


        elif button_name == '&No' and self.status == 'checking':
            self.add_question.setHidden(True)

        elif button_name == "&Yes" and self.status == 'saving':
            # todo remove check value from variables list and run method to save to db
            index = self.variable_list.index(self.check_var)

            self.save_question()

    def update_ui_values(self):
        var_dict = self.variable_dict
        # del var_dict['Choose Target Variable']
        var_dict['Start Height'] = 'h'
        var_list = self.variable_list
        var_list += ['h']
        index = var_list.index(self.check_var)

        inp_suvat = [self.inp_sy,
                     self.inp_uy,
                     self.inp_vy,
                     self.inp_ay,
                     self.inp_ty]

        inp_svt = [self.inp_sx,
                   self.inp_vx,
                   self.inp_tx]

        h = self.inp_height

        if index <= 3:
            inp_suvat[index].setText(str(self.calculated_val[1]))

        elif index == 4:
            inp_suvat[4].setText(str(self.calculated_val[1]))
            inp_svt[2].setText(str(self.calculated_val[1]))

        else:
            inp_svt[index - 5].setText(str(self.calculated_val[1][0]))


    def save_question_clicked(self):
        # pull values from PyQt
        invalid = False
        suvat = [self.inp_sy.text(),
                 self.inp_uy.text(),
                 self.inp_vy.text(),
                 self.inp_ay.text(),
                 self.inp_ty.text()]

        svt = [self.inp_sx.text(),
               self.inp_vx.text(),
               self.inp_tx.text()]

        h = self.inp_height.text()
        # convert to floats to compare to the already inputted values
        # fixme time being copied over to both suvat and svt results in original and new not being equal
        try:
            for i in range(5):
                if suvat[i] != '':
                    suvat[i] = float(suvat[i])
                if suvat[i] != self.suvat_values[i]:
                    invalid = True

            for i in range(3):
                if svt[i] != '':
                    svt[i] = float(svt[i])
                if svt[i] != self.svt_values[i]:
                    invalid = True

            if h != '':
                h = float(h)
            if h != self.h_val:
                invalid = True
        except ValueError:
            invalid = True

        print(f'{suvat = }, {svt = }, {h = }')
        print(f'{self.suvat_values = }, {self.svt_values}, {self.h_val = }')

        # if inputs havent changed
        if not invalid:
            self.status = 'saving'
            self.box.setIcon(QMessageBox.Question)
            self.box.setText('Are you sure you add the question:')
            list_of_vars = self.suvat_values + self.svt_values + [self.h_val]
            # remove duplicate time value
            list_of_vars.pop(4)
            # begin to make output string
            output_string = ''
            var_dict = self.variable_dict
            # add height to list / dict
            del var_dict['Choose Target Variable']
            var_dict['Start Height'] = 'h'
            var_list = self.variable_list
            var_list.remove('none')
            var_list = var_list + ['h']
            # iterate through variables and thier values
            for i in range(len(list_of_vars)):
                # varible find the key using the value for the variable name
                var_name = list(var_dict.keys())[list(var_dict.values()).index(var_list[i])]
                # construct output string
                output_string += f'{var_name} = {list_of_vars[i]} \n'

            var_name = list(var_dict.keys())[list(var_dict.values()).index(self.check_var)]
            # output answer variable and answer value
            output_string += f'answer variable = {var_name}\nanswer value = {self.check_val}'
            # run popout box
            self.box.setInformativeText(output_string)
            self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.box.setDefaultButton(QMessageBox.Yes)
            self.box.exec()

        else:
            message = 'Numbers have been changed since they were last checked, check again'
            self.box.setText('Values changed:')
            self.box.setInformativeText(message)
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()


    def save_question(self):
        # get rid of check_variable's value
        index = self.variable_list.index(self.check_variable)
        if index <= 3:
            self.suvat_values[index] = ''
        elif index == 4:
            self.suvat_values[index] = ''
            self.svt_values[index - 5] = ''
        else:
            self.svt_values[index - 5] = ''


        #
        # var_name = list(var_dict.keys())[list(var_dict.values()).index(self.check_var)]




    # todo also make a back button that goes back to hw screen