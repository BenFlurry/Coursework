from app import App
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import sys
import os
import traceback


# print errors into command line
def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    # sys.exit(1)


sys.excepthook = my_exception_hook


def main():
    app = QApplication(sys.argv)
    app_window = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
