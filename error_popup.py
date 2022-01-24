from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
ui = uic.loadUiType('error_popup.ui')[0]

'''
text edit -> error_message
'''
#
# class ErrorPopup(QMessageBox):
#     def show_popup(self, title, message, type):
#         msg = QMessageBox()
#         msg.setWindowTitle(title)
#         msg.setText(message)
#         msg.
#         if type == 'warning':
#             msg.setIcon(QMessageBox.Warning)
#         elif type == 'question':
#             msg.setIcon(QMessageBox.Question)
#         elif type == 'critical':
#             msg.setIcon(QMessageBox.Critical)
#
#         popup = msg.exec_()
'''
.setText
.setInformativeText
.setIcon(QMessageBox.Information)
.setStandardButtons(QMessageBox.Ok)
.setDefaultButton(QMessageBox.Ok)
.exec()
'''