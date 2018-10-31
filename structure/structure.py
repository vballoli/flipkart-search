from .vector_space import VectorSpace
from .preprocess import *
from scipy import stats
import time

def prepare_search(dataset_path):
    """
    Prepares search for the Search app
    """
    print("Preparing search")
    generation_time = time.time()
    raw_data = load_reviews(dataset_path)
    print("Len " + str(len(raw_data)))
    vector_space = VectorSpace()
    corpus_list = vector_space.generate_corpus_list(raw_data)
    vocabulary = vector_space.generate_vocabulary(corpus_list)
    frequency_matrix = vector_space.generate_frequency_matrix(vocabulary, raw_data, corpus_list)
    tf_idf_matrix = vector_space.generate_tf_idf_matrix(frequency_matrix)
    with open('structure/tf_idf_matrix.pickle', 'wb') as f:
        pickle.dump(tf_idf_matrix, f)
        print("TF-IDF Matrix saved")
    for i in range(len(corpus_list)):
        corpus_list[i] = list(set(corpus_list[i]))
    with open('structure/corpus_list.pickle', 'wb') as f:
        pickle.dump(corpus_list, f)
        print("Corpus list saved")
    print("Matrices generated in: " + str(time.time() - generation_time))

def get_sentiment(device_name):
    """
    Returns sentiment for a particular phone
    """
    classifier = pickle.load(open('sentiment/sentiment_clf.pk', 'rb'))
    vectorizer = pickle.load(open('sentiment/vect.pk', 'rb'))
    try:
        with open('scraping/flipkart/infos/' + device_name, 'rb') as file:
            dict = pickle.load(file)
            for key in dict.keys():
                if key != 'specs':
                    reviews = [dict[key] for key in dict.keys() if key != 'specs']
                    reviews_vec = vectorizer.transform(reviews)
                    sentiments = classifier.predict(reviews_vec)
                    if stats.mode(sentiments)[0] == 1:
                        return " - Generally postive reviews"
                    elif stats.mode(sentiments)[0] == 0:
                        return " - Generally negative reviews"
    except Exception as e:
        return " - " + str(e)
