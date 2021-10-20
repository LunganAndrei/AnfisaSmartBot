import json
import time
import os
from selenium import webdriver

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("disable-notifications")
# op.add_argument("--headless")  # don t open a window
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")

class GroceryALDI(webdriver.Chrome):
    def __init__(self,driver_path=r"chromedriver.exe"):
        self.driver_path = driver_path


        super(GroceryALDI, self).__init__(options=op)
        self.implicitly_wait(15)

    def get_main_page(self):
        self.get("https://deliveroo.ie/menu/dublin/santry-demesne/aldi-santry")

    def cookies(self):
        try:
            btnMenu=self.find_element_by_css_selector('body > div:nth-child(48) > div > div > div > div.ccl-c0cfdd4489ca1c33 > div > span:nth-child(2) > button')
            btnMenu.click()
        except:
            pass
        try:
            whereBtn = self.find_element_by_css_selector('body > div:nth-child(47) > div > div > div > div.ccl-9bcf8db942e088a2.ccl-afd7f53ad24cb4ea > div > div.ccl-b5a044c3742b89f4 > div > div:nth-child(3) > button')
            whereBtn.click()
        except:
            pass
        try:

            cookiesBtn = self.find_element_by_css_selector('body > div.optanon-alert-box-wrapper > div.optanon-alert-box-bg > div.optanon-alert-box-button-container > div.optanon-alert-box-button.optanon-button-allow > div > button')
            cookiesBtn.click()
        except:
            pass

    def get_productList(self):
        nameList = self.find_elements_by_css_selector('p[class="ccl-19882374e640f487 ccl-1daa0367dee37c3b ccl-a5fb02a1085896d3 ccl-dd90031787517421 ccl-9d0a5327c911d0f3"]')
        # descriptionList = self.find_elements_by_css_selector('p[class="ccl-19882374e640f487 ccl-417df52a76832172 ccl-dfaaa1af6c70149c ccl-9d0a5327c911d0f3 ccl-c8eb8fd8fb351d32"]')
        priceList =self.find_elements_by_css_selector('span[class="UIMenuItemCard-132307914e856acc"]')
        time.sleep(5)
        imgList= self.find_elements_by_css_selector('div[class="ccl-45bd106b75353ec9"]')
        time.sleep(5)
        fullProductList =[]
        count=0
        for i in range(len(nameList)):
            price = priceList[i].text
            name = nameList[i].text
            img = imgList[i+1].get_attribute("style")     # currently nesolved

            fullProductList.append([count,name,price])
            count+=1
        return fullProductList
    def findProductByName(self,productName):
        pass


bot = GroceryALDI()
bot.get_main_page()
bot.cookies()
bot.get_productList()
