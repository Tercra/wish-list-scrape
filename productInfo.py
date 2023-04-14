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

    return {"success" : False, "req":None}

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
    if(soup.find("meta", property="og:availability")["content"] == "instock"):
        res["inStock"] = True
    else:
        res["inStock"] = False
    
    #requestImage
    imgURL = soup.find("meta", property="og:image")["content"].removesuffix(".l_thumbnail.webp")
    # img = base64.b64encode(requestURL(imgURL)["req"].content)
    img = "data:image/jpeg;base64," + base64.b64encode(requestURL(imgURL)["req"].content).decode("utf-8")
    res["img"] = img

    return {"success" : True, "res" : res}


if __name__ == "__main__":
    req = requestURL("https://otakurepublic.com/product/product_page_5741091.html")["req"]
    print(extractOrigin("https://otakurepublic.com/product/product_page_5741091.html"))
    print(otakuRepublicScrape(req.text))