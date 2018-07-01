from selenium import webdriver
import os

driver = webdriver.Chrome(os.getenv('HOME') + '/dev/caguete/uf/chromedriver')

# open website
driver.get("https://google.com")

# get the text
print("Text retrieved : "+ driver.find_element_by_link_text("Sobre").text)

# close browser
driver.close()
