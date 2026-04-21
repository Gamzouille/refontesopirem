# Soupirame

Simulateur de réseau informatique avec interface graphique. Crée des PC et des switchs virtuels, relie-les entre eux, et simule des échanges réseau (ping, ARP, trames).

## Prérequis

- [Python 3.10+](https://www.python.org/downloads/) — vérifier avec `python3 --version`
- [Git](https://git-scm.com/) — vérifier avec `git --version`

## Installation

```bash
# 1. Cloner le projet
git clone https://gitlab.com/siollb/refontesopirem.git
cd refontesopirem

# 2. Installer la dépendance
pip install PyQt6
```

## Lancer l'application

```bash
python main.py
```

> Sur macOS/Linux, utilise `python3` si `python` ne fonctionne pas.

## Sauvegarde

Les projets sont enregistrés en JSON dans `data/sauvegardes/` et peuvent être rechargés depuis l'interface.
