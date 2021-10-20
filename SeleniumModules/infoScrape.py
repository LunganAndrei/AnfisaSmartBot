import datetime
import time

from selenium import webdriver
import json


op = webdriver.ChromeOptions()
op.add_argument("disable-notifications")
op.add_argument("--headless")  # don t open a window
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")


class ScrapeBOT(webdriver.Chrome):
    def __init__(self,driver_path="chromedriver.exe",teardown=False):
        self.driver_path = driver_path
        self.teardown=teardown
        super(ScrapeBOT, self).__init__(options=op)
        self.implicitly_wait(10)
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def news(self,newsNumber=2):
        self.get("https://www.tion.ro/")
        title_list =self.find_elements_by_class_name("enews-article-offerer-title")
        link_list = self.find_elements_by_css_selector(".enews-article-offerer-title [href]")
        img_list = self.find_elements_by_xpath("//a/img")
        full_list=[]
        try:
            for i in range(newsNumber):
                title =title_list[i].text
                link= link_list[i].get_attribute("href")
                picture=img_list[i+2].get_attribute("data-src")

                full_list.append([title, link, picture])
            self.quit()
            return full_list
        except:
            return "None"

    def get_weather(self,city):
        try:
            self.get(f"https://www.google.ro/search?q=vremea+in+{city}")
            vremea = self.find_element_by_class_name("UQt4rd")
            imageLinks = self.find_element_by_xpath('//*[@id="wob_tci"]')
            imageNames =imageLinks.get_attribute("src")

            return [vremea.text, imageNames]
        except:
            return "None"

    def get_wikipedia_info(self,subj):
        self.get(f"https://www.google.ro/search?q=what+is+{subj}")
        try:
            title = self.find_element_by_class_name("kno-rdesc")
            return title.text
        except:
            return "None"

    def translate(self,propozitie, limba="engleza"):
        try:
            self.get(f"https://www.google.ro/search?q=traducere+{propozitie}+{limba}")
            after_translate = self.find_element_by_xpath('//*[@id="tw-target-text"]')
            return after_translate.text
        except:
            return "None"

    def exchange_money(self,suma, ffrom):
        if ffrom == "lei":
            to = "euro"
        elif ffrom == "euro":
            to = "lei"
        else:
            to = "euro"
        try:
            self.get(f"https://www.google.ro/search?q=cat+este+{suma}+{ffrom}+in+{to}")
            total = self.find_element_by_xpath(
                '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')
            return f"{suma} {ffrom} este egal cu {total.text} {to}"
        except:
            return "None"

    def get_flayer(self):
        a_file = open("SeleniumModules/products.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        result =[]
        for i in json_object["flayers"]:
            code=int(i["code"])
            try:
                self.get(i["link"])
                flyer= self.find_elements_by_css_selector(f'{i["htmlRoute"]}')
                img = self.find_elements_by_css_selector(f'{i["imgRoute"]}')
                period = self.find_elements_by_css_selector(f'{i["textRoute"]}')

                subscribers = i["subscribers"]
                name = i["name"]

                nextweek = flyer[code].get_attribute("href")
                imgLink = img[code].get_attribute("src")
                text = period[code].get_attribute("innerText")
                if i["previewsflyer"] != name:
                    result.append([name, text, nextweek, imgLink, subscribers])
            except:
                print(f'am avut eroare la {i["name"]}')

        return result



# bot = ScrapeBOT()
# print(bot.get_flayer())
# print(datetime.datetime.today().weekday())


