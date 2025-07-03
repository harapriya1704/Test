from excel_operations import extract_glassbox_data
from config import EXCEL_PATH, OUTPUT_EXCEL
from web_operations import process_glassbox_links
from file_operations import initialize_output_excel

def main():
    initialize_output_excel(OUTPUT_EXCEL)
    data = extract_glassbox_data(EXCEL_PATH)
    process_glassbox_links(data)

if __name__ == "__main__":
    main()
