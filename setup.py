import os
import importlib
from zipfile import ZipFile

cur_dir = os.getcwd()

def modules():
    """
    Checks for required modules and module data
    """
    if importlib.util.find_spec("scrapy") is not None:
        if importlib.util.find_spec("nltk") is not None:
            if importlib.util.find_spec("sklearn") is not None:
                dataset()
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
    from search.app import run_gui
    os.chdir(cur_dir)
    try:
        print("Checking for dataset")
        if os.listdir(cur_dir + '/scraping/flipkart').index('infos'):
            if len(os.listdir(cur_dir + '/scraping/flipkart/infos')) > 0:
                run_gui(dataset_path=cur_dir + '/scraping/flipkart/infos')
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
    if os.path.isfile(cur_dir + '/sentiment/Amazon_Unlocked_Mobile.csv'):
        pass
    else:
        with ZipFile(cur_dir + '/sentiment/Amazon_Unlocked_Mobile.csv.zip', 'r') as zip:
            zip.extractall("sentiment/")

    print("Looking for existing classifier")
    try:
        if os.path.isfile(cur_dir + '/sentiment/sentiment_clf.pickle') and os.path.isfile(cur_dir + '/sentiment/vect.pickle'):
            print("Found classifier")
        else:
            print("Classifier not found. Pretraining...")
            os.system('python ' + cur_dir + '/sentiment/classifier.py')
    except Exception as e:
        pass

if __name__=='__main__':
    print("Starting")
    train_classifier()
    #modules()
    dataset()
