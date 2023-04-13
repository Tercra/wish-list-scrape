from bs4 import BeautifulSoup, SoupStrainer
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


if __name__ == "__main__":
    print(requestURL("https://otakurepublic.com/product/product_page_5741091.html"))
    print(extractOrigin("https://otakurepublic.com/product/product_page_5741091.html"))

    print(requestURL("https://ww.cdjapan.co.jp/"))