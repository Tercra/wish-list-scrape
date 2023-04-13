import unittest
import productInfo

class TestScrapingMethods(unittest.TestCase):
    def test_requestURL(self):
        self.assertEqual(productInfo.requestURL("https://otakurepublic.com/product/product_page_5741091.html")["req"].status_code, 200)

        self.assertEqual(productInfo.requestURL("https://ww.cdjapan.co.jp/")["success"], False)
        self.assertEqual(productInfo.requestURL("https://store.crunchyroll.coco/")["success"], False)


    def test_extractOrigin(self):
        self.assertEqual(productInfo.extractOrigin("https://otakurepublic.com/product/product_page_5741091.html"), "otakurepublic")
        self.assertEqual(productInfo.extractOrigin("https://www.cdjapan.co.jp/product/NEODAI-11875"), "cdjapan")
        self.assertEqual(productInfo.extractOrigin("https://www.omocat-shop.com/collections/omocat-x-hololive-en/products/holomyth-long-sleeve-shirt"), "omocat-shop")
        self.assertEqual(productInfo.extractOrigin("https://store.crunchyroll.com/products/blue-lock-bachira-meguru-pop-up-parade-4580416947268.html"), "store.crunchyroll")
        self.assertEqual(productInfo.extractOrigin("https://www.amiami.com/eng/detail?scode=FIGURE-153159&rank="), "amiami")

        self.assertNotEqual(productInfo.extractOrigin("htttttps://otakurepublic.com/product/product_page_5741091.html"), "otakurepublic")
        self.assertEqual(productInfo.extractOrigin("https://otakurepublic.coom/"), "N/A")
        self.assertNotEqual(productInfo.extractOrigin("htps:///w./www.etsy.com/"), "etsy")
        
        
if __name__ == "__main__":
    unittest.main()