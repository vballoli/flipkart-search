import scrapy
import pickle
import os

class ProductSpider(scrapy.Spider):
	"""
	Runs a spider for product url and fetches specs, ratings, and full review links.
	"""
	name="ProductSpider"


	def __init__(self):
		self.base_url = "https://www.flipkart.com"
		self.ratings_class = "_2_KrJI" #div
		self.review_title_class = "_2xg6Ul" #p
		self.review_content_class = "qwjRop" #div
		self.product_title_class = "_35KyD6" #span
		self.product_price_parent_class = "_1uv9Cb"
		self.product_price_class = "_1vC4OE _3qQ9m1"
		self.count = 0
		self.product_info_list = []

	def start_requests(self):
		with open('product_urls.pickle', 'rb') as f:
			product_endpoints = pickle.load(f)
			self.count = len(product_endpoints)
			urls = []
			for p_url in product_endpoints:
				urls.append(self.base_url + str(p_url))
			for url in urls:
				yield scrapy.Request(url=url, callback=self.parse)



	def parse(self, response):
		product_title = str(response.css("h1." + "_9E25nV" + " span." + self.product_title_class + "::text").extract_first())
		product_rating = str(response.selector.xpath('//span[@class="_2_KrJI"]/div/text()').extract_first())
		product_price = str(response.selector.xpath('//div[@class="_1uv9Cb"]/div/text()').extract_first())
		product_review_url = self.base_url + str(response.selector.xpath('//div[@class="col _39LH-M"]/a/@href').extract_first())
		product_specs = list(response.selector.xpath('//div[@class="_3WHvuP"]/ul/li/text()').extract())
		print(product_review_url)
		self.product_info_list.append([product_title, product_price, product_rating, product_review_url, product_specs])
		print("Count == " + str(self.count))
		print("List len " + str(len(self.product_info_list)))
		if self.count == len(self.product_info_list):
			with open('product_info.pickle', 'wb') as p:
				pickle.dump(self.product_info_list, p)
