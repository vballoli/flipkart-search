# CS F469 - Information Retrieval Assignment

## Get the dataset

Software requirements: `python3` and `pip`

Run the following in the rootdir/ 

1. `pip3 install -r requirements.txt`

Run the following in rootdir/scraping/flipkart/

2. `scrapy crawl FlipkartProduct`

3. `scrapy crawl ProductSpider`

4. `scrapy crawl ReviewSpider`

Check for the pickles of each item in a dictionary {review title: review content} in the scraping/flipkart/infos



