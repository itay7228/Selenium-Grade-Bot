# This bot checks the MoE's website for new Bagrut grades, and notifies you via telegram if there are any.
# Please note that in order to use this code, one must configure telegram-send on one's pc (and thereby create the
# Telegram bot).


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import telegram_send
import time

Chrome_path = "C:\\Users\\itays\\Documents\\chromedriver_win32\\chromedriver"


def check_grades(grade):
    # This function checks the website for a change in the number of grades.
    browser = reach_web_page()
    for i in range(50):
        # A new window is opened every 50 refreshes in order to prevent chromedriver from running out of memory.
        # The time.sleep functions prevents the bot from giving a false positive and spitting an exceptiom,
        # as it cannot detect the element while the page is loading. It also moderates the frequency
        # of the grade checking.
        time.sleep(30)
        new_grade = get_number_of_grades(browser)
        if new_grade != grade:
            print(new_grade)
            telegram_send.send(messages=["יש ציונים?"])
            telegram_send.send(messages=["!*"])
            break
        browser.refresh()
    browser.quit()


def reach_web_page():
    # This functions creates the webdriver instance and reaches the Bagrut grades web page.
    options = Options()
    options.add_argument("--window-position=2560,0")
    # The options are used in order to place the window in my second monitor (on the right-hand side of the main 1440p).
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.maximize_window()
    browser.get("https://students.education.gov.il/matriculation-exams/grades")
    browser.find_element("xpath", "/html/body/app-root/div[1]/div/div/tlm-header/header/div/div[2]/a[1]").click()
    browser.find_element("xpath", "/html/body/app-root/div[1]/div/div/tlm-header/header/div/div[2]/div[1]/div[1]"
                                  "/a").click()
    browser.find_element("xpath", "/html/body/section/div[1]/div[3]/div[1]").click()
    browser.find_element("xpath", "/html/body/section/div[1]/div[3]/form/fieldset/input[2]").send_keys(sys.argv[1])
    browser.find_element("xpath", "/html/body/section/div[1]/div[3]/form/fieldset/span/input[4]").send_keys(sys.argv[2])
    browser.find_element("xpath", "/html/body/section/div[1]/div[3]/form/fieldset/button").click()
    return browser


def get_number_of_grades(browser):
    # This function gets the number of grades from the website (in order to check if it has changed).
    grade_board = browser.find_element("xpath", "/html/body/app-root/div[1]/div/daf-sherut-page-layout/div/div[2]/"
                                                "section[1]/grades-wrapper/div/div/all-grades/div/ul/li[1]/button")
    return grade_board.get_attribute("innerHTML")


def main():
    # First, we get the initial number of grades, then start to check it periodically for changes.
    browser = reach_web_page()
    time.sleep(30)
    # The time.sleep functions prevents the bot from giving a false positive and spitting an exceptiom,
    # as it cannot detect the element while the page is loading.
    grade = get_number_of_grades(browser)
    browser.quit()
    while True:
        try:
            check_grades(grade)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    main()



