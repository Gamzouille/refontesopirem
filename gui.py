# gui.py
import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame)


class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sopirem")
        self.resize(500, 300)

        # --- Centrer la fenêtre sur l'écran ---
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        # --- Contenu central ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)
        central.setLayout(layout)

        # --- Titre ---
        self.title = QLabel("Bienvenue sur Sopirem")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addStretch(1)
        layout.addWidget(self.title)

        # --- Boutons ---
        self.btn_pc = QPushButton("Ajouter un PC")
        self.btn_switch = QPushButton("Ajouter un switch")
        self.btn_quit = QPushButton("Quitter")
        for btn in (self.btn_pc, self.btn_switch, self.btn_quit):
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    border-radius: 12px;
                    background-color: #738eb0;
                    color: white;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #2e3947;
                }
            """)
            layout.addWidget(btn)
        layout.addStretch(2)

        # --- Connexions boutons ---
        self.btn_pc.clicked.connect(self.ajoutePC)
        self.btn_switch.clicked.connect(self.ajouteSwitch)
        self.btn_quit.clicked.connect(self.close)

    def ajoutePC(self):
        self.title.setText("Ajouter un PC(placeholder)")

    def ajouteSwitch(self):
        self.title.setText("Ajouter un switch(placeholder)")


def run_app():
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())