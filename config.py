# config.py
import os

# Toggle for test mode
TEST_MODE = True

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
EXCEL_PATH = os.path.join(BASE_DIR, "sample_data.xlsx")  
OUTPUT_EXCEL = os.path.join(BASE_DIR, "output", "glassbox_results.xlsx")

# Increased wait times for Selenium actions
WAIT_TIMES = {
    "PAGE_LOAD": 40,      # Increased from 20
    "GIA_LOAD": 25,       # Increased from 8
    "SHORT": 10,          # Increased from 3
    "COOKIE_EXTRACTION": 20  # New wait time
}

# Authentication URL for Glassbox login
AUTH_URL = "https://glassbox.dell.com/webinterface/webui/sessions"

# Optional credentials
USERNAME = "your_username"
PASSWORD = "your_password"
