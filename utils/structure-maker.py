import os

IGNORED_DIRS = {"__pycache__", ".git", ".idea", ".vscode"}
IGNORED_FILES = {".DS_Store"}

def construire_arborescence(chemin, prefix=""):
    lignes = []

    elements = sorted(os.listdir(chemin))
    elements = [
        e for e in elements
        if e not in IGNORED_DIRS and e not in IGNORED_FILES
    ]

    for index, element in enumerate(elements):
        chemin_complet = os.path.join(chemin, element)
        dernier = index == len(elements) - 1

        branche = "└── " if dernier else "├── "
        lignes.append(prefix + branche + element)

        if os.path.isdir(chemin_complet):
            extension = "    " if dernier else "│   "
            lignes.extend(
                construire_arborescence(chemin_complet, prefix + extension)
            )

    return lignes


if __name__ == "__main__":
    racine = os.getcwd()
    nom_racine = os.path.basename(racine)

    lignes = [nom_racine + "/"]
    lignes.extend(construire_arborescence(racine))

    with open("structure_projet.txt", "w", encoding="utf-8") as f:
        for ligne in lignes:
            f.write(ligne + "\n")

    print("✅ Structure du projet écrite dans structure_projet.txt")
