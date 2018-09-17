import os
import importlib

from search.app import search

cur_dir = os.curdir

def modules():
    """
    Checks for required modules and module data
    """
    if importlib.util.find_spec("scrapy") is not None:
        if importlib.util.find_spec("nltk") is not None:
            dataset()
            return
    try:
        print("Installing missing modules")
        os.system('pip3 install -r requirements.txt')
        if importlib.util.find_spec("ntlk.tokenize") is None or importlib.util.find_spec("ntlk.stem") is None:
            os.system("python3 -c nltk.download('punkt')")
            os.system("python3 -c nltk.download('stopwords')")
        start_scrape()
    except Exception as e:
        print("pip3 install -r requirements.txt failed. Install pip3 and try again.")


def start_scrape():
    """
    Scrapes data from Flipkart
    """
    print("Fetching dataset ...")
    os.chdir('scraping/flipkart')
    os.system('scrapy crawl FlipkartProduct')
    os.system('scrapy crawl ProductSpider')
    os.system('scrapy crawl ReviewSpider')
    dataset()

def dataset():
    """
    Checks scraped dataset
    """
    os.chdir(cur_dir)
    try:
        print("Checking for dataset")
        if os.listdir(os.curdir + '/scraping/flipkart').index('infos'):
            if len(os.listdir(os.curdir + '/scraping/flipkart/infos')) > 0:
                search(dataset_path=os.curdir + '/scraping/flipkart/infos')
            else:
                print("Dataset does not exist")
                start_scrape()
    except ValueError as e:
        print("Dataset doesn't exist")
        start_scrape()

if __name__=='__main__':
    print("Starting")
    modules()
