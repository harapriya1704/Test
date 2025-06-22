import os

# Toggle for test mode
TEST_MODE = True

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
EXCEL_PATH = os.path.join(BASE_DIR, "sample_data.xlsx")  
OUTPUT_EXCEL = os.path.join(BASE_DIR, "output", "glassbox_results.xlsx")

# Wait times for Selenium actions
WAIT_TIMES = {
    "PAGE_LOAD": 20,
    "GIA_LOAD": 8,
    "SHORT": 3
}

# Authentication URL for Glassbox login
AUTH_URL = "https://glassbox.dell.com/webinterface/webui/sessions"

# Optional credentials
USERNAME = "your_username"
PASSWORD = "your_password"
