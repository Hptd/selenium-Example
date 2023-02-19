from selenium import webdriver
from selenium.webdriver.common.by import By
import time


web = webdriver.Chrome()
web.get("http://www.baidu.com/")
text_input = web.find_element(By.ID, "kw")
time.sleep(2)
text_input.send_keys("百度翻译")
time.sleep(2)
web.find_element(By.CSS_SELECTOR, "#su").click()
time.sleep(2)