# Sopirem

Simulateur de réseau informatique avec interface graphique. Crée des PC et des switchs virtuels, relie-les entre eux, et simule des échanges réseau (ping, ARP, trames).

## Prérequis

- [Python 3.10+](https://www.python.org/downloads/) — vérifier avec `python3 --version`
- [Git](https://git-scm.com/) — vérifier avec `git --version`

## Installation

```bash
# 1. Cloner le projet
git clone https://gitlab.com/siollb/refontesopirem.git
cd refontesopirem

# 2. Créer un environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement virtuel
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 4. Installer la dépendance
pip install PyQt6
```

> L'environnement virtuel isole les dépendances du projet. Il faut le recréer à chaque nouveau clone.

## Lancer l'application

Active d'abord le venv si ce n'est pas déjà fait, puis :

```bash
source venv/bin/activate   # macOS / Linux
python main.py
```

## Sauvegarde

Les projets sont enregistrés en JSON dans `data/sauvegardes/` et peuvent être rechargés depuis l'interface.
