import time
import datetime
from selenium import webdriver



op = webdriver.ChromeOptions()
# op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("disable-notifications")
# op.add_argument("--headless")  # don t open a window
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")


class BookingBOT(webdriver.Chrome):
    def __init__(self,driver_path=r"chromedriver.exe"):
        self.driver_path = driver_path


        super(BookingBOT, self).__init__(options=op)
        self.implicitly_wait(15)

    def get_main_page(self):
        self.get("https://www.lastminute.ie/city-breaks/")
        try:
            acceptCookies = self.find_element_by_css_selector('button[data-qa="oil-YesButton"]')
            acceptCookies.click()
        except:
            pass
    def get_location(self,to,frrom="dublin"):
        try:
            insertFrom,insertTo = self.find_elements_by_css_selector('input[data-test="lmn-sw-input"]')
            insertFrom.send_keys(f"{frrom}")

            fromClickButton =self.find_element_by_xpath('//*[@id="hub-csw-container"]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div')
            fromClickButton.click()
            time.sleep(5)

            insertTo.send_keys(f"{to}")

            toClick = self.find_element_by_xpath('//*[@id="hub-csw-container"]/div/div/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div')
            toClick.click()
        except Exception as o:
            print(o)
            self.close()


    def get_dates(self,check_in,check_out):
        data = datetime.date.today()
        currentMonth = int(data.month)
        inList = check_in.split(" ")
        outList = check_out.split(" ")
        checkinMonth = int(inList[1])


        for i in range(checkinMonth-currentMonth-1):
            selectMonth= self.find_element_by_class_name("calendarNextMonth")
            selectMonth.click()

        dayCheckin= self.find_element_by_css_selector(f''
                                                      f'#hub-csw-container > div > div > div > div > div.lmn-sw-mainFieldsContainer > div.lmn-sw-calContainer > div > div.floatingCalendarPositioner > div > div.dropdownContent > div > div.calendarContainer '
                                                      f'> div.monthContainer.monthContainerFirst > div.monthContainerInner > div.monthDays > div:nth-child({int(inList[0])+1})')
        dayCheckin.click()

        dayCheckOut= self.find_element_by_css_selector(f''
                                                      f'#hub-csw-container > div > div > div > div > div.lmn-sw-mainFieldsContainer > div.lmn-sw-calContainer > div > div.floatingCalendarPositioner > div > div.dropdownContent > div > div.calendarContainer '
                                                      f'> div.monthContainer.monthContainerFirst > div.monthContainerInner > div.monthDays > div:nth-child({int(outList[0])+1})')

        dayCheckOut.click()

    def confirmTrip(self):
        btn = self.find_element_by_css_selector('#hub-csw-container > div > div > div > div > div.lmn-sw-submitContainer > div > div')
        btn.click()


    def returnResultList(self):
        returnList=[]
        nameList = self.find_elements_by_class_name("card__hotel-name")
        resList = self.find_elements_by_css_selector('.card__anchor[href]')
        imgList=self.find_elements_by_css_selector('img[alt="hotel-img"]')
        priceList = self.find_elements_by_class_name('card__offer-resume')
        count=0
        for i in range(2):
            name=nameList[i].text
            link=resList[i].get_attribute("href")
            picture = imgList[i+count].get_attribute("src")
            price = priceList[i].text
            priceSorted = price.replace("\\n"," ")
            count+=1
            returnList.append([name,priceSorted,link,picture])
        self.close()
        return returnList

