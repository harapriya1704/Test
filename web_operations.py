# web_operations.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import WAIT_TIMES, AUTH_URL
import time

def extract_gia_insights(driver):
    try:
        print("Waiting for page to fully load...")
        WebDriverWait(driver, WAIT_TIMES["PAGE_LOAD"]).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Check for iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"Found {len(iframes)} iframes, switching to first iframe")
            driver.switch_to.frame(iframes[0])

        print("Clicking GIA Insights button...")
        gia_button = WebDriverWait(driver, WAIT_TIMES["GIA_LOAD"]).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'GIA Insights')]"))
        )
        driver.execute_script("arguments[0].click();", gia_button)
        print("GIA Insights button clicked")

        print("Waiting for insights container...")
        insights_container = WebDriverWait(driver, WAIT_TIMES["GIA_LOAD"]).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'insights-body')]"))
        )

        previous_length = 0
        stable_count = 0
        max_wait = WAIT_TIMES["GIA_LOAD"] * 2
        start_time = time.time()

        while time.time() - start_time < max_wait:
            current_text = driver.execute_script("return arguments[0].innerText;", insights_container)
            current_length = len(current_text)

            if current_length == previous_length:
                stable_count += 1
            else:
                stable_count = 0
                previous_length = current_length

            if stable_count >= 3:
                break

            time.sleep(1)

        print(f"Extracted GIA Insights ({len(current_text)} characters)")
        return current_text

    except Exception as e:
        print("GIA Insights extraction failed:", str(e))
        return ""

def close_gia_insights(driver):
    print("Attempting to close GIA Insights popover...")
    try:
        # Try closing using the close button
        close_btn = WebDriverWait(driver, WAIT_TIMES["SHORT"]).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
        )
        close_btn.click()
        print("✅ Closed GIA Insights popover using close button")
        time.sleep(2)
        return True
    except Exception:
        try:
            print("Trying fallback: clicking GIA Insights button...")
            toggle_btn = WebDriverWait(driver, WAIT_TIMES["SHORT"]).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'GIA Insights')]"))
            )
            toggle_btn.click()
            print("✅ Closed GIA Insights popover by toggling button")
            time.sleep(2)
            return True
        except Exception as e:
            print("❌ Failed to close GIA Insights popover:", str(e))
            return False

def extract_cookie_ids(driver):
    try:
        print("Attempting to extract cookie IDs...")
        
        # Switch back to default content in case we were in an iframe
        driver.switch_to.default_content()
        
        # Try to find the cookie table without clicking anything first
        try:
            print("Looking for cookie table without clicking...")
            WebDriverWait(driver, WAIT_TIMES["COOKIE_EXTRACTION"]).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@title, 'DellCEMSessionCookie')]"))
            )
        except TimeoutException:
            print("Cookie table not found, trying to reveal it...")
            try:
                cross_icon = WebDriverWait(driver, WAIT_TIMES["COOKIE_EXTRACTION"]).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'Close')]"))
                )
                cross_icon.click()
                print("Clicked icon to reveal cookie table")
                time.sleep(3)
            except Exception:
                print("Could not find reveal icon, proceeding anyway")

        print("Extracting cookie values...")
        cem_span = WebDriverWait(driver, WAIT_TIMES["COOKIE_EXTRACTION"]).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@title, 'DellCEMSessionCookie')]"))
        )
        mcmid_span = WebDriverWait(driver, WAIT_TIMES["COOKIE_EXTRACTION"]).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@title, 'MCMID')]"))
        )

        cem_id = cem_span.get_attribute("title")
        mcmid = mcmid_span.get_attribute("title")

        print(f"✅ Extracted CEM ID: {cem_id}")
        print(f"✅ Extracted MCMID: {mcmid}")

        return cem_id, mcmid

    except Exception as e:
        print("❌ Cookie extraction failed:", str(e))
        return "", ""

def process_glassbox_links(data):
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    results = []

    print("Loading authentication URL...")
    driver.get(AUTH_URL)
    input("Please complete fingerprint authentication and press Enter to continue...")

    # Create main window handle reference
    main_window = driver.current_window_handle

    for index, entry in enumerate(data):
        try:
            print(f"\nProcessing entry {index+1}/{len(data)}: {entry['order_number']}")
            
            # Open new tab
            driver.execute_script("window.open('about:blank', '_blank');")
            WebDriverWait(driver, WAIT_TIMES["SHORT"]).until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            
            print(f"Loading Glassbox link: {entry['glassbox_link']}")
            driver.get(entry["glassbox_link"])
            
            # Wait for page to load
            time.sleep(WAIT_TIMES["PAGE_LOAD"] // 2)
            WebDriverWait(driver, WAIT_TIMES["PAGE_LOAD"]).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Process the page
            entry["gia_insights"] = extract_gia_insights(driver)
            close_gia_insights(driver)
            
            # Switch back to default content before cookie extraction
            driver.switch_to.default_content()
            
            cem_id, mcmid = extract_cookie_ids(driver)
            entry["cem_id"] = cem_id
            entry["mcmid"] = mcmid

        except Exception as e:
            print(f"⚠️ Error processing {entry['order_number']}: {e}")
            entry["gia_insights"] = ""
            entry["cem_id"] = ""
            entry["mcmid"] = ""
        finally:
            results.append(entry)
            print(f"Completed processing {entry['order_number']}")
            
            # Close current tab and switch back to main window
            if len(driver.window_handles) > 1:
                driver.close()
            driver.switch_to.window(main_window)
            time.sleep(2)  # Pause between sessions

    driver.quit()
    return results
