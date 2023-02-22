import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

driver = webdriver.Chrome()
driver.get('https://www.nike.com/pl/t/buty-dunk-low-next-nature-DbG5gV/DN1431-002')
time.sleep(1)

elem_list = driver.find_element(By.CSS_SELECTOR,"#buyTools > div:nth-child(1) > fieldset > div > div:nth-child(1) > label")
print(elem_list.text)

