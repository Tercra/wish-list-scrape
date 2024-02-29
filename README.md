# wish-list scrape
A web application that allows users to add items/products using a url of a shopping website that is supported. The website keeps the compilation of items and allows users to see and organize what they want to buy in one place.


## Parts
* productinfo.py
    * Python script that scrapes info form configured websites (url, name, price, currency, image)
* testScraping.py
    * Unittest to test methods in productinfo.py
    * Test will not work in time, because certain info like price and availibility will change in time

#

### Python Dependencies
* pip install beautifulsoup4
* For selenium
    * Download a web driver (Firefox in this example https://github.com/mozilla/geckodriver/releases)
    * Extract from zip
    * Add the PATH
    * pip install selenium

