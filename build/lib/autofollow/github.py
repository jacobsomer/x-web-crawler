from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def login(driver, username, password):
    driver.get("https://github.com/login")
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "login_field"))).send_keys(username)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "commit"))).click()
    except TimeoutException:
        print("Login failed, check your credentials. Assuming already logged in.")
        
def follow_users(driver, page_number=0, url=None, username_password=None, duration=300):
    if username_password:
        login(driver, username_password[0], username_password[1])

    page = page_number

    for _ in range(4):  # Adjust the number of iterations as needed
        if page == 0:
            driver.get(url)
        else:
            driver.get(f"{url}?page={page}")
        
        start_time = time.time()  # Start time for 20 seconds duration

        while time.time() - start_time < 20:  # Run for 20 seconds
            time.sleep(2)
            try:
                # Wait for all follow buttons to be visible
                follow_buttons = WebDriverWait(driver, 3).until(
                    EC.visibility_of_any_elements_located(
                        (By.XPATH, "//input[@value='Follow']")
                    )
                )

                # Check each button to see if it's actionable
                actionable_buttons = [
                    btn for btn in follow_buttons
                    if btn.is_enabled() and btn.is_displayed()
                ]

                # Click all actionable "Follow" buttons
                for button in actionable_buttons:
                    button.click()

                # Check if there were any buttons to click, if not, just go next
                if not actionable_buttons:
                    print("No actionable 'Follow' buttons, clicking 'Next'.")

                # Attempt to click 'Next' page button
                next_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@rel='next']"))
                )
                next_page.click()
            except TimeoutException:
                # If 'Next' button is not clickable or not found, break the loop
                print("No more pages to navigate or no 'Next' button found.")
                next_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@rel='next']"))
                )
                next_page.click()
            except NoSuchElementException:
                # If no 'Next' button is found but page loaded, also break
                print("Reached the last page.")
                break

        print(f"Page {page}, Page {page + 1}, and Page {page + 2} completed.")
        print("Waiting for 1 minute before next iteration.")
        time.sleep(60)  # Wait for 1 minute before next iteration
        page += 3

    # Quit the driver after all iterations are done
    driver.quit()
