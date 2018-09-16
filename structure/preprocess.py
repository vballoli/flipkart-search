import os
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def load_reviews():
        product_data = pickle.load(open('product_info.pickle', 'rb'))

        review_data = []
        for file in os.listdir('infos'):
            filename = os.fsdecode(file)
            dict = pickle.load(open('infos/'+filename, 'rb'))
            review_data.append([filename[:-7], dict])

        return review_data

def process_reviews(reviews):
    words =  [stop(stem(tokenize(clean(review)))) for review in cat(reviews)]
    return words

def cat(dict):
    full = [k+v for (k,v) in dict.items() if k != 'specs']
    return full

def clean(text):
    text = re.sub("[^A-Za-z0-9]+", ' ', text).lower()
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
