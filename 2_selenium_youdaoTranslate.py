from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# 隐藏浏览器，不用打开浏览器后台运行
Chrome_options = Options()
Chrome_options.add_argument('--headless')
web = webdriver.Chrome(options=Chrome_options)
# 当页面没有刷新完成之前，等待时常。适用于全局等待，只要界面没刷新出来就一直等待。
web.implicitly_wait(0.5)
web.get("https://fanyi.youdao.com/")
# 传入要翻译的词
web.find_element(By.CSS_SELECTOR, "#js_fanyi_input").send_keys("this is test Text!")
trans_btn = web.find_element(By.CSS_SELECTOR, "#TextTranslate > div.source > div.sourceAction > div > div.opt-right.yd-form-container > a")
trans_btn.click()
trans_text = web.find_element(By.CSS_SELECTOR, "#js_fanyi_output_resultOutput > p > span").text
print(trans_text)
web.quit()
