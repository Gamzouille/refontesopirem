from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import sys

def lancer_ui():
    """Lance la fenêtre principale avec le texte 'Exemple'."""
    app = QApplication(sys.argv)
    
    fenetre = QWidget()
    fenetre.setWindowTitle("Exemple")
    fenetre.setGeometry(100, 100, 300, 200)  # x, y, largeur, hauteur

    layout = QVBoxLayout()
    label = QLabel("Exemple")
    layout.addWidget(label)
    fenetre.setLayout(layout)

    fenetre.show()
    sys.exit(app.exec())
