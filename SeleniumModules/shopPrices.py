import json
import time
import os
from selenium import webdriver

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("disable-notifications")
op.add_argument("--headless")  # don t open a window
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")

#  driver.implicitly_Wait(seconds)

#  driver.find_element_by_css_selector("button[onclick='examplename()']")
def get_details(link):
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=op)
    driver.get(link)
    driver.implicitly_wait(5)
    name=link
    try:
        product_id = driver.find_element_by_xpath(
            '//*[@id="main-container"]/section[1]/div/div[1]/div[2]/div[1]').text
        id = product_id[12:]
    except Exception as o:
        id = 0
        print(name)
        print(o)
    # get Name
    try:
        product_title = driver.find_element_by_xpath(
            '//*[@id="main-container"]/section[1]/div/div[1]/h1').text
        name = product_title[0:50]
    except Exception as o:
        print(name)
        print(o)
        name = 0
    # get Price
    try:
        product_price = driver.find_element_by_css_selector('#main-container > section:nth-child(1) > div > div.row > div.col-sm-5.col-md-7.col-lg-7 > div > div > div.col-sm-12.col-md-6.col-lg-5 > form > div.product-highlight.product-page-pricing > div:nth-child(1) > div > div.pricing-block.has-installments > p.product-new-price.has-deal').text
        newP = int(product_price[0:-6].replace(".", ""))   #
    except Exception as o:
        print(name)
        print(o)
        newP = 0
    try:
        resigilatdriver = driver.find_element_by_css_selector(
            "#main-container > section:nth-child(1) > div > div.row > div.col-sm-5.col-md-7.col-lg-7 > div > div > div.col-sm-12.col-md-6.col-lg-5 > div.highlights-resealed-panel > div > div.panel-body > div > p.product-new-price").text
        newR = int(resigilatdriver[0:-6].replace(".", ""))
    except:
        newR = 0

    return [id,name,newP,newR]




def follow_product(link, userID):
    id, name, newP, newR = get_details(link)
    a_file = open("SeleniumModules/products.json", "r")
    json_object = json.load(a_file)
    a_file.close()



    new_link = {
        "link": f"{link}",
        "name": name,
        "id": id,
        "price": newP,
        "resigilat": newR,
        "user": userID

    }

    json_object["product"].append(new_link)

    a_file = open("SeleniumModules/products.json", "w")
    json.dump(json_object, a_file)
    a_file.close()
    return "I will let you know when the price drops "


def unfollow_product(nameList):
    try:
        a_file = open("SeleniumModules/products.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        count = 0
        print(nameList)
        for i in json_object["product"]:
            if nameList in i["name"]:
                json_object["product"].pop(count)
                a_file = open("SeleniumModules/products.json", "w")
                json.dump(json_object, a_file)
                a_file.close()
                return "unsubscribe successfully"
            else:
                count += 1


        return "check the name again"
    except:
        return "check the name again"



def price_scrape():
    global name, id, newR
    a_file = open("SeleniumModules/products.json", "r")
    json_temp = json.load(a_file)
    a_file.close()

    count = 0
    for i in json_temp["product"]:

        link ,price,resigilat,userID= i["link"],i["price"],i["resigilat"],i["user"]
        id, name, newP, newR = get_details(link)
        if price != newP or resigilat != newR:

            new_dict = {
                "link": link,
                "name": name,
                "id": id,
                "price": newP,
                "resigilat": newR,
                "user": userID
            }

            json_temp["product"][count] = new_dict

            a_file = open("SeleniumModules/products.json", "w")
            json.dump(json_temp, a_file)
            a_file.close()

            count+=1
            if newP == price:
                pass
            if newP > price:
                price = newP
                return [f" PRICE for {name} grew to {newP} Ron",userID]
            elif newP < price:
                price = newP
                return [f"PRICE for {name} decreased to {newP} Ron",userID]
            else:
                pass

            if newR == resigilat:
                pass
            elif newR > resigilat:
                resigilat = newR
                return [f"RESEALED for {name} grew to {newR} Ron",userID]
            elif newR < resigilat:
                resigilat = newR
                return [f"RESEALED for {name} decreased to {newR} Ron",userID]
            else:
                resigilat = newR
        else:

            count += 1


 # print(get_details("https://www.emag.ro/laptop-ultraportabil-asus-zenbook-duo-14-ux482ea-cu-procesor-intelr-coretm-i7-1165g7-pana-la-4-70-ghz-14-full-hd-touch-32gb-1tb-ssd-intelr-iris-xe-graphics-windows-10-pro-celestial-blue-ux482ea-hy029r/pd/D14F1DMBM/"))