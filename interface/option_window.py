from PyQt6.QtWidgets import QWidget


class OptionWindow(QWidget):
    def __init__(self):
        super(OptionWindow, self).__init__()
        self.setWindowTitle("Option Window")
