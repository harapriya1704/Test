# file_operations.py
from openpyxl import Workbook
import os

def save_results_to_excel(results, output_path):
    wb = Workbook()
    ws = wb.active
    
    # Headers including specific cookie columns
    headers = [
        "Fiscal Week", 
        "Date", 
        "Order Number", 
        "Sat/Dissat", 
        "Improve Text",
        "GIA Insights",
        "Global_DellCEMSessionCookie_CSH",
        "Global_MCMID_CSH"
    ]
    ws.append(headers)
    
    for item in results:
        row = [
            item.get("fiscal_week", ""),
            item.get("date", ""),
            item.get("order_number", ""),
            item.get("sat_dissat", ""),
            item.get("improve_text", ""),
            item.get("gia_insights", ""),
            item.get("Global_DellCEMSessionCookie_CSH", ""),
            item.get("Global_MCMID_CSH", "")
        ]
        ws.append(row)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"✅ Results saved to {output_path}")
