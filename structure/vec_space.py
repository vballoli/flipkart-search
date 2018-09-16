from preprocess import *
from helper import *
import pickle
from math import log, log10

raw_data = load_reviews()

all_words = []
for i in range(len(raw_data)):
    review_voc = process_reviews(raw_data[i][1])
    specs_voc = process_specs(raw_data[i][1]['specs'])
    name_voc = process_title(raw_data[i][0])
    all_words.append(name_voc + specs_voc + review_voc)

vocab = []
N = len(all_words)
for product_words in all_words:
    vocab += product_words

vocab = list(set(vocab))

del product_words

frequency_matrix = dict()

for word in vocab:
    frequency_matrix[word] = []
    for i in range(len(raw_data)):
        product_words = all_words[i]
        occurences = 0
        for product_word in product_words:
            if (product_word == word):
                occurences += 1
        frequency_matrix[word].append(occurences)

tfidf_mat = frequency_matrix
score = []
for term in frequency_matrix:
    row = frequency_matrix[term]
    idf = log10(N/(N - row.count(0)))
    for i in range(N):
        score.append(0)
        tfidf_mat[term][i] = log(1+frequency_matrix[term][i])*idf

del frequency_matrix

print("Enter query")
query = input()

query = stop(stem(tokenize(clean(query))))

for term in query:
    wtq = query.count(term)
    for i in range(N):
        wtd = tfidf_mat[term][i]
        score[i] += wtd * wtq

for i in range(N):
    score[i] = score[i] / N

for highscore in sorted(score, reverse=True)[:10]:
    print(highscore)
    print(all_words[score.index(highscore)])
