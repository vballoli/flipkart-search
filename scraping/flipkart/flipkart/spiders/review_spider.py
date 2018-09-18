import os
import pickle
import scrapy

class ReviewSpider(scrapy.Spider):
    name="ReviewSpider"

    def __init__(self):
        self.base_url = "https://www.flipkart.com"
        self.length = 0
        self.count = 0
        self.specs = []

    def start_requests(self):
        os.mkdir('infos')
        with open('product_info.pickle', 'rb') as f:
            product_info = pickle.load(f)
            urls = []
            self.length  = len(product_info)
            for product in product_info:
                if str(product[3]).find('None') < 0:
                    urls.append(product[3])
                    self.specs.append(product[4])

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            product_name = response.selector.xpath('//div[@class="_1SFrA2"]/span/text()').extract_first()
            product_name = str(product_name)
            product_rating = response.selector.xpath('//div[@class="niH0FQ _36Fcw_"]/span/div/text()').extract_first()
            print(product_rating)
            product_price = response.selector.xpath('//div[@class="_1vC4OE"]/text()').extract_first()
            product_price = str(product_price)
            review_titles = response.selector.xpath('//div[@class="col _390CkK"]/div/p/text()').extract()
            print(review_titles)
            review_contents = response.selector.xpath('//div[@class="col _390CkK"]/div/div/div/div/text()').extract()
            print(review_contents)
            d = dict()
            product_specs = self.specs[self.count]
            self.count += 1
            for i in range(len(review_titles)):
                d[review_titles[i]] = review_contents[i]
            d['specs'] = product_specs
            with open('infos/' + product_name + " " + product_price + '.pickle', 'wb') as p:
                pickle.dump(d, p)

        except Exception as e:
            print(e)
            pass
