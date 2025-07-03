import os

TEST_MODE = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_PATH = os.path.join(BASE_DIR, "sample_data.xlsx")  
OUTPUT_EXCEL = os.path.join(BASE_DIR, "output", "glassbox_results.xlsx")


WAIT_TIMES = {
    "PAGE_LOAD": 40,      
    "GIA_LOAD": 25,      
    "SHORT": 10,          
    "COOKIE_EXTRACTION": 20  
}

AUTH_URL = "https://glassbox.dell.com/webinterface/webui/sessions"

USERNAME = "your_username"
PASSWORD = "your_password"
