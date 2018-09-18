import pickle
import os
import sys
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
import time

root_dir = os.getcwd()
sys.path.insert(0, root_dir)

from structure.helper import *
from structure.structure import *

class PhoneGUI(Frame):
    """
    Constructs GUI Window
    """

    def __init__(self, dataset_path):
        super().__init__()
        self.dataset_path = dataset_path
        self.results = []
        with open('structure/corpus_list.pickle', 'rb') as f:
            cl = pickle.load(f)
        with open(root_dir + "/structure/tf_idf_matrix.pickle", 'rb') as f:
            tf_idf_matrix = pickle.load(f)
        self.tf_idf_matrix = tf_idf_matrix
        self.cl = cl
        self.initUI()

    def get_result(self, frames, entry, dataset_path):
        for frame in frames:
            frame.pack_forget()
        self.results = search(qin=entry.get(), dataset_path=dataset_path, cl=self.cl, tf_idf_matrix=self.tf_idf_matrix)
        self.initUI()

    def initUI(self):

        self.master.title("Mobile Search")
        self.pack(fill=BOTH, expand=True)

        self.master.iconbitmap(root_dir + "/search/favicon.ico")

        search_frame = ttk.Frame(self)
        search_frame.pack(fill=X)

        res_frame = ttk.Frame(self)
        res_frame.pack(fill=BOTH, expand=True)

        search_field = ttk.Entry(search_frame, font='Calibri 12', background='gray25')
        search_field.pack(fill=BOTH, padx=5, pady=5, expand=True, side=LEFT)

        search_btn = ttk.Button(search_frame, text="Search", width=5,
         command=lambda: self.get_result([search_frame, res_frame], search_field, dataset_path=self.dataset_path))
        search_btn.pack(side=LEFT, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(res_frame)
        scrollbar.pack(side=RIGHT, fill=Y, pady=5)

        res_txt = Text(res_frame, yscrollcommand=scrollbar.set, wrap=WORD, background='gray25')
        res_txt.pack(fill=BOTH, pady=5, padx=5, expand=True, ipadx=5, ipady=5)

        scrollbar.config(command = res_txt.yview)

        for result in self.results:
            res_txt.insert(END, result + '\n\n')
            res_txt.tag_add("result", '1.0', 'end')
        res_txt.pack()

        res_txt.tag_config("result", font='Calibri 13 ', foreground='white')


def search(qin, K=10, dataset_path=None, cl=None, tf_idf_matrix=None):
    """
    Processes the query(qin) and returns result
    """
    try:
        if os.path.isfile(root_dir + "/structure/tf_idf_matrix.pickle"):
            document_list = os.listdir(root_dir + '/scraping/flipkart/infos')
            print("Data loaded")
        else:
            matrix_time = time.time()
            prepare_search(dataset_path)
            print("Building matrices finished in: " + str(time.time() - matrix_time))
            with open(root_dir + "/structure/tf_idf_matrix.pickle", 'rb') as f:
                tf_idf_matrix = pickle.load(f)
            document_list = os.listdir(root_dir + '/scraping/flipkart/infos')
            print("Data loaded")

    except Exception as e:
        print("Exception")
        pass

    while (True):
        query_time = time.time()
        query = qin
        if query != "exit<>" and query != "||K||":
            query = stop(stem(tokenize(clean(query))))
            print(query)
            score = []
            N = len(tf_idf_matrix[list(tf_idf_matrix.keys())[0]])
            for _ in range(N):
                score.append(0)
            results = []
            try:
                for term in query:
                    wtq = query.count(term)
                    for i in range(N):
                        wtd = tf_idf_matrix[term][i]
                        score[i] += wtd * wtq
            except KeyError as e:
                results.append("No results found for " + qin)
                return results

            for i in range(N):
                score[i] = score[i] / len(cl[i])  # Score normalization according to corresponding document

            prev = None
            for highscore in sorted(score, reverse=True)[:K]:  # Retrieve sorted scores in descending order
                device_name = document_list[score.index(highscore)]
                print(str(device_name).strip(".pickle") + get_sentiment(device_name))
                if device_name != prev:
                    results.append(str(device_name).strip(".pickle") + get_sentiment(device_name))
                    prev = device_name
            print("Search time: " + str(time.time() - query_time))
            return results
        elif query == "exit<>":
            exit()
        else:
            K = input("Enter K: ")
            search(K=int(K))


def run_gui(K=10, dataset_path=None):
    """
    Starts the GUI for search
    """
    try:
        if os.path.isfile(root_dir + "/structure/tf_idf_matrix.pickle"):
            root = tk.ThemedTk()
            root.get_themes()
            root.set_theme('black')
            root.geometry("600x300")
            app = PhoneGUI(dataset_path)
            root.mainloop()
        else:
            prepare_search(dataset_path)
            run_gui(dataset_path=dataset_path)
    except Exception as e:
        pass
