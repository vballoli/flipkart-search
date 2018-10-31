from .preprocess import *
from .helper import *
import pickle
from math import log, log10

class VectorSpace:

    def __init__(self):
        self.N = 0

    def generate_corpus_list(self, raw_data):
        """
        Return list of all terms in each document
        """
        print("Generating formatable corpus")
        corpus_list = []
        for i in range(len(raw_data)):
            review_voc = process_reviews(raw_data[i][1])
            specs_voc = process_specs(raw_data[i][1]['specs'])
            name_voc = process_title(raw_data[i][0])
            corpus_list.append(name_voc + specs_voc + review_voc)
        print("Corpus generated")
        return corpus_list

    def generate_vocabulary(self, corpus_list):
        """
        Returns list of set of vocabulary from te documents
        """
        print("Building corpus vocabulary")
        vocabulary = []
        N = len(corpus_list)
        self.N = N
        for document_terms in corpus_list:
            vocabulary += document_terms
        print("Vocabulary built")
        return list(set(vocabulary))

    def generate_frequency_matrix(self, vocabulary, raw_data, corpus_list):
        """
        Generates and returns Frequency matrix of each term in vocabulary in the corpus data
        """
        print("Constructing Frequency Matrix")
        print(self.N)
        frequency_matrix = dict()
        for word in vocabulary:
            frequency_matrix[word] = []
            for i in range(len(raw_data)):
                product_words = corpus_list[i]
                occurences = 0
                for product_word in product_words:
                    if (product_word == word):
                        occurences += 1
                frequency_matrix[word].append(occurences)
        print("Frequency Matrix constructed!")
        return frequency_matrix

    def generate_tf_idf_matrix(self, frequency_matrix):
        """
        Generates and returns TF-IDF matrix from the input Frequency Matrix
        """
        print("Constructing TF-IDF matrix")
        N = self.N
        print("N in tfidf " + str(N))
        tfidf_matrix = frequency_matrix
        score = []
        for term in frequency_matrix:
            row = frequency_matrix[term]
            idf = log10(N/(N - row.count(0)))
            for i in range(N):
                score.append(0)
                tfidf_matrix[term][i] = log(1+frequency_matrix[term][i])*idf
        print("TF-IDF Matrix constructed")
        return tfidf_matrix
