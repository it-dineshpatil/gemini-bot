from security import read_env
import requests
import json
from pathlib import Path


CUSTOMER_LIST_JS = Path(__file__).with_name("customer_list.js")

def save_customers_to_js(customers, file_path=CUSTOMER_LIST_JS):
    js_text = "const customer_list = "
    js_text += json.dumps(customers, indent=4, ensure_ascii=False)
    js_text += ";\n"
    file_path.write_text(js_text, encoding="utf-8")

def fetch_customers(customer_name):
    env = read_env()

    url = env.get("ERPNEXT_URL") + "/api/resource/Customer"
    api_key = env.get("ERPNEXT_API_KEY")
    api_secret = env.get("ERPNEXT_API_SECRET")
    headers = {
        "Authorization": f"token {api_key}:{api_secret}"
    }
    params = {
        "fields": json.dumps(["name", "customer_name"]),
        "filters": json.dumps([
            ["Customer", "customer_name", "like", f"%{customer_name}%"]
        ]),
        "limit_page_length": 10
    }
    response = requests.get(url, headers=headers, params=params)
    data = {}
    customers = []
    if response.status_code == 200:
        data = response.json()
        for customer in data.get("data", []):
            customers.append({
                "name": customer.get("name", ""),
            }) 
        save_customers_to_js(customers)
    return customers




# def jsn_data():
#     file_date = open("customer_list.js", "r")
#     data = file_date.read()
#     # con = json.loads(data)
#     return data
# print(jsn_data())