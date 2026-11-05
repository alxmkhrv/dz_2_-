import json
from pathlib import Path


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            metadata = json.load(file)
        return metadata
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as table:
            table_data = json.load(table)
        return table_data
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    Path("data").mkdir(exist_ok=True)
    filepath = f"data/{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as table:
        json.dump(data, table, ensure_ascii=False, indent=4)
