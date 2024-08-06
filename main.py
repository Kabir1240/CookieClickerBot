import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# time spent clicking before checking for the most expensive item you can buy
TIME_BEFORE_BUY = 5
# set up driver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)


def buy_something() -> None:
    """
    Purchases the most expensive available item on the cookie clicker website
    """
    
    # get score, and convert into an integer
    score = driver.find_element(By.ID, "cookies").text.split()
    score = "".join(score[0:2]).replace("cookies", "")
    score = convert_score_to_int(score)
    
    # find all unlocked items
    unlocked_items = driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled")
    
    # max price for comparison
    max_price = 0
    max_price_item = None
    # loop through all the items
    for item in unlocked_items:
        # convert prices of each item to integer
        item_price = item.find_element(By.CLASS_NAME, "price").text
        item_price = convert_score_to_int(item_price)
        
        # find the max price, store the item with the max price
        if item_price > max_price:
            max_price = item_price
            max_price_item = item
    
    # click the item with the highest price currently
    if max_price > 0:
        max_price_item.click()
    

def convert_score_to_int(score:str) -> int:
    """
    converts prices and scores from the cookie clicker website into integers. Accounting for all formats

    :param score: score or price
    :type score: str
    :return: score converted into integer
    :rtype: int
    """
    
    score = score.replace(",", "")
    if "million" in score:
        score.replace(" million", "")
        return int(score) * 100000
    else:
        return int(score)
    

# goto the cookie clicker site
driver.get("https://orteil.dashnet.org/cookieclicker/")
# wait 3 seconds before looking for the language prompt
time.sleep(3)
try: 
    # this prompt only shows up on the first time launching. Find prompt and choose english as the language
    lang_prompt = driver.find_element(By.CSS_SELECTOR, "#promptContent #langSelect-EN")
    lang_prompt.click()
    # sleep again, due to loading screen
    time.sleep(3)
except NoSuchElementException:
    pass
finally:
    # Initialize the last run time for buy_something
    last_run_time = time.time()
    
    # find the big cookie to click on
    big_cookie = driver.find_element(By.ID, "bigCookie")
    while True:
        # click on the cookie
        big_cookie.click()
        score = driver.find_element(By.ID, "cookies")
        
        # Get the current time
        current_time = time.time()

        # Check if designated time has passed since the last execution of command2
        if current_time - last_run_time >= TIME_BEFORE_BUY:
            buy_something()
            # Update the last run time
            last_run_time = current_time
