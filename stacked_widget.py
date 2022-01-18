from PyQt5.QtWidgets import QStackedWidget, QMainWindow
from login_screen import LoginScreen

class StackedWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget
        self.show()


    def add_widget(self, screen):
        self.stacked_widget.addWidget(self, screen)
