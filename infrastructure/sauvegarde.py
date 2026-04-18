def sauvegarde_json(pc: PC, json_file: str, var_name: str):
    """
    Ajoute un objet Pc dans un fichier JSON et enregistre le nom de variable.
    """
    entry = pc.__dict__.copy()
    entry["_var_name"] = var_name

    data = {}
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)

    if "Pc" not in data:
        data["Pc"] = []

    data["Pc"].append(entry)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"[JSON] Pc sauvegardé sous '{var_name}'")
