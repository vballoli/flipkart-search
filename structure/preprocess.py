import os
import pickle
from .helper import *


def load_reviews(dataset_path):
    """
    Loads dataset from infos folder
    """
    print("Loading data")
    product_data = []
    for file in os.listdir(dataset_path):
        filename = os.fsdecode(file)
        dict = pickle.load(open(dataset_path + '/' +filename, 'rb'))
        product_data.append([filename[:-7], dict])
    print("Successfully loaded!")
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
