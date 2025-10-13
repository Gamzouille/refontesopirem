import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame)

from ui_nouveau_projet import ProjectWindow

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accueil - Soupir'âme")
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
        self.title = QLabel("Bienvenue sur Soupir'âme")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addStretch(1)
        layout.addWidget(self.title)

        # --- Soulignement animé (frame verte) ---
        self.underline = QFrame(self)
        self.underline.setGeometry(
            self.title.x(), self.title.y() + self.title.height() + 3, 0, 3
        )
        self.underline.setStyleSheet("background-color: #4CAF50; border-radius: 2px;")
        self.underline_anim = QPropertyAnimation(self.underline, b"geometry")
        self.underline_anim.setDuration(800)  # durée animation en ms

        # --- Boutons ---
        self.btn_new = QPushButton("Créer un nouveau projet")
        self.btn_import = QPushButton("Importer un projet existant")
        self.btn_quit = QPushButton("Quitter")
        for btn in (self.btn_new, self.btn_import, self.btn_quit):
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    border-radius: 12px;
                    background-color: #4CAF50;
                    color: white;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            layout.addWidget(btn)
        layout.addStretch(2)

        # --- Connexions boutons ---
        self.btn_new.clicked.connect(self.create_project)
        self.btn_import.clicked.connect(self.import_project)
        self.btn_quit.clicked.connect(self.close)

        # --- Animation d'apparition de la fenêtre ---
        self.fade_in()

        # --- Lancer le soulignement après 1,5 seconde ---
        QTimer.singleShot(500, self.animate_underline)

    def fade_in(self):
        """Animation d'apparition en fondu"""
        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def animate_underline(self):
        """Animation de soulignement du titre de gauche à droite"""
        title_geom = self.title.geometry()
        start_rect = QRect(title_geom.x(), title_geom.y() + title_geom.height() + 5, 0, 3)
        end_rect = QRect(title_geom.x(), title_geom.y() + title_geom.height() + 5, title_geom.width(), 3)
        self.underline_anim.setStartValue(start_rect)
        self.underline_anim.setEndValue(end_rect)
        self.underline_anim.start()

    def create_project(self):
        """Ouvre la fenêtre du nouveau projet"""
        self.project_window = ProjectWindow()
        self.project_window.show()
        self.close()

    def import_project(self):
        self.title.setText("Importation d’un projet (placeholder)")


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