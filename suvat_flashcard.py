from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5 import uic
from suvat_lib import *
import sqlite3
from data import Data
from data import data_dict

ui = uic.loadUiType('create_question.ui')[0]

'''
inp_(suvat variable name) -> line edit
inp_check_variable -> combo box
show_graph -> push button
suvat_question -> radio button
velangle_question -> radio button
check_valid_quesiton -> push button
add_question -> push button
question_name -> line edit
'''

# todo need to handle tuples tuples and more tuples


class CreateSuvatFlashcard(QMainWindow, ui):
    def __init__(self, app_window):
        # load UI
        super().__init__()
        self.setupUi(app_window)

        # connect to SQL db
        self.conn = sqlite3.connect('database3.db', isolation_level=None)
        self.c = self.conn.cursor()
        # button handlers
        self.check_valid_question.clicked.connect(self.check_valid)
        self.add_question.clicked.connect(self.save_question_clicked)
        self.show_graph.clicked.connect(self.graph_on)
        # initialise popout box
        self.box = QMessageBox()
        self.box.setIcon(QMessageBox.Critical)
        self.box.buttonClicked.connect(self.handle_box)
        self.graph_allowed = False
        self.data = Data()



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
        self.calculated_val = False,

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
        # todo handle tuple inputs
        if self.inp_check_variable.currentText() != 'Choose Target Variable':
            try:
                # set the check variable
                check_variable = self.variable_dict[self.inp_check_variable.currentText()]
                # if 2 values of t entered, they must be equal
                if suvat[4] == '' or svt[2] == '' or (suvat[4] == svt[2] and suvat[4] != '' and svt[2] != ''):
                    # check if inputs is a tuple:
                    if ',' in svt[0]:
                        svt[0] = list(svt[0].split(','))
                        svt[0][0] = float(svt[0][0])
                        svt[0][1] = float(svt[0][1])
                    if ',' in svt[1]:
                        svt[1] = list(svt[1].split(','))
                        svt[1][0] = float(svt[1][0])
                        svt[1][1] = float(svt[1][1])

                    if ',' in suvat[4]:
                        suvat[4] = list(suvat[4].split(','))
                        svt[2] = suvat[4]
                        suvat[4][0] = float(suvat[4][0])
                        suvat[4][1] = float(suvat[4][1])
                    # change t to int
                    else:
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
                    print(f'{index = }')
                    if index <= 4:
                        if suvat[index] == '':
                            message = 'enter a value for the target variable'
                            valid_input = False
                        else:
                            if type(suvat[index]) != list:
                                check_value = float(suvat[index])
                            else:
                                check_value = suvat[index]
                    elif 5 <= index <= 7:
                        if svt[index - 5] == '':
                            message = 'enter a value for the target variable'
                            valid_input = False
                        else:
                            if type(svt[index-5]) != list:
                                check_value = float(svt[index - 5])
                            else:
                                check_value = svt[index-5]

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
                                except TypeError:
                                    pass
                    else:
                        message = 'Check time inputs. time must be greater than or equal to 0'
                        valid_input = False
                else:
                    message = 'Check time inputs. If 2 are entered, they must be equal'
                    valid_input = False
            except ValueError:
                message = 'Input numbers only'
                valid_input = False
        else:
            message = 'Choose a target variable'
            valid_input = False

        if h != '':
            h = float(h)

        self.valid_question = False

        print(f'{valid_input = }')

        if valid_input:
            print(f'{type(check_value) = }')
            if type(check_value) == list:
                check_value = tuple(check_value)
            a = suvat; b = svt; c = h; d = check_variable; e = check_value
            print(f'{suvat = }, {svt = }')
            verified = verify_suvat(a, b, c, d, e)
            # print(f'after verified: {suvat = }, {svt = }')
            index = self.variable_list.index(check_variable)

            if index <= 4:
                suvat[index] = check_value
            if index >= 4:
                svt[index-5] = check_value

            # print(f'{self.variable_list = }')
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
                f'The answer you entered "{check_value}" does not equal the calculated answer '
                f'"{verified[1][0] if len(verified[1]) == 1 else verified[1]}"')
            self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.box.setDefaultButton(QMessageBox.Yes)
            self.box.buttonClicked.connect(self.handle_box)
            self.check_var = check_variable
            self.check_val = check_value
            index = self.variable_list.index(check_variable)
            # set the incorrect value to correct value
            if len(verified) == 1:
                if index <= 3:
                    suvat[index] = verified[1][0]
                elif index == 4:
                    suvat[4] = verified[1][0]
                    svt[2] = verified[1][0]
                else:
                    svt[index - 4] = verified[1][0]
            else:
                if index <= 3:
                    suvat[index] = verified[1]
                elif index == 4:
                    suvat[4] = verified[1]
                    svt[2] = verified[1]
                else:
                    svt[index - 4] = verified[1]

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
            # print(f'initial function: {self.suvat_values = }, {self.svt_values = }')

        if self.allow_graph.isChecked():
            self.graph_allowed = True
        else:
            self.graph_allowed = False

        self.box.exec()

    def handle_box(self, button_name):
        button_name = button_name.text()
        # if the user wants to change the value of the answer to the calculated answer

        if button_name == "&Yes" and self.status == 'saving':
            self.finalise()

        elif button_name == '&Yes' and self.status == 'checking' or self.calculated_val[0] is True:
            self.add_question.setHidden(False)
            self.update_ui_values()

        elif button_name == '&No' and self.status == 'checking':
            self.add_question.setHidden(True)

    # update values on the ui
    def update_ui_values(self):
        var_dict = self.variable_dict
        # del var_dict['Choose Target Variable']
        var_dict['Start Height'] = 'h'
        var_list = self.variable_list
        if 'h' not in var_list:
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

        untuple = False
        if len(self.calculated_val[1]) == 1:
            untuple = True

        if index <= 3:
            if untuple:
                inp_suvat[index].setText(str(self.calculated_val[1][0]))
            else:
                inp_suvat[index].setText(str(self.calculated_val[1][0]) + ', ' + str(self.calculated_val[1][1]))

        elif index == 4:
            if untuple:
                inp_suvat[4].setText(str(self.calculated_val[1][0]))
                inp_svt[2].setText(str(self.calculated_val[1][0]))
            else:
                inp_suvat[4].setText(str(self.calculated_val[1][0]) + ', ' + str(self.calculated_val[1][1]))
                inp_svt[2].setText(str(self.calculated_val[1][0]) + ', ' + str(self.calculated_val[1][1]))

        else:
            if untuple:
                inp_svt[index - 5].setText(str(self.calculated_val[1][0]))
            else:
                inp_svt[index - 5].setText(str(self.calculated_val[1][0]) + ', ' + str(self.calculated_val[1][1]))

    # check values havent changed and ask if they wish to save
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
        try:
            if suvat[4] == '' or svt[2] == '' or (suvat[4] == svt[2] and suvat[4] != '' and svt[2] != ''):
                # check if inputs is a tuple:
                if ',' in svt[0]:
                    svt[0] = list(svt[0].split(','))
                    svt[0][0] = float(svt[0][0])
                    svt[0][1] = float(svt[0][1])
                if ',' in svt[1]:
                    svt[1] = list(svt[1].split(','))
                    svt[1][0] = float(svt[1][0])
                    svt[1][1] = float(svt[1][1])

                if ',' in suvat[4]:
                    suvat[4] = list(suvat[4].split(','))
                    svt[2] = suvat[4]
                    suvat[4][0] = float(suvat[4][0])
                    suvat[4][1] = float(suvat[4][1])
                # change t to int
                else:
                    if suvat[4] != '':
                        suvat[4] = float(suvat[4])
                    else:
                        suvat[4] = svt[2]

                    if svt[2] != '':
                        svt[2] = float(svt[2])
                    else:
                        svt[2] = suvat[4]

            # print(f'{self.suvat_values[4] = }')

            for i in range(5):
                if type(suvat[i]) == list:
                    suvat[i] = tuple(suvat[i])
                elif suvat[i] != '':
                    suvat[i] = float(suvat[i])
                elif self.suvat_values[i] is None:
                    self.suvat_values[i] = ''
                elif suvat[i] != self.suvat_values[i]:
                    invalid = True

            for i in range(3):
                if type(svt[i]) == list:
                    svt[i] = tuple(svt[i])
                elif svt[i] != '':
                    svt[i] = float(svt[i])
                elif self.svt_values[i] is None:
                    self.svt_values[i] = ''
                elif svt[i] != self.svt_values[i]:
                    invalid = True

            if h != '':
                h = float(h)
            if h != self.h_val:
                invalid = True
        except TypeError:
            invalid = True
            print('value error')

        # print(f'{self.suvat_values = }, {self.svt_values = }')
        # print(f'{suvat = }, {svt = }')

        # if inputs havent changed
        if not invalid:
            print('im here')
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
            if 'Choose Target Variable' in list(var_dict.keys()):
                del var_dict['Choose Target Variable']
            var_dict['Start Height'] = 'h'
            var_list = self.variable_list
            if 'none' in var_list:
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

    def finalise(self):
        # get rid of check_variable's value
        print('nowhere')
        index = self.variable_list.index(self.check_var)
        if index <= 3:
            self.suvat_values[index] = ''
        elif index == 4:
            self.suvat_values[index] = ''
            self.svt_values[index - 5] = ''
        else:
            self.svt_values[index - 5] = ''
        # userid = self.data.get_userid()
        userid = data_dict['userid']
        print(f'{userid = }')
        flashcard_name = self.question_name.text()
        values = self.suvat_values + self.svt_values + [self.h_val]
        for i in range(len(values)):
            if type(values[i]) == float:
                values[i] = str(values[i])

        # get rid of duplicate t value
        values.pop(len(values) - 2)

        # insert values into SQL
        try:
            if flashcard_name != '':
                # insert into the flashcard table
                insert = '''INSERT INTO flashcards VALUES (null, ?, ?, ?)'''
                setid = data_dict['setid']
                self.c.execute(insert, (flashcard_name, setid, 'suvat'))

                # get the flashcard id
                select = '''SELECT MAX(flashcardid) 
                FROM flashcards 
                WHERE name = ?'''
                self.c.execute(select, (flashcard_name,))
                flashcard_id = self.c.fetchall()[0][0]

                # so we can add the flashcard id, and the values to the suvat values table
                insert = f'''INSERT INTO suvatcards
                VALUES (null{', ?' * 13}) '''
                # un-tuple the answer, so it can be added as 2 values in the table
                if len(self.calculated_val[1]) == 1:
                    answer = (str(self.calculated_val[1][0]), '')
                else:
                    answer = (str(self.calculated_val[1][0]),
                              str(self.calculated_val[1][1]))

                self.c.execute(insert, (flashcard_id,
                                        *values,
                                        int(self.graph_allowed),
                                        self.check_var,
                                        answer[0],
                                        answer[1]))

            else:
                self.box.setWindowTitle('Invalid Entry')
                self.box.setText('Enter a question name')
                self.box.setInformativeText('')
                self.box.setStandardButtons(QMessageBox.Ok)
                self.box.setDefaultButton(QMessageBox.Ok)
                self.box.exec()

        except Exception as e:
            print(f'exception: {e}')

    def graph_on(self):
        if self.h_val == '':
            h = 0
        else:
            h = self.h_val

        index = self.variable_list.index(self.check_var)
        if index <= 3:
            self.suvat_values[index] = ''
        elif index == 4:
            self.suvat_values[index] = ''
            self.svt_values[index - 5] = ''
        else:
            self.svt_values[index - 5] = ''

        suvat = self.suvat_values
        svt = self.svt_values
        for i in range(5):
            if suvat[i] is None:
                suvat[i] = ''

        for i in range(3):
            if svt[i] is None:
                svt[i] = ''

        print(f' graphing {suvat = }, {svt = }')
        message = graph_main_suvat(suvat, svt, h)
        if not message:
            self.box.setWindowTitle('Input Error')
            self.box.setIcon(QMessageBox.Critical)
            self.box.setText('Not enough information to plot the graph')
            self.box.setStandardButtons(QMessageBox.Ok)
            self.box.setInformativeText('')
            self.box.setDefaultButton(QMessageBox.Ok)
            self.box.exec()

