from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
import base64
import json
import requests
import re

def requestURL(url):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    try:
        req = requests.get(url, headers=header)
    except:
        print(f"Invalid url: {url}")
        return {"success" : False}
    else:
        return {"success" : True, "req":req}

def requestAitaikuji(url):
    try:
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        options.set_capability("pageLoadStrategy", "eager")
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        html = driver.page_source
    except:
        print(f"Invalid url: {url}")
        return {"success" : False}
    else:
        return {"success" : True, "req":html}
    finally:
        driver.quit()

def extractOrigin(url):     #Can return None if no match
    m = re.search(r"^(https://)?(www\.)?(\S+?)\.(com|co\.jp)", url)

    if m is None:
        return "N/A"

    return m.group(3)

#Scraping info from otaku republic and sister sites
def otakuRepublicScrape(html):
    metaTags = SoupStrainer("meta")
    soup = BeautifulSoup(html, "html.parser", parse_only=metaTags)
    if(soup.find("meta", property="og:type")["content"] != "product"):
        return {"success" : False}

    # Scraping info from the meta tags
    res = {}
    res["url"] = soup.find("meta", property="og:url")["content"]
    res["name"] = soup.find("meta", property="og:title")["content"]
    res["price"] = float(soup.find("meta", property="og:price:amount")["content"])
    res["currency"] = soup.find("meta", property="og:price:currency")["content"]
    if(soup.find("meta", property="og:availability")["content"] == "instock"):      #preorders are also listed as instock
        res["inStock"] = True
    else:
        res["inStock"] = False
    
    #requestImage
    imgURL = soup.find("meta", property="og:image")["content"].removesuffix(".l_thumbnail.webp")
    # img = base64.b64encode(requestURL(imgURL)["req"].content)
    img = "data:image/jpeg;base64," + base64.b64encode(requestURL(imgURL)["req"].content).decode("utf-8")
    res["img"] = img

    return {"success" : True, "res" : res}

#Scraping info from CDJapan
def cdJapanScrape(html):
    soup = BeautifulSoup(html, "html.parser")

    res = {}
    res["url"] = soup.find("meta", property="og:url")["content"]
    #Checking if the url is a product page
    if(res["url"].find("cdjapan.co.jp/product/") < 0):
        return {"success" : False}

    res["name"] = soup.find("meta", property="og:title")["content"].strip()
    res["price"] = float(soup.find("span", itemprop="price")["content"])
    res["currency"] = "JPY"
    if(soup.find("a", href="https://www.cdjapan.co.jp/guide/help/shipping/when_will_my_order_ship").get_text().strip() == "Sold Out"):
        res["inStock"] = False
    else:
        res["inStock"] = True
    
    #Request Image
    imgURL = soup.find("meta", property="og:image")["content"]
    img = "data:image/jpeg;base64," + base64.b64encode(requestURL(imgURL)["req"].content).decode("utf-8")
    res["img"] = img

    return {"success" : True, "res" : res}

#Scraping info from Aitaikuji
def aitaikujiScrape(html):
    soup = BeautifulSoup(html, "html.parser")

    res = {}
    temp = soup.find("meta", property="og:type")
    #Cheking if url is product page
    if(temp is None or temp["content"] != "og:product"):
        return {"success" : False}

    res["url"] = soup.find("meta", property="og:url")["content"]
    res["name"] = soup.find("meta", property="og:title")["content"]
    res["price"] = float(soup.find("meta", property="product:price:amount")["content"])
    res["currency"] = soup.find("meta", property="product:price:currency")["content"]
    if(soup.find("div", title="Availability")["class"][1] == "available"):
        res["inStock"] = True
    else:
        res["inStock"] = False

    #Request Image
    imgURL = soup.find("meta", property="og:image")["content"]
    img = "data:image/jpeg;base64," + base64.b64encode(requestURL(imgURL)["req"].content).decode("utf-8")
    res["img"] = img

    return {"success" : True, "res" : res}

