import json
import requests
import pandas as pd
from pathlib import Path
from security import read_env
import datetime as dt

def execute_and_export_report(sales_man_name):
    env = read_env()
    base_url = "https://gokultexprint.frappe.cloud"
    url = f"{base_url}/api/method/frappe.desk.query_report.run"
    headers = {
        "Authorization": f"token {env.get('ERPNEXT_API_KEY')}:{env.get('ERPNEXT_API_SECRET')}"
    }
    filters = {
        "company": "Gokul Texprints Private Limited",
        "from_date": "2026-01-01",
        "to_date": dt.date.today().strftime("%Y-%m-%d"),
        "Sales_Person": [sales_man_name] if sales_man_name else [],
        "status": ["To Deliver and Bill"], # Only Pending Order Report Data
        "filt_repo_choice": "Order Summary Report",
    }
    payload = {
        "report_name": "Sales Order Tracking iDashboard Report Hns-Rep",
        "filters": json.dumps(filters),
        "ignore_prepared_report": 1
    }

    response = requests.post(url, headers=headers, data=payload)
    print(f"API Response Status: {response.status_code}")

    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    res_json = response.json()
    report_data = res_json.get("message", {})

    data_rows = report_data.get("data") or report_data.get("result") or []
    print(len(data_rows))

    clean_rows = [row for row in data_rows if isinstance(row, dict)]
    df = pd.DataFrame(clean_rows)

    columns_map = {
        "posting_date": "Posting Date",
        "party": "Party Name",
        "customerbroker": "Customer Broker",
        "voucher_no": "Voucher No",
        "city": "City Name",
        "state": "State Name",
        "custom_broker": "Broker Name",
        "invoiced": "Invoiced Amount",
        "credit_note": "Debit Note",
        "paid": "Paid Amount",
        "return": "Return Amount",
        "outstanding": "Outstanding Amount",
        "runtot": "runtot",
        "days": "Days",
        "customer_bal": "Ledger BAl",
        "voucher_type": "Voucher Type",
        "gst_no": "Gst No",
        "total": "Base Amount",
        "total_taxes_and_charges": "Total Taxes Amount",
        "party_account": "Payble Account",
        "cost_center": "Cost Center"
    }
    df.rename(columns=columns_map, inplace=True)
    remove_columns = [
        "runtot", "Gst No", "Payble Account", "Cost Center", "sort_order", "formatter",
        "account_currency", "credit_note_in_account_currency", "territory", "customer_group",
        "customer_primary_contact", "currency", "Broker Name", "Party Name"
    ]
    df.drop(columns=remove_columns, inplace=True, errors="ignore")

    file_name = f"{sales_man_name.replace(' ', '_')}_report.xlsx"
    output_folder = Path(__file__).resolve().parent / "reports"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / file_name

    df.to_excel(output_path, index=False)
    print(f"Excel file '{output_path}' created successfully!")
    return str(output_path)

print(execute_and_export_report("Dilip Singh"))