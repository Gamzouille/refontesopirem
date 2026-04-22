import json
import os
from classes.pc import Pc

def lecture_json(json_file: str):
    """
    Charge tous les Pc depuis test.json
    et recrée les variables sous forme d'un dictionnaire.
    """
    if not os.path.exists(json_file):
        print(f"Le fichier {json_file} n'existe pas.")
        return {}

    with open(json_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            print(f"Le fichier {json_file} est vide.")
            return {}

        data = json.loads(content)

    pcs_recrees = {}

    for obj_dict in data.get("Pc", []):
        var_name = obj_dict.pop("_var_name", None)
        pc = Pc(**obj_dict)

        if var_name:
            pcs_recrees[var_name] = pc
            print(f"[JSON] Pc recréé : '{var_name}'")

    return pcs_recrees
