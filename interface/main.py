import sys
from PyQt6.QtWidgets import QApplication
from ui_home import HomeWindow

def main():
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
