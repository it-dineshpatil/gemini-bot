import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(base_dir, "number.json")

with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

data.get("918140021166")