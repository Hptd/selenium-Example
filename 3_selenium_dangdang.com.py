from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from PIL import Image
from io import BytesIO


class DangdangBookPrice(object):
    def __init__(self):
        self.excel_path = "F:/临时文件夹/当当网数据下载/"
        self.book_type = input("你想获得哪类书的信息：")
        self.page = int(input("你想过爬取多少页信息："))

    def manage_web_message(self):
        web_dangdang = webdriver.Chrome()
        web_dangdang.implicitly_wait(20)
        web_dangdang.get("https://dangdang.com/")

        web_dangdang.find_element(By.CSS_SELECTOR, "#key_S").send_keys(self.book_type)
        web_dangdang.find_element(By.CSS_SELECTOR, "#form_search_new > input.button").click()

        wb = Workbook()
        sheet = wb.active
        sheet["A1"].value = "封面"
        sheet["B1"].value = "书名"
        sheet["C1"].value = "当前价格"
        sheet["D1"].value = "原始价格"

        j = 1
        for i in range(0, self.page):
            shop_list = web_dangdang.find_elements(By.XPATH, "/html/body/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/ul/li")
            for li in shop_list:
                # 反爬机制，每一页的第一个图片与后面的链接不同。
                if li == shop_list[0]:
                    book_img_src = li.find_element(By.CSS_SELECTOR, "a > img").get_attribute("src")
                else:
                    book_img_src = li.find_element(By.CSS_SELECTOR, "a > img").get_attribute("data-original")
                    book_img_src = "http:" + book_img_src
                book_name = li.find_element(By.CSS_SELECTOR, "a").get_attribute("title")
                book_price_new = li.find_element(By.CSS_SELECTOR, ".search_now_price").text
                book_price_old = li.find_element(By.CSS_SELECTOR, ".search_pre_price").text

                # 图片
                img_resp = requests.get(book_img_src)
                img = Image.open(BytesIO(img_resp.content))
                # 调整列宽
                sheet.column_dimensions['A'].width = img.width * 0.15
                # 调整行高
                sheet.row_dimensions[j+1].height = img.height * 0.8
                excel_img = ExcelImage(img)
                sheet.add_image(excel_img, f'A{j + 1}')

                cell_B = "B" + str(j + 1)
                cell_B = sheet[cell_B]
                cell_B.value = book_name

                cell_C = "C" + str(j + 1)
                cell_C = sheet[cell_C]
                cell_C.value = book_price_new

                cell_D = "D" + str(j + 1)
                cell_D = sheet[cell_D]
                cell_D.value = book_price_old

                print(f"已经获取 {j} 条信息。")

                j += 1

            next_page = web_dangdang.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div[1]/div[5]/div[2]/div/ul/li[10]/a")
            next_page.click()
            time.sleep(2)
        wb.save(self.excel_path + f"img_excel_{self.book_type}.xlsx")
        print("Done.")
        web_dangdang.quit()


if __name__ == '__main__':
    DangdangBookPrice().manage_web_message()
