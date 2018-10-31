import os
import importlib
from zipfile import ZipFile
import time

cur_dir = os.getcwd()

def modules():
    """
    Checks for required modules and module data
    """
    if importlib.util.find_spec("scrapy") is not None:
        if importlib.util.find_spec("nltk") is not None:
            if importlib.util.find_spec("sklearn") is not None:
                dataset()
                return
    try:
        modules_time = time.time()
        print("Installing missing modules")
        os.system('pip3 install -r requirements.txt')
        if importlib.util.find_spec("ntlk.tokenize") is None or importlib.util.find_spec("ntlk.stem") is None:
            os.system("python3 -c 'nltk.download('punkt')'")
            os.system("python3 -c 'nltk.download('stopwords')'")
        print("Modules installation finished in: " + str(time.time() - modules_time))
        start_scrape()
    except Exception as e:
        print("pip3 install -r requirements.txt failed. Install pip3 and try again.")


def start_scrape():
    """
    Scrapes data from Flipkart
    """
    print("Fetching dataset ...")
    os.chdir('scraping/flipkart')
    scrape_time = time.time()
    os.system('scrapy crawl FlipkartProduct')
    os.system('scrapy crawl ProductSpider')
    os.system('scrapy crawl ReviewSpider')
    print("Scraping finished in: " + str(time.time() - scrape_time))
    train_classifier()

def dataset():
    """
    Checks scraped dataset
    """
    from search.app import run_gui
    os.chdir(cur_dir)
    try:
        print("Checking for dataset")
        if os.listdir(cur_dir + '/scraping/flipkart').index('infos'):
            if len(os.listdir(cur_dir + '/scraping/flipkart/infos')) > 0:
                run_gui(dataset_path=cur_dir + '/scraping/flipkart/infos')
                return
            else:
                print("Dataset does not exist")
                start_scrape()
    except ValueError as e:
        print("Dataset doesn't exist")
        start_scrape()

def train_classifier():
    """
    Trains Sentiment Analysis Classifier
    """
    print("Looking for classifier")
    try:
        if os.path.isfile(cur_dir + '/sentiment/sentiment_clf.pk') and os.path.isfile(cur_dir + '/sentiment/vect.pk'):
            print("Found classifier")
            dataset()
        else:
            print("Classifier not found. Pretraining...")
            os.system('python ' + cur_dir + '/sentiment/classifier.py')
    except Exception as e:
        pass

if __name__=='__main__':
    print("Starting")
    modules()
