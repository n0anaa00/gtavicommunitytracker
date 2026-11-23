import json

source = "/data/custom_vss_dbc.json"
destination = "/data/kuksa_vss.json"


def clean_vss(value):
    if isinstance(value, dict):
        cleaned = {}

        for key, item in value.items():
            if key == "description" and item is None:
                cleaned[key] = ""
            elif item is None:
                continue
            else:
                cleaned[key] = clean_vss(item)

        return cleaned

    if isinstance(value, list):
        return [clean_vss(item) for item in value]

    return value


with open(source, "r", encoding="utf-8-sig") as file:
    data = json.load(file)

cleaned = clean_vss(data)

with open(destination, "w", encoding="utf-8") as file:
    json.dump(cleaned, file, indent=2)

print(f"Created compatible VSS file: {destination}")