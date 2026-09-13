"""
Project: Project Demo
File: resources.py
Author: Diego Vegas Acosta
Date: 30/03/26

Description:
----------------------------------------------------------------------------
This file contains the constants, modules and imports (mapping, etc...) 

Main Features:
----------------------------------------------------------------------------
- Normalize (columns names to centroid material or sql columns)

Technologies Used:
----------------------------------------------------------------------------
- Python
- Regular expressions

Notes:
----------------------------------------------------------------------------
- Normalize function could be refinated

Usage:
----------------------------------------------------------------------------
Import it as a module:
    from resources import [resource]

Example:
----------------------------------------------------------------------------
# Example usage
if __name__ == "__main__":

"""


import hashlib
import re
import unicodedata

CSV_PATH = "./resources/sensitive_columns.txt"
HASH_PATH = "./resources/sensitive_hash.txt"


def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def load_hash(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_hash(hash_value, path):
    with open(path, "w") as f:
        f.write(hash_value)


def hash_changed(csv_path=CSV_PATH, hash_path=HASH_PATH):
    old_hash = load_hash(hash_path)
    new_hash = file_hash(csv_path)

    if old_hash != new_hash:
        save_hash(new_hash, hash_path)
        return True
    return False



# lo pasa todo a nombres, pero con espacio
def normalize(text: str, to_sql: bool = False) -> str:
    # 1. asegurar string
    text = str(text)

    # 2. quitar acentos
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    # 3. separar camelCase / PascalCase
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)

    # 4. unificar separadores
    text = re.sub(r"[_\-]+", " ", text)

    # 5. lowercase
    text = text.lower()

    # 6. quitar caracteres raros
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # 7. normalizar espacios
    text = re.sub(r"\s+", " ", text).strip()

    # 8. salida según modo
    if to_sql:
        text = text.replace(" ", "_")

    return text



COST_PER_1K_TOKENS = 0.00002  # text-embedding-3-small (aprox)
