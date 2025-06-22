from openpyxl import Workbook
import os

def save_results_to_excel(results, output_path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Fiscal Week", "Date", "Order Number", "Sat/Dissat", "Improve Text", "GIA Insights"])
    for item in results:
        ws.append([
            item.get("fiscal_week", ""),
            item.get("date", ""),
            item.get("order_number", ""),
            item.get("sat_dissat", ""),
            item.get("improve_text", ""),
            item.get("gia_insights", "")
        ])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
