from bs4 import BeautifulSoup, SoupStrainer
import base64
import requests
import re

def requestURL(url):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    try:
        req = requests.get(url, headers=header)
    except:
        print(f"Invalid url: {url}")
    else:
        return {"success" : True, "req":req}

    return {"success" : False}

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


ORIGINS = {
    "otakurepublic" : otakuRepublicScrape,
    "goodsrepublic" : otakuRepublicScrape,
    "japanese-snacks-republic" : otakuRepublicScrape,
    "cdjapan" : cdJapanScrape
}

def scrapeInfo(url):
    #Check if url is valid and if origin is part of configured sites
    origin = extractOrigin(url)
    if(origin == "N/A" or origin not in ORIGINS.keys()):
        return {"success" : False}

    reqResponse = requestURL(url)

    if(not reqResponse["success"]):
        return {"success" : False}

    info = ORIGINS[origin](reqResponse["req"].text)

    if(info["success"]):
        return {"success" : True, "res" : info["res"]}
    
    return {"success" : False}
    


if __name__ == "__main__":
    # req = requestURL("https://otakurepublic.com/product/product_page_5741091.html")["req"]
    # print(extractOrigin("https://otakurepublic.com/product/product_page_5741091.html"))
    # print(otakuRepublicScrape(req.text))
    # print(scrapeInfo("https://otakurepublic.com/product/product_page_5741091.html"))
    print(scrapeInfo("https://www.cdjapan.co.jp/product/NEODAI-116550"))
