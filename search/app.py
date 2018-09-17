import pickle
import os
import sys

root_dir = os.getcwd()
sys.path.insert(0, root_dir)

from structure.helper import *

def search(K=10, dataset_path=None):
    """
    Search app
    """
    try:
        if os.listdir(root_dir + '/structure').index("tf_idf_matrix.pickle") is not None:
            with open(root_dir + "/structure/tf_idf_matrix.pickle", 'rb') as f:
                tf_idf_matrix = pickle.load(f)
            document_list = os.listdir(root_dir + '/scraping/flipkart/infos')
        else:
            prepare_search(dataset_path)
            search()
    except Exception as e:
        pass
    while (True):
        print("Enter Query \n"
            + "Default Result length = 10. To change, type '||K||'(without '') . \n"
            + "Type '||exit||' (without '') to exit.")
        query = input(">> ")
        if query != "||exit||" and query != "||K||":
            query = stop(stem(tokenize(clean(query))))
            print(query)
            score = []
            N = len(tf_idf_matrix[list(tf_idf_matrix.keys())[0]])
            print("N in app" + str(N))
            for _ in range(N):
                score.append(0)
            try:
                for term in query:
                    print(term)
                    wtq = query.count(term)
                    for i in range(N):
                        wtd = tf_idf_matrix[term][i]
                        score[i] += wtd * wtq
            except KeyError as e:
                print("No results found")
                search(K)

            for i in range(N):
                score[i] = score[i] / N
                print(score[i])
            print("K" + str(K))
            for highscore in sorted(score, reverse=True)[:K]:
                print(str(document_list[score.index(highscore)]).strip(".pickle"))
        elif query == "||exit||":
            exit()
        else:
            K = input("Enter K ")
            search(K=int(K))

if __name__=="__main__":
    search()
