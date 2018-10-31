from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re

def cat(dict):
    """
    Returns concatenated review title and review content
    """
    full = [k+" "+v for (k,v) in dict.items() if k != 'specs']
    return full

def clean(text):
    """
    Strips the text of special characters
    """
    text = re.sub("\W+", ' ', text).lower()
    return text

def tokenize(text):
    """
    Returns stripped text.
    """
    tokens = word_tokenize(text)
    return tokens

def stem(words):
    """
    Returns list of stemmed(Porter Stemmer) words.
    """
    stemmer = PorterStemmer()
    stems = list(set([stemmer.stem(word) for word in words]))
    return stems

def stop(words):
    """
    Removes list of words removing common stop words.
    """
    stop_words = stopwords.words('english')
    return [word for word in words if word not in stop_words]
