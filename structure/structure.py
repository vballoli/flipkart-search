from vector_space import VectorSpace
from preprocess import *

def prepare_search(dataset_path):
    """
    Prepares search for the Search app
    """
    print("Preparing search")
    raw_data = load_reviews(dataset_path)
    print("Len " + str(len(raw_data)))
    vector_space = VectorSpace()
    corpus_list = vector_space.generate_corpus_list(raw_data)
    vocabulary = vector_space.generate_vocabulary(corpus_list)
    frequency_matrix = vector_space.generate_frequency_matrix(vocabulary, raw_data, corpus_list)
    tf_idf_matrix = vector_space.generate_tf_idf_matrix(frequency_matrix)
    with open('tf_idf_matrix.pickle', 'wb') as f:
        pickle.dump(tf_idf_matrix, f)
        print("TF-IDF Matrix saved")
