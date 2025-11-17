# ------------------------
# Importation des classes
from classes.pc import Pc 
# ------------------------


# ------------------------
# Importation des fonctions
from fonctions.sauvegarde import sauvegarde_pc
from fonctions.lecture import lecture_pcs
# ------------------------

# ------------------------
# Importation de l'UI
from UI.exemple_ui import lancer_ui
# ------------------------


# ------------------------ 
# Selection du fichier json
JSON_FILE = "structure/sauvegardes/test.json"
# ------------------------


# ------------------------
# Création et sauvegarde
pc1 = Pc("Serveur", "192.168.1.10", "AA:BB:CC:DD:EE:01")
pc2 = Pc("Bureau", "192.168.1.11", "AA:BB:CC:DD:EE:02")

sauvegarde_pc(pc1, JSON_FILE, "pc1")
sauvegarde_pc(pc2, JSON_FILE, "pc2")
# ------------------------


# ------------------------
# Lecture et utilisation
pcs = lecture_pcs(JSON_FILE)

print(pcs["pc1"].ip)
print(pcs["pc2"].mac)
# ------------------------


# ------------------------
# Lancement UI
lancer_ui()
# ------------------------