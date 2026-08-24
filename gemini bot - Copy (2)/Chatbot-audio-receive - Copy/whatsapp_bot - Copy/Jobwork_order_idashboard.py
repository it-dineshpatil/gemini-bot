import json
import requests
import pandas as pd
import pathlib
from security import read_env
from datetime import date, timedelta

def execute_and_export_report(sales):
    output_path = pathlib.Path(f"report/{sales}_jobwork_report.xlsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.unlink()    
    except FileNotFoundError:
        pass
    #api Key Fetch  Security File In
    env = read_env()
    today = date.today()
    date_from = today - timedelta(days=60)
    to_date = today - timedelta(days=1)
    # print(date_from , to_date)

    url = f"{env.get('ERPNEXT_URL')}/api/method/frappe.desk.query_report.run"
    
    api_key = env.get("ERPNEXT_API_KEY")
    api_secret = env.get("ERPNEXT_API_SECRET")
    headers = {
    "Authorization": f"token {api_key}:{api_secret}"
    }

    filters = {
        "company": "Gokul Texprints Private Limited",
        "from_date": date_from.strftime("%Y-%m-%d"),
        "to_date": to_date.strftime("%Y-%m-%d"),
        "jobwork_order": "",
        "job_worker": [],
        "sales_order": "",
        "consume_item": [],
        "jobwork_order_series": [],
        "issue_status": "",
        "multi_jo_status": "",
        "sales_partner": [sales],
        "completed_so":"1",
        "filt_repo_type": "Register Report"
    }
    payload = {
        "report_name": "Jobwork Order iDashboard Hns-Rep",
        "filters": json.dumps(filters)
    }
    
    response = requests.post(url, headers=headers, data=payload)
    print(f"API Response Status: {response.status_code}")
    
    if response.status_code != 200:
        # print(response.text)
        response.raise_for_status()

    res_json = response.json()
    report_data = res_json.get("message", {})

    # print(f"Full API Response: {json.dumps(report_data, indent=2)[:500]}")  # Print first 500 chars
    
    data_rows = report_data.get("data") or report_data.get("result") or []
    # 

    clean_rows = [row for row in data_rows if isinstance(row, dict)]

    df = pd.DataFrame(clean_rows)
    # print(len(df), "rows fetched from API")

    column_names = {
        "ecustomer": "Customer Name",
        "custom_sales_partner": "Sales Partner",
        "dsales_order_no": "SO No",
        "adocument_no": "Job Order No",
        "cdate": "Job Order Date",
        "Multijo": "Multi Order No",
        "Multijodate": "Multi Order Date",
        "bjob_worker": "Jobworker Name",
        "design_created_date": "Design Created Date",
        "design_remark": "Design Remark",
        "ffabric": "Fabric",
        "cns_item_name": "Consume Item Name",
        "tjoborderitem": "Job Order Item",
        "ujoborderitem_name": "Job Order Item Name",
        "vfinish_item_code": "Finish Item Code",
        "xitem_name": "Finish Item Name",
        "grefrence_no": "Ref No",
        "hdescription": "Description",
        "liss_no": "Issue No",
        "miss_date": "Issue Date",
        "rec_no": "Rec No",
        "custom_cancel_reason": "Cancel Reason",
        "nsource_warehouse": "Source Warehouse",
        "otarget_warehouse": "Target Warehouse",
        "yfinish_qty": "Finish Qty",
        "kjwo_qty": "JO Qty",
        "pqty": "Issue Qty",
        "qjbal_qty": "JO Bal Qty",
        "rec_mts": "Rec Qty",
        "ret_mts": "Ret Qty",
        "short_mts": "Short Qty",
        "rec_bal_qty": "Rec Bal Qty",
        "iissue_status": "Issue Status",
        "qbal_qty": "Bal Qty",
        "design_created" :"Desing No",
        "custom_black_plain_item": "Black Plain Item",

    }

    df.rename(columns=column_names, inplace=True)

    # Reorder columns so the report starts with customer and sales partner
    desired_column_order = ["Customer Name", "Sales Partner" , "SO No", "Job Order No", "Job Order Date", "Multi Order No", "Multi Order Date",
                            "Jobworker Name", "Design Created Date","Desing No", "Design Remark","Issue Status","Fabric", "Consume Item Name", "Job Order Item", "Job Order Item Name", "Finish Item Code", "Finish Item Name",
                            "Ref No", "Description", "Issue No", "Issue Date", "Rec No", "Cancel Reason", "Source Warehouse", "Target Warehouse", "Finish Qty", "JO Qty", "Issue Qty", "JO Bal Qty", "Rec Qty", "Ret Qty", "Short Qty", "Rec Bal Qty", "Bal Qty", "Black Plain Item"]
    
    ordered_cols = [col for col in desired_column_order if col in df.columns]
    remaining_cols = [col for col in df.columns if col not in ordered_cols]
    df = df[ordered_cols + remaining_cols]
    
    #  Drop unnecessary columns
    if sales != "Bikash Behera":
           columns_to_drop = [ "Description", "Cancel Reason", "Multi Order No", 
                       "Multi Order Date", "company", "Ref No", "Black Plain Item","cns_item_code","sort_order","formatter","naming_series"]
    else:
        columns_to_drop = [ "Description", "Cancel Reason", "Multi Order No","naming_series","formatter" ,
        "Multi Order Date", "company", "Ref No", "Black Plain Item","cns_item_code","sort_order",
        "Design Created Date","Design Remark","Multi Order No","Black Plain Item","Desing No","Rec Bal Qty","Finish Qty","Finish Item Code","jmulti_jo_status"]
        
         
    existing_cols = [col for col in columns_to_drop if col in df.columns]
    df.drop(columns=existing_cols, inplace=True, errors="ignore")
    
    #  Export to Excel once
    df.to_excel(output_path, index=False)
    return str(output_path)

# if __name__ == "__main__":
#     execute_and_export_report("Hitesh Batra")
