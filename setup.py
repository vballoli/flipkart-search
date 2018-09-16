import os
import importlib


def modules():
    if importlib.util.find_spec("scrapy") is not None:
        if importlib.util.find_spec("nltk") is not None:
            dataset()
            return
    try:
        print("Installing missing modules")
        os.system('pip3 install -r requirements.txt')
    except Exception as e:
        print("pip3 install -r requirements.txt failed. Install pip3 and try again.")


def start_scrape():
    print("Fetching dataset ...")
    os.system('scrapy crawl FlipkartProduct')
    os.system('scrapy crawl ProductSpider')
    os.system('scrapy crawl ReviewSpider')

def dataset():
    try:
        print("Checking for dataset")
        if os.listdir(os.curdir + '/scraping/flipkart').index('infos'):
            if len(os.listdir(os.curdir + '/scraping/flipkart/infos')) > 0:
                print("Starting the search engine")
            else:
                print("Dataset does not exist")
                start_scrape()
    except ValueError as e:
        print("Dataset doesn't exist")
        start_scrape()

if __name__=='__main__':
    print("Starting")
    modules()
