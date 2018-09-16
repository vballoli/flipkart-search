import os
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def load_reviews():
    """
    Loads dataset from infos folder
    """
    product_data = []
    for file in os.listdir('../scraping/flipkart/infos'):
        filename = os.fsdecode(file)
        dict = pickle.load(open('../scraping/flipkart/infos/'+filename, 'rb'))
        product_data.append([filename[:-7], dict])

    return product_data

def process_reviews(reviews):
    """
    Input: dict of reviews
    Ouptput: list containing stemmed reviews
    """
    words = []
    for review in cat(reviews):
        words = words + stop(stem(tokenize(clean(review))))
    return words

def process_specs(specs):
    """
    Input: list of product specs
    Output: list of stemmed specs
    """
    words = []
    for spec in specs:
        words = words + stop(stem(tokenize(clean(spec))))
    return words

def process_title(product_name):
    """
    Input: Product Name / Title
    Output: Tokenized product title
    """
    return tokenize(clean(product_name))

def cat(dict):
    full = [k+v for (k,v) in dict.items() if k != 'specs']
    return full

def clean(text):
    text = re.sub("\W+", ' ', text).lower()
    return text

def tokenize(text):
    tokens = word_tokenize(text)
    return tokens

def stem(words):
    stemmer = PorterStemmer()
    stems = list(set([stemmer.stem(word) for word in words]))
    return stems

def stop(words):
    stop_words = stopwords.words('english')
    return [word for word in words if word not in stop_words]
