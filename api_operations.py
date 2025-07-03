import pandas as pd
import requests
import urllib3
from datetime import datetime, timedelta


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


file_path = r"C:\Users\Harapriya_Swain\OneDrive\Python\glassbox_automation_V13(api)\output\glassbox_results.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")


filtered_df = df[df['Sat/Dissat'].str.upper() == 'DSAT'].copy()


def convert_excel_date(excel_date):
    if isinstance(excel_date, (int, float)):
        return (datetime(1899, 12, 30) + timedelta(days=excel_date)).date()
    elif isinstance(excel_date, datetime):
        return excel_date.date()
    elif isinstance(excel_date, str):
        try:
            return pd.to_datetime(excel_date).date()
        except:
            return None
    return None

def fetch_filtered_order_details(order_number, target_date):
    try:
        url = f"https://carepulse-server.g3p.pcf.dell.com/api/getOrderDetails?orderNumber={order_number}"
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [entry for entry in data if entry.get("CreatedDate", "").startswith(str(target_date))]
        return []
    except requests.RequestException as e:
        print(f"API call failed for order {order_number}: {e}")
        return []

order_details_list = []
for _, row in filtered_df.iterrows():
    order_number = row['Order Number']
    excel_date = convert_excel_date(row['Date'])
    filtered_entries = fetch_filtered_order_details(order_number, excel_date) if excel_date else []
    order_details_list.append(filtered_entries)

filtered_df['order_details'] = order_details_list


output_file = r"C:\Users\Harapriya_Swain\OneDrive\Python\glassbox_automation_V13(api)\output\enriched_glassbox_results.xlsx"
filtered_df.to_excel(output_file, index=False)

print(f"✅ Enriched data saved to {output_file}")
