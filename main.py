import time
from selenium import  webdriver
from selenium.webdriver.common.by import By


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://python.org")
# time.sleep(2)
menu = driver.find_element(By.CSS_SELECTOR, ".medium-widget.event-widget.last div.shrubbery ul.menu")
dates = [date.text for date in menu.find_elements(By.TAG_NAME, "time")]
titles = [title.text for title in menu.find_elements(By.TAG_NAME, "a")]

events = {}
for num in range(len(dates)):
    events[num] = \
        {
            "time":dates[num],
            "name":titles[num],
        }

print(events)