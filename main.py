from excel_operations import extract_glassbox_data
from config import EXCEL_PATH, OUTPUT_EXCEL
from web_operations import process_glassbox_links
from file_operations import save_results_to_excel

def main():
    data = extract_glassbox_data(EXCEL_PATH)
    results = process_glassbox_links(data)
    save_results_to_excel(results, OUTPUT_EXCEL)

if __name__ == "__main__":
    main()
