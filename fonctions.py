import json
from typing import Any
import os

# -- Fonction pour ajouter un objet au fichier json ---

def append_object_to_json_by_class(obj: Any, json_file: str, var_name: str):
    """
    Ajoute un objet Python à un fichier JSON existant en triant par classe,
    et stocke le nom de la variable pour pouvoir le recréer tel quel.
    """
    try:
        class_name = obj.__class__.__name__
        obj_dict = obj.__dict__.copy()
        obj_dict["_var_name"] = var_name  # on stocke le nom de la variable

        # Charge le contenu existant
        data = {}
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    if not isinstance(data, dict):
                        data = {}

        # Initialise la liste pour la classe si nécessaire
        if class_name not in data:
            data[class_name] = []

        # Ajoute l'objet dans la liste correspondant à sa classe
        data[class_name].append(obj_dict)

        # Réécrit le contenu dans le fichier
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"L'objet de la classe '{class_name}' ({var_name}) a été ajouté dans {json_file}")

    except Exception as e:
        print(f"Erreur lors de l'ajout de l'objet : {e}")


# Les classes doivent être définies

"""
class Pc:
    def __init__(self, nom, ip, mac):
        self.nom = nom
        self.ip = ip
        self.mac = mac
"""

# Les objets doivent être définis

"""
pc1 = Pc("PC1","192.168.50.1","AA:BB:CC:DD:EE:FF")
"""

# Exemple d'utilisation ("test.json" étant le fichier json de destination et "pc1" la variable de l'objet visé)

"""
append_object_to_json_by_class(pc1, "test.json", "pc1")
"""








# --- Fonction pour récupérer les éléments sauvegardés dans le fichier json ---

def load_objects_and_create_vars(json_file: str):
    """
    Recrée les objets depuis le JSON et crée les variables avec les noms
    stockés dans '_var_name'.
    """
    if not os.path.exists(json_file):
        print(f"Le fichier {json_file} n'existe pas.")
        return []

    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if not content:
            print(f"Le fichier {json_file} est vide.")
            return []
        data = json.loads(content)

    created_objects = []

    for class_name, objects_list in data.items():
        cls = globals().get(class_name)
        if cls is None:
            continue

        for obj_dict in objects_list:
            var_name = obj_dict.pop("_var_name", None)  # récupère le nom de variable
            obj = cls(**obj_dict)
            created_objects.append(obj)

            if var_name:
                globals()[var_name] = obj
                print(f"Recréé : {class_name} avec {obj_dict} -> variable '{var_name}' créée")
            else:
                print(f"Recréé : {class_name} avec {obj_dict} (pas de nom de variable)")

    return created_objects

# Il faut charger le fichier json ("test.json" étant le fichier de destination))
objs = load_objects_and_create_vars("test.json")


# Les classes doivent être définies

"""
class Pc:
    def __init__(self, nom, ip, mac):
        self.nom = nom
        self.ip = ip
        self.mac = mac
"""

# Les variables sont sauvegardées par la fonction append_object_to_json_by_class, ce qui signifie que l'on peut appeler les fonctions récupérées
# comme si elles étaient écrites dans le code

"""
print(pc1.ip)     # 192.168.50.1
"""