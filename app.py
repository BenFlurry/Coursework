from PyQt5.QtWidgets import QMainWindow, QLineEdit
import sys
from PyQt5 import uic

from suvat_svt_entry import SuvatEntryWindow

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        # create and load the suvat entry window
        self.setup_suvat_svt_entry()
        self.show()

    def setup_suvat_svt_entry(self):
        self.suvat_entry_window = SuvatEntryWindow(self)
