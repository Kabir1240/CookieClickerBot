import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)


def buy_something():
    score = driver.find_element(By.ID, "cookies").text.split()
    score = "".join(score[0:2]).replace("cookies", "")
    score = convert_score_to_int(score)
    
    unlocked_items = driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled")
    
    max_price = 0
    max_price_item = None
    for item in unlocked_items:
        item_price = item.find_element(By.CLASS_NAME, "price").text
        item_price = convert_score_to_int(item_price)
        
        if item_price > max_price:
            max_price = item_price
            max_price_item = item
    
    if max_price > 0:
        max_price_item.click()
    

def convert_score_to_int(score):
    score = score.replace(",", "")
    if "million" in score:
        score.replace(" million", "")
        return int(score) * 100000
    else:
        return int(score)
    
    
driver.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(3)
try: 
    lang_prompt = driver.find_element(By.CSS_SELECTOR, "#promptContent #langSelect-EN")
    lang_prompt.click()
    time.sleep(3)
except NoSuchElementException:
    pass
finally:
    # Initialize the last run time for buy_something
    last_run_time = time.time()
    
    big_cookie = driver.find_element(By.ID, "bigCookie")
    while True:
        big_cookie.click()
        score = driver.find_element(By.ID, "cookies")
        
        # Get the current time
        current_time = time.time()

        # Check if 5 seconds have passed since the last execution of command2
        if current_time - last_run_time >= 5:
            buy_something()
            # Update the last run time
            last_run_time = current_time
