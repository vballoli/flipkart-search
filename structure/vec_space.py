import preprocess as pre
import pickle

raw_data = pre.load_reviews()

vocab = []
for i in range(len(raw_data)):
    review_voc = pre.process_reviews(raw_data[i][1])
    specs_voc = pre.process_specs(raw_data[i][1]['specs'])
    name_voc = pre.process_title(raw_data[i][0])
    vocab = vocab + name_voc + specs_voc + review_voc

print(len(vocab))