#Scraping info from Etsy (Doesn't work well with options + out of stock)
def etsyScrape(html):
    soup = BeautifulSoup(html, "html.parser", parse_only=SoupStrainer("script"))
    infoJSON = soup.find("script", type="application/ld+json")

    if(infoJSON is None):
        return {"success" : False}
        
    infoJSON = json.loads(infoJSON.get_text())
    res = {}
    res["url"] = infoJSON["url"]
    res["name"] = infoJSON["name"]
    if("highPrice" in infoJSON["offers"].keys()):
        res["price"] = float(infoJSON["offers"]["highPrice"])
    else:
        res["price"] = float(infoJSON["offers"]["price"])
    res["currency"] = infoJSON["offers"]["priceCurrency"]
    res["inStock"] =  (infoJSON["offers"]["availability"] == "https://schema.org/InStock")

    #Requesting Image
    if(type(infoJSON["image"]) is list):
        imgURL = infoJSON["image"][0]["contentURL"]
    else:
        imgURL = infoJSON["image"]
    img = "data:image/jpeg;base64," + base64.b64encode(requestURL(imgURL)["req"].content).decode("utf-8")
    res["img"] = img

    return {"success" : True, "res" : res}

#Scraping info from omocat
def omocatScrape(html):
    soup = BeautifulSoup(html, "html.parser")

    #check if product page
    if(soup.find("meta", property="og:type")["content"] != "product"):
        return {"success" : False}
    
    res = {}
    infoJSON = soup.find("script", class_="product-json").get_text()
    infoJSON = json.loads(infoJSON)
    soup = BeautifulSoup(html, "html.parser", parse_only=SoupStrainer("meta"))
    res["url"] = soup.find("meta", property="og:url")["content"]
    res["name"] = infoJSON["title"]
    res["price"] = float(soup.find("meta", property="og:price:amount")["content"])
    res["currency"] = soup.find("meta", property="og:price:currency")["content"]
    res["inStock"] = infoJSON["available"]

    #Request Image
    # imgURL = infoJSON["featured_image"]
    imgURL = soup.find("meta", property="og:image")["content"]
    img = "data:image/jpeg;base64," + base64.b64encode(requestURL(imgURL)["req"].content).decode("utf-8")
    res["img"] = img

    return {"success" : True, "res" : res}


SCRAPEMETHODS = {
    "aitaikuji" : requestAitaikuji
}

ORIGINS = {
    "otakurepublic" : otakuRepublicScrape,
    "goodsrepublic" : otakuRepublicScrape,
    "japanese-snacks-republic" : otakuRepublicScrape,
    "cdjapan" : cdJapanScrape,
    "aitaikuji" : aitaikujiScrape,
    "etsy" : etsyScrape,
    "omocat-shop" : omocatScrape
}

def scrapeInfo(url):
    #Check if url is valid and if origin is part of configured sites
    origin = extractOrigin(url)
    if(origin == "N/A" or origin not in ORIGINS.keys()):
        return {"success" : False}

    if(origin in SCRAPEMETHODS.keys()):
        reqResponse = SCRAPEMETHODS[origin](url)
        info = ORIGINS[origin](reqResponse["req"])
    else:
        reqResponse = requestURL(url)

        if(not reqResponse["success"]):
            return {"success" : False}

        info = ORIGINS[origin](reqResponse["req"].text)

    if(info["success"]):
        return {"success" : True, "res" : info["res"]}
    
    return {"success" : False}
    


if __name__ == "__main__":
    # pass
    # req = requestAitaikuji("https://www.aitaikuji.com/series/genshin-impact/genshin-impact-hoyoverse-official-goods-diluc-dress-shirt-black")["req"]
    # print(req)
    x = scrapeInfo("https://www.omocat-shop.com/collections/omocat-x-hololive-en/products/tsukumo-sana-varsity-jacket")
    print(x)
    # with open("./test.txt", "w") as f:
    #     f.write(x["res"]["img"])