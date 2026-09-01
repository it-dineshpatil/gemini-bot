import json
import os
def meation():
        json_path = os.path.join(os.path.dirname(__file__), "number.json")
        with open(json_path, "r") as f:
            data = json.load(f)  
            regading_person = []
            for i in data:
                regading_person.append(data[i])
        return regading_person
ar = meation()    
print(len(ar))