import json
import os
def create_by(from_number):
        json_path = os.path.join(os.path.dirname(__file__), "number.json")
        with open(json_path, "r") as f:
            data = json.load(f)  
            return data.get(from_number)
