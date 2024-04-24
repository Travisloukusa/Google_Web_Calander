import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def scrape(user, password):
    # Set the webdriver
    driver = webdriver.Safari()
    driver.implicitly_wait(20)  # seconds

    # Open the SCSU login website
    driver.get("https://www.stcloudstate.edu/advisingdays/d2l-login.aspx")

    # Send username to input field
    elem = driver.find_element(By.ID, "userName")
    elem.send_keys(user)

    # Send password to input field
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, "password"))).send_keys(password)

    # Send enter key to submit the form and open D2L website
    elem.send_keys(webdriver.Keys.RETURN)

    time.sleep(10)

    for window in driver.window_handles:
        driver.switch_to.window(window)

    # Navigate directly to calendar
    driver.get("https://stcloudstate.learn.minnstate.edu/d2l/le/calendar/1")

    for window in driver.window_handles:
        driver.switch_to.window(window)

    assignments = []
    assignments_list = driver.find_elements(By.CSS_SELECTOR, ".d2l-datalist-item.d2l-datalist-item-actionable.d2l-datalist-checkboxitem")

    for assignment in assignments_list:
        assignment = assignment.find_element(By.CLASS_NAME, "d2l-datalist-item-content")
        title = assignment.get_attribute("title")
        class_name = assignment.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > .d2l-offscreen").text
        due_date = assignment.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(2) > div:nth-child(1)").text
        assignments.append({"Title": title, "Class": class_name, "Due Date": due_date})

    driver.quit()
    return json.dumps(assignments)


if __name__ == '__main__':
    data = scrape("user","password")
    print(data)

