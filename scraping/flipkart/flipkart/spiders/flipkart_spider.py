import scrapy
import pickle

class FlipkartProductSpider(scrapy.Spider):
    """
    Runs a spider that retrieves all the urls of the phones sold on flipkart from the search page
    """
    name="FlipkartProduct"

    def __init__(self):
        self.base_url = "https://www.flipkart.com"
        self.begin_url = "https://www.flipkart.com/search?q=mobile&sid=tyy/4io&as=on&as-show=on&marketplace=FLIPKART&otracker=AS_QueryStore_OrganicAutosuggest_1_5&otracker1=AS_QueryStore_OrganicAutosuggest_1_5&as-pos=1&as-type=Top&as-backfill=on"
        self.product_urls = []
        self.count = 0

    def start_requests(self):
        yield scrapy.Request(url=self.begin_url, callback=self.parse)

    def parse(self, response):
        next_class = "_3fVaIS"
        product_class = "_31qSD5"
        for product_href in list(response.css("a." +product_class+"::attr(href)").extract()):
            self.product_urls.append(product_href)
        print("Count == " + str(self.count))
        self.count = self.count + 1
        next_page = list(response.css("a." + next_class+"::attr(href)").extract())
        if len(next_page) != 0:
            next_page = next_page.pop()
            next_page = self.base_url + next_page
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        else:
            url_products_file = "product_urls.pickle"
            print("Size " + str(len(self.product_urls)))
            product_file = open(url_products_file, 'wb')
            pickle.dump(self.product_urls, product_file)
            product_file.close()
