import json
import requests
import pandas as pd
from pathlib import Path
from security import read_env
import datetime as dt
import time
from whatsapp_send_text  import  whatsapp_send_text
ORDER_SUMMARY_COLUMNS = {
    "customer_name": "Customer Name",
    "sal_ord_no": "Sales Order",
    "1DaysDifference": "DiffDays",
    "sal_ord_date": "SO Date",
    "delivery_date": "Del_Date",
    "sal_ord_qty": "SO Qty",
    "del_qty": "Del Qty",
    "city": "City",
    "remarks": "Remarks",
    "sales_man": "Sales Man",
    "12Days": "Days",
    "1DaysDifference": "DiffDays",
    "Cjw_no": "Customer Job No",
    "cjw_date": "Customer Job Date",
    "CJw_total_qty": "Customer Job Qty",
    "po_supplier_name": "Po Supplier Name",
    "po_no": "Purchase Order",
    "po_date": "PO Date",
    "po_qty": "PO Qty",
    "po_rec_no": "Purchase Rec No",
    "po_rec_date": "Po Rec Date",
    "po_rec_qty": "PO Rec Qty",
    "jo_no": "Jobwork Order",
    "jo_date": "JO Date",
    "job_cns_item": "JO Item",
    "jo_qty": "JO Qty",
    "design_created": "Design No",
    "design_created_date": "Design Date",
    "design_remark": "Design Remark",
    "jobworker": "Jobworker",
    "iss_no": "Issue No",
    "iss_date": "Iss Date",
    "iss_qty": "Iss Qty",
    "rec_no": "Rec No",
    "rec_date": "Rec Date",
    "rec_mts": "Rec Qty",
    "cut_no": "Cut No",
    "cut_date": "Cut Date",
    "cut_mts": "Cut Qty",
    "del_no": "Delivery No",
    "del_date": "Del Date",
    
    "sal_inv_no": "Sales Invoice No",
    "sal_inv_date": "Sales Invoice Date",
    "sal_inv_qty": "Sal Inv Qty",
}

# TURN_OVER_TIME_COLUMNS = {
#     "sal_ord_no": "Sales Order",
#     "customer_name": "Customer Name",
#     "sal_ord_date": "SO Date",
#     "2_job_days": "Job Days",
#     "21_Design_days": "Design Days",
#     "3_po_days": "Po Days",
#     "4_po_rec_days": "Po Rec Data",
#     "5_iss_days": "Issue Days",
#     "6_rec_days": "Rec Days",
#     "7_del_days": "Del Days",
#     "8_inv_days": "Inv Days",
# }


def sales_report_exu(from_number,sales_man_name, report_type="Order Summary Report"):
    env = read_env()
    base_url = (env.get("ERPNEXT_URL") or "https://gokultexprint.frappe.cloud").rstrip("/")
    url = f"{base_url}/api/method/frappe.desk.query_report.run"
    headers = {
        "Authorization": f"token {env.get('ERPNEXT_API_KEY')}:{env.get('ERPNEXT_API_SECRET')}"
    }
    filters = {
        "company": "Gokul Texprints Private Limited",
        "from_date": "2026-09-25",
        "to_date": dt.date.today().strftime("%Y-%m-%d"),
        "sales_order": "",
        "customer": [],
        "city": "",
        "Sales_Person": [sales_man_name] if sales_man_name else [],
        "status": "To Deliver and Bill",
        "jo_qty": 0,
        "iss_qty": 0,
        "rec_mts": 0,
        "po_qty": 0,
        "po_rec_no": 0,
        "del_qty": 0,
        "sal_inv_qty": 0,
        "filt_repo_type": report_type,
    }
    payload = {
        "report_name": "Sales Order Tracking iDashboard Report Hns-Rep",
        "filters": json.dumps(filters),
        "ignore_prepared_report": 1
    }

    for attempt in range(3):
        try:
            response = requests.post(
                url,
                headers=headers,
                data=payload,
                timeout=(10, 120),
            )
            break
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt == 2:
                raise RuntimeError(
                    f"Could not get a response from ERPNext at {base_url}. "
                    "Check the server URL, network connection, and ERPNext availability."
                ) from exc
            time.sleep(attempt + 1)

    print(f"API Response Status: {response.status_code}")

    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

        
        
    res_json = response.json()
    report_data = res_json.get("message", {})

    data_rows = report_data.get("data") or report_data.get("result") or []
    print(len(data_rows))

    if data_rows and isinstance(data_rows[0], (list, tuple)):
        report_columns = report_data.get("columns") or []
        fieldnames = [
            column.get("fieldname") if isinstance(column, dict) else None
            for column in report_columns
        ]
        clean_rows = [
            dict(zip(fieldnames, row))
            for row in data_rows
            if isinstance(row, (list, tuple))
        ]
    else:
        clean_rows = [row for row in data_rows if isinstance(row, dict)]
    # print(clean_rows)
    df = pd.DataFrame(clean_rows)

    columns_map = ORDER_SUMMARY_COLUMNS

    df.rename(columns=columns_map, inplace=True)
    df.drop(columns=["sort_order", "formatter"], inplace=True, errors="ignore")

    desired_column_order = [
        label for fieldname, label in columns_map.items() if clean_rows and fieldname in clean_rows[0]
    ]
    ordered_columns = [column for column in desired_column_order if column in df.columns]
    remaining_columns = [column for column in df.columns if column not in ordered_columns]
    df = df[ordered_columns + remaining_columns]

    file_name = f"{sales_man_name.replace(' ', '_')}_report.xlsx"
    output_folder = Path(__file__).resolve().parent / "reports"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / file_name

    df.to_excel(output_path, index=False)
    print(f"Excel file '{output_path}' created successfully!")
    error_message = f"""⚠️ Technical Error \n\n We’re unable to process your request due to a temporary backend issue.\n\n👨‍💻 Please contact Dinesh – IT Team for assistance.\n\n Please try again later."""

    if response.status_code != 200:
        whatsapp_send_text(from_number,error_message)
    return str(output_path)

# print(sales_report_exu("9181002166","Bikash Behera"))