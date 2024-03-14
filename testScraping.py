import unittest
import productInfo

class TestScrapingMethods(unittest.TestCase):
    def test_requestURL(self):
        self.assertEqual(productInfo.requestURL("https://otakurepublic.com/product/product_page_5741091.html")["req"].status_code, 200)

        self.assertFalse(productInfo.requestURL("https://ww.cdjapan.co.jp/")["success"])
        self.assertFalse(productInfo.requestURL("https://store.crunchyroll.coco/")["success"])


    def test_extractOrigin(self):
        self.assertEqual(productInfo.extractOrigin("https://otakurepublic.com/product/product_page_5741091.html"), "otakurepublic")
        self.assertEqual(productInfo.extractOrigin("https://www.cdjapan.co.jp/product/NEODAI-11875"), "cdjapan")
        self.assertEqual(productInfo.extractOrigin("https://www.omocat-shop.com/collections/omocat-x-hololive-en/products/holomyth-long-sleeve-shirt"), "omocat-shop")
        self.assertEqual(productInfo.extractOrigin("https://store.crunchyroll.com/products/blue-lock-bachira-meguru-pop-up-parade-4580416947268.html"), "store.crunchyroll")
        self.assertEqual(productInfo.extractOrigin("https://www.amiami.com/eng/detail?scode=FIGURE-153159&rank="), "amiami")

        self.assertNotEqual(productInfo.extractOrigin("htttttps://otakurepublic.com/product/product_page_5741091.html"), "otakurepublic")
        self.assertEqual(productInfo.extractOrigin("https://otakurepublic.coom/"), "N/A")
        self.assertNotEqual(productInfo.extractOrigin("htps:///w./www.etsy.com/"), "etsy")

    def test_otakuRepublicScrape(self):
        #Working product page
        res = productInfo.otakuRepublicScrape(productInfo.requestURL("https://otakurepublic.com/product/product_page_3456630.html?ref=drawer&type=product_matrix")["req"].text)["res"]
        self.assertEqual(res["name"], "Doujinshi - Fate/Grand Order / Gudako (female protagonist) (Smile for ●●!) / 30000℃")
        self.assertEqual(res["price"], 20.08)
        self.assertEqual(res["currency"], "USD")
        self.assertFalse(res["inStock"])
        self.assertEqual(res["url"], "https://otakurepublic.com/product/product_page_3456630.html")

        #Not a product page
        res = productInfo.otakuRepublicScrape(productInfo.requestURL("https://otakurepublic.com/product/tag_page.html?tags=343&type=header_tab")["req"].text)["success"]
        self.assertFalse(res)

        #Sister website page
        res = productInfo.otakuRepublicScrape(productInfo.requestURL("https://goodsrepublic.com/product/product_page_5642705.html?ref=cart&type=history_product")["req"].text)["res"]
        self.assertEqual(res["name"], "Osaka Shizuku & Takasaki Yu - Tapestry - NijiGaku")
        self.assertEqual(res["price"], 47.20)
        self.assertEqual(res["currency"], "USD")
        self.assertFalse(res["inStock"])
        self.assertEqual(res["url"], "https://goodsrepublic.com/product/product_page_5642705.html")

    def test_cdJapanScrape(self):
        #Working product page
        res = productInfo.cdJapanScrape(productInfo.requestURL("https://www.cdjapan.co.jp/product/TFXQ-78234")["req"].text)["res"]
        self.assertEqual(res["name"], "Midnight Grand Orchestra 1st Live \"Overture\"  Midnight Grand Orchestra Blu-ray")
        self.assertEqual(res["price"], float(6800))
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])
        self.assertEqual(res["url"], "https://www.cdjapan.co.jp/product/TFXQ-78234")
        
        #Sold out product page
        res = productInfo.cdJapanScrape(productInfo.requestURL("https://www.cdjapan.co.jp/product/NEODAI-116550")["req"].text)["res"]
        self.assertFalse(res["inStock"])

        #Not a product page
        res = productInfo.cdJapanScrape(productInfo.requestURL("https://www.cdjapan.co.jp/toys/")["req"].text)
        self.assertFalse(res["success"])

        # Invalid product side
        res = productInfo.scrapeInfo("https://www.cdjapan.co.jp/product/NEODAI-")
        self.assertFalse(res["success"])
        
    def test_aitaikujiScrape(self):
        #Working product page
        res = productInfo.aitaikujiScrape(productInfo.requestAitaikuji("https://www.aitaikuji.com/series/genshin-impact/genshin-impact-hoyoverse-official-goods-diluc-dress-shirt-black")["req"])["res"]
        self.assertEqual(res["name"], "Genshin Impact Hoyoverse Official Goods Diluc Dress Shirt Black")
        self.assertEqual(res["price"], 9500.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])
        self.assertEqual(res["url"], "https://www.aitaikuji.com/series/genshin-impact/genshin-impact-hoyoverse-official-goods-diluc-knit-sweater-1")

        #Sold out product
        res = productInfo.aitaikujiScrape(productInfo.requestAitaikuji("https://www.aitaikuji.com/genshin-impact-apex-1-7-scale-figurine-ganyu-plenilune-gaze-ver")["req"])["res"]
        self.assertFalse(res["inStock"])

        #Not a product Page
        res = productInfo.aitaikujiScrape(productInfo.requestAitaikuji("https://www.aitaikuji.com/series/kirby")["req"])
        self.assertFalse(res["success"])

    def test_estyScrape(self):
        #Working Product (multi price)
        res = productInfo.scrapeInfo("https://www.etsy.com/listing/1230404476/hololive-vtuber-hoshimachi-suisei-enamel?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=suisei&ref=sr_gallery-1-1&sts=1&organic_search_click=1&variation0=2648039902")["res"]
        self.assertEqual(res["name"], "Hololive Vtuber Hoshimachi Suisei Enamel Pin, Fan Merch")
        self.assertEqual(res["price"], 17.0)
        self.assertEqual(res["currency"], "USD")
        self.assertTrue(res["inStock"])
        self.assertEqual(res["url"], "https://www.etsy.com/listing/1230404476/hololive-vtuber-hoshimachi-suisei-enamel")
        #Image still works(checked)

        #Sold out product (singular price)
        res = productInfo.scrapeInfo("https://www.etsy.com/listing/262439329/static-noise-tee?click_key=2edd8650d19904a2c6bb557eb76b5ae89f393ec1%3A262439329&click_sum=f3890994&ref=user_profile&sts=1")["res"]
        self.assertEqual(res["price"], 35.0)
        self.assertFalse(res["inStock"])

        #Not a product page
        res = productInfo.scrapeInfo("https://www.etsy.com/people/17cbpocf/favorites/persona?ref=hp_recently_viewed_cl_recs_ref-1&anchor_to_listings=0&rerank_collection=1290886932&dataset=lw")
        self.assertFalse(res["success"])

    def test_omocatScrape(self):
        #working product
        res = productInfo.scrapeInfo("https://www.omocat-shop.com/collections/omocat-x-hololive-en/products/irys-track-jacket")["res"]
        self.assertEqual(res["name"], "IRyS Track Jacket")
        self.assertEqual(res["price"], 85.0)
        self.assertEqual(res["currency"], "USD")
        self.assertTrue(res["inStock"])
        self.assertEqual(res["url"], "https://www.omocat-shop.com/products/irys-track-jacket")
        #image works


        #sold out product
        res = productInfo.scrapeInfo("https://www.omocat-shop.com/collections/omori/products/mewo-pixel-plush")["res"]
        self.assertFalse(res["inStock"])

        #Not a product page
        res = productInfo.scrapeInfo("https://www.omocat-shop.com/collections/omori")["success"]
        self.assertFalse(res)

    def test_crunchyrollScrape(self):
        #Working product
        res = productInfo.scrapeInfo("https://store.crunchyroll.com/products/hololive-production-nekomata-okayu-pop-up-parade-4580416943994.html")["res"]
        self.assertEqual(res["name"], "Nekomata Okayu Hololive Production Pop Up Parade Figure")
        self.assertEqual(res["price"], 33.14)
        self.assertEqual(res["currency"], "USD")
        self.assertEqual(res["url"], "https://store.crunchyroll.com/products/nekomata-okayu-hololive-production-pop-up-parade-figure-4580416943994.html")
        self.assertTrue(res["inStock"])
        #Working image

        #Sold out product
        res = productInfo.scrapeInfo("https://store.crunchyroll.com/products/hololive-houshou-marine-figure-anchor-ver-4545784043172.html")["res"]
        self.assertFalse(res["inStock"])

        #Not product page
        res = productInfo.scrapeInfo("https://store.crunchyroll.com/collections/clothing/")["success"]
        self.assertFalse(res)

    def test_melonbooksScrape(self):
        #working product
        res = productInfo.scrapeInfo("https://www.melonbooks.co.jp/detail/detail.php?product_id=1721255&adult_view=1")["res"]
        self.assertEqual(res["url"], "https://www.melonbooks.co.jp/detail/detail.php?product_id=1721255")
        self.assertEqual(res["name"], "月海の果て")
        self.assertEqual(res["price"], 785.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])
        #image works

        #sold out product
        res = productInfo.scrapeInfo("https://www.melonbooks.co.jp/detail/detail.php?product_id=1628658")["res"]
        self.assertFalse(res["inStock"])

        #Not a product page
        res = productInfo.scrapeInfo("https://www.melonbooks.co.jp/comic/list.php?category_id=4")
        self.assertFalse(res["success"])

        # Invalid product side
        res = productInfo.scrapeInfo("https://www.melonbooks.co.jp/detail/detail.php?product_id=1721")
        self.assertFalse(res["success"])

    def test_goodsmileScrape(self):
        #working product
        res = productInfo.scrapeInfo("https://goodsmileshop.com/en/CATEGORY-ROOT/Goods/Code-Geass--Lelouch-of-the-Rebellion-Plushie-Lelouch-Lamperouge/p/GSC_WD_05284")["res"]
        self.assertEqual(res["url"], "https://goodsmileshop.com/en/On-Sale-Now/Available-Now/Code-Geass--Lelouch-of-the-Rebellion-Plushie-Lelouch/p/GSC_WD_05284")
        self.assertEqual(res["name"], "Code Geass: Lelouch of the Rebellion Plushie Lelouch")
        self.assertEqual(res["price"], 3080.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        #sold out product
        res = productInfo.scrapeInfo("https://goodsmileshop.com/en/On-Sale-Now/Available-Now/Shigure--Casual-Ver-/p/GSC_SCA_WD_00115")["res"]
        self.assertFalse(res["inStock"])

        #Not product page
        res = productInfo.scrapeInfo("https://goodsmileshop.com/en/CATEGORY-ROOT/Nendoroid/c/133?site=goodsmile-global&lang=en&sessionId=56480E1287294A228B4068B4DA141602.node43")
        self.assertFalse(res["success"])

    def test_hobbygenkiScrape(self):
        # Working product
        res = productInfo.scrapeInfo("https://hobby-genki.com/en/scale-figures-statues/13635-1-one-slash-ruka-kayamori-heaven-burns-red-17-scale-figure-parco-limited-4580485881012.html")["res"]
        self.assertEqual(res["url"], "https://hobby-genki.com/en/scale-figures-statues/13635-1-one-slash-ruka-kayamori-heaven-burns-red-17-scale-figure-parco-limited-4580485881012.html")
        self.assertEqual(res["name"], "1/ ONE SLASH Ruka Kayamori Heaven Burns Red 1/7 Scale Figure LIMITED")
        self.assertEqual(res["price"], 30990.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        # Sold out product
        res = productInfo.scrapeInfo("https://hobby-genki.com/en/aniplex/17720-hitori-gotoh-tsuchinoko-mendako-ver-bocchi-the-rock-deformed-figure-set-aniplex-limited.html")["res"]
        self.assertFalse(res["inStock"])

        # Not product page
        res = productInfo.scrapeInfo("https://hobby-genki.com/en/2-accueil")
        self.assertFalse(res["success"])

    def test_solarisjapanScrape(self):
        # Working Product
        res = productInfo.scrapeInfo("https://solarisjapan.com/products/kantai-collection-kan-colle-shigure-1-7-casual-ver-good-smile-company#")["res"]
        self.assertEqual(res["url"], "https://solarisjapan.com/products/kantai-collection-kan-colle-shigure-1-7-casual-ver-good-smile-company")
        self.assertEqual(res["name"], "Kantai Collection ~Kan Colle~ - Shigure - 1/7 - Casual Ver. (Good Smile Company)")
        self.assertEqual(res["price"], 83.44)
        self.assertEqual(res["currency"], "USD")
        self.assertTrue(res["inStock"])

        # Sold out product
        res = productInfo.scrapeInfo("https://solarisjapan.com/collections/figures/products/jujutsu-kaisen-sukuna-jujutsu-kaisen-jukon-no-kata-bandai-spirits#")["res"]
        self.assertFalse(res["inStock"])

        # Not product page
        res = productInfo.scrapeInfo("https://solarisjapan.com/collections/genshin-impact-figures")
        self.assertFalse(res["success"])

    def test_toranoanaScrape(self):
        # Working product page
        res = productInfo.scrapeInfo("https://ecs.toranoana.jp/tora/ec/item/040030755120/")["res"]
        self.assertEqual(res["url"], "https://ecs.toranoana.jp/tora/ec/item/040030755120/")
        self.assertEqual(res["name"], "かるいカルデア ４")
        self.assertEqual(res["price"], 785.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        # Sold out page
        res = productInfo.scrapeInfo("https://ec.toranoana.jp/tora_r/ec/item/040030247626/")["res"]
        self.assertFalse(res["inStock"])

        # Not product page
        res = productInfo.scrapeInfo("https://ecs.toranoana.jp/tora/ec/cot/")
        self.assertFalse(res["success"])

    def test_hljScrape(self):
        # Working product page
        res = productInfo.scrapeInfo("https://www.hlj.com/master-detective-archives-rain-code-plushie-shinigami-gsc19032")["res"]
        self.assertEqual(res["url"], "https://www.hlj.com/product/GSC19032/")
        self.assertEqual(res["name"], "Master Detective Archives: RAIN CODE Plushie Shinigami")
        self.assertEqual(res["price"], 4275.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        # Sold out page
        res = productInfo.scrapeInfo("https://www.hlj.com/1-8-scale-fate-grand-order-alter-ego-meltryllis-pvc-alt20617?utm_source=tumblr.com&utm_medium=social&utm_content=&utm_campaign=1/8%20Fate/Grand%20Order:%20Alter%20Ego%20Meltryllis%20PVC")["res"]
        self.assertFalse(res["inStock"])

        # Not a product page
        res = productInfo.scrapeInfo("https://www.hlj.com/")
        self.assertFalse(res["success"])

    def test_dlsiteScrape(self):
        # Working product page
        res = productInfo.scrapeInfo("https://www.dlsite.com/home/work/=/product_id/RJ295773.html/?locale=en_US")["res"]
        self.assertEqual(res["url"], "https://www.dlsite.com/home/work/=/product_id/RJ295773.html")
        self.assertEqual(res["name"], "#GensoukyouHoloism [English Ver.]")
        self.assertEqual(res["price"], 2200.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        # Not a product page
        res = productInfo.scrapeInfo("https://www.dlsite.com/home/")
        self.assertFalse(res["success"])

    def test_boothScrape(self):
        # Working product
        res = productInfo.scrapeInfo("https://booth.pm/en/items/1482245")["res"]
        self.assertEqual(res["url"], "https://booth.pm/ja/items/1482245")
        self.assertEqual(res["name"], "舞風-Maikaze Original Vocal Songs Archives 2006～2018")
        self.assertEqual(res["price"], 2480.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        # Sold out product
        res = productInfo.scrapeInfo("https://yuusa.booth.pm/items/1979778")["res"]
        self.assertFalse(res["inStock"])

        # Sold out product button disabled
        res = productInfo.scrapeInfo("https://maikazeshop.booth.pm/items/4596085")["res"]
        self.assertFalse(res["inStock"])

        # Not product page
        res = productInfo.scrapeInfo("https://booth.pm/en")
        self.assertFalse(res["success"])

        # Different price option
        res = productInfo.scrapeInfo("https://otakuhane.booth.pm/items/4815715")["res"]
        self.assertEqual(res["price"], 990.0)

    def test_bookwalkerScrape(self):
        # Working product page
        res = productInfo.scrapeInfo("https://global.bookwalker.jp/de41ac8341-d35f-41c5-b0e4-6437de32ef2a/")["res"]
        self.assertEqual(res["url"], "https://global.bookwalker.jp/de41ac8341-d35f-41c5-b0e4-6437de32ef2a/")
        self.assertEqual(res["name"], "5 Seconds Before a Witch Falls in Love")
        self.assertEqual(res["price"], 1000.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        # Not a product page
        res = productInfo.scrapeInfo("https://global.bookwalker.jp/genre/14/?np=0&page=1")
        self.assertFalse(res["success"])

    def test_usagundamstoreScrape(self):
        # Working product page
        res = productInfo.scrapeInfo("https://www.usagundamstore.com/products/fate-grand-carnival-pop-up-parade-ritsuka-fujimaru?variant=41171106758853")["res"]
        self.assertEqual(res["url"], "https://www.usagundamstore.com/products/fate-grand-carnival-pop-up-parade-ritsuka-fujimaru")
        self.assertEqual(res["name"], "Fate/Grand Carnival Pop Up Parade Ritsuka Fujimaru")
        self.assertEqual(res["price"], 29.99)
        self.assertEqual(res["currency"], "USD")
        self.assertTrue(res["inStock"])

        # Sold out product page
        res = productInfo.scrapeInfo("https://www.usagundamstore.com/products/digimon-tamers-figure-rise-standard-amplified-dukemon-gallantmon?variant=38049604337861")["res"]
        self.assertFalse(res["inStock"])

        # Not a product page
        res = productInfo.scrapeInfo("https://www.usagundamstore.com/pages/search-results-page?collection=all")
        self.assertFalse(res["success"])

    def test_surugayaScrape(self):
        # Working product page
        res = productInfo.scrapeInfo("https://www.suruga-ya.jp/product/detail/602241993")["res"]
        self.assertEqual(res["url"], "https://www.suruga-ya.jp/product/detail/602241993")
        self.assertEqual(res["name"], "駿河屋 -<新品/中古>ランサー/謎のアルターエゴ・Λ 「Fate/Grand Order」 1/7 PVC＆ABS製塗装済み完成品（フィギュア）")
        self.assertEqual(res["price"], 24500.0)
        self.assertEqual(res["currency"], "JPY")
        self.assertTrue(res["inStock"])

        # Sold out product page
        res = productInfo.scrapeInfo("https://www.suruga-ya.jp/product/detail/ZHORE196603?tenpo_cd=")["res"]
        self.assertFalse(res["inStock"])

        # Not a product page
        res = productInfo.scrapeInfo("https://www.suruga-ya.jp/")
        self.assertFalse(res["success"])

if __name__ == "__main__":
    unittest.main()