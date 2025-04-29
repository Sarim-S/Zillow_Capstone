from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep


ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfg0lMB30XDPG0vgLYy5nZXQWTtU_33cpueq4yCqOZEiI-SBA/viewform?pli=1"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=ZILLOW_URL)

price_text = []
urls = []
addresses = []

prices = driver.find_elements(By.CLASS_NAME, value="PropertyCardWrapper__StyledPriceLine")

price_text = [price.text for price in prices]
for price in price_text:
    if "+" in price:
        formatted_price = price.split("+")[0]
        price_text[price_text.index(price)] = formatted_price
    elif "/" in price:
        formatted_price = price.split("/")[0]
        price_text[price_text.index(price)] = formatted_price


url_elements = driver.find_elements(By.CLASS_NAME, value="StyledPropertyCardDataArea-anchor")
urls = [url.get_attribute("href") for url in url_elements]

address_elements = driver.find_elements(By.CSS_SELECTOR, value="address")
addresses = [address.text for address in address_elements]


for i in range(len(price_text)):

    driver.get(FORM_URL)

    address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.click()
    sleep(0.5)
    address_input.send_keys(addresses[i])

    price_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.click()
    sleep(0.5)
    price_input.send_keys(price_text[i])

    url_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    url_input.click()
    sleep(0.5)
    url_input.send_keys(urls[i])

    submit = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()

driver.quit()