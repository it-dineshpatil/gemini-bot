import json
import os


def number_check(from_number):
    json_path = os.path.join(os.path.dirname(__file__), "number.json")
    with open(json_path, "r") as f:
        data = json.load(f)
        if from_number in data:
            return True
        else:
            return False
        
# print(number_check("919327228985"))
# # def meation():
# #         json_path = os.path.join(os.path.dirname(__file__), "number.json")
# #         with open(json_path, "r") as f:
# #             data = json.load(f)  
# #             regading_person = []
# #             for i in data:
# #                 regading_person.append(data[i])
# #         return regading_person
    
# # print(meation())
# # def meation():
# #         json_path = os.path.join(os.path.dirname(__file__), "number.json")
# #         with open(json_path, "r") as f:
# #             data = json.load(f)  
# #             regading_person = []
# #             for i in data:
# #                 regading_person.append(data[i])
# #         return regading_person
    
def data():
    json_path = os.path.join(os.path.dirname(__file__), "number.json")
    with open(json_path, "r") as f:
        data = json.load(f)


def meation_person_whatsapp(name):
    json_path = os.path.join(os.path.dirname(__file__), "number.json")
    with open(json_path,"r") as f:
        data = json.load(f)
    for number, username in data.items():
        if username == name:
            return number
        
# print(meation_person_whatsapp("dinesh"))