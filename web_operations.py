from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import WAIT_TIMES, AUTH_URL
import time

def extract_gia_insights(driver):
    try:
        WebDriverWait(driver, WAIT_TIMES["PAGE_LOAD"] + 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        WebDriverWait(driver, WAIT_TIMES["SHORT"] + 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'GIA Insights')]"))
        ).click()

        insights_container = WebDriverWait(driver, WAIT_TIMES["GIA_LOAD"] + 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'insights-body')]"))
        )

        previous_length = 0
        stable_count = 0
        max_wait = 40
        start_time = time.time()

        while time.time() - start_time < max_wait:
            current_text = driver.execute_script("return arguments[0].innerText;", insights_container)
            current_length = len(current_text)

            if current_length == previous_length:
                stable_count += 1
            else:
                stable_count = 0
                previous_length = current_length

            if stable_count >= 5:
                break

            time.sleep(1)

        print("Extracted Full GIA Insights:", current_text[:1200])
        return current_text

    except Exception as e:
        print("GIA Insights extraction failed:", str(e))
        return ""

def close_gia_insights(driver):
    print("Attempting to close GIA Insights popover...")

    try:
        print("Trying fallback: clicking GIA Insights button again...")
        toggle_btn = WebDriverWait(driver, WAIT_TIMES["SHORT"] + 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'GIA Insights')]"))
        )
        try:
            toggle_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", toggle_btn)

        print("✅ Closed GIA Insights popover by toggling the button.")
        time.sleep(2)
        return

    except Exception as e:
        print("❌ Fallback toggle failed — GIA Insights popover could not be closed:", str(e))

def extract_cookie_ids(driver):
    try:
        print("Clicking the cross icon to reveal cookie table...")
        cross_icon = WebDriverWait(driver, WAIT_TIMES["SHORT"] + 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'Close')]"))
        )
        cross_icon.click()

        print("Waiting for cookie table to load...")
        WebDriverWait(driver, WAIT_TIMES["PAGE_LOAD"] + 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@title, 'Global_DellCEMSessionCookie_CSH') or contains(@title, 'Global_MCMID_CSH')]"))
        )

        cem_span = driver.find_element(By.XPATH, "//span[contains(@title, 'DellCEMSessionCookie')]")
        mcmid_span = driver.find_element(By.XPATH, "//span[contains(@title, 'MCMID')]")

        cem_id = cem_span.get_attribute("title")
        mcmid = mcmid_span.get_attribute("title")

        print(f"✅ Extracted CEM ID: {cem_id}")
        print(f"✅ Extracted MCMID: {mcmid}")

        return cem_id, mcmid

    except Exception as e:
        print("❌ Failed to extract cookie IDs:", str(e))
        return "", ""

def process_glassbox_links(data):
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    results = []

    driver.get(AUTH_URL)
    input("Please complete fingerprint authentication and press Enter to continue...")

    for index, entry in enumerate(data):
        try:
            driver.execute_script("window.open('about:blank', '_blank');")
            WebDriverWait(driver, WAIT_TIMES["SHORT"] + 5).until(lambda d: len(d.window_handles) > index + 1)
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(entry["glassbox_link"])

            time.sleep(WAIT_TIMES["PAGE_LOAD"] + 10)

            entry["gia_insights"] = extract_gia_insights(driver)
            close_gia_insights(driver)

            cem_id, mcmid = extract_cookie_ids(driver)
            entry["cem_id"] = cem_id
            entry["mcmid"] = mcmid

        except Exception as e:
            print(f"Error processing link: {e}")
            entry["gia_insights"] = ""
            entry["cem_id"] = ""
            entry["mcmid"] = ""

        results.append(entry)

    driver.quit()
    return results

