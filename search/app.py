import pickle
import os
import sys
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk

root_dir = os.getcwd()
sys.path.insert(0, root_dir)

from structure.helper import *
from structure.structure import *

class PhoneGUI(Frame):
    """
    GUI Window
    """

    def __init__(self, dataset_path):
        super().__init__()

        self.dataset_path = dataset_path
        self.results = []
        self.initUI()

    def get_result(self, frames, entry, dataset_path):
        for frame in frames:
            frame.pack_forget()
        self.results = search(qin=entry.get(), dataset_path=dataset_path)
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


def search(qin, K=10, dataset_path=None):
    """
    Search app
    """
    try:
        if os.path.isfile(root_dir + "/structure/tf_idf_matrix.pickle"):
            with open(root_dir + "/structure/tf_idf_matrix.pickle", 'rb') as f:
                tf_idf_matrix = pickle.load(f)
            document_list = os.listdir(root_dir + '/scraping/flipkart/infos')
            print("Data loaded")
        else:
            prepare_search(dataset_path)
            search()
    except Exception as e:
        pass

    while (True):
        print("Enter Query \n"
            + "Current max result length = "+ str(K) +". To change, type '||K||'(without '') . \n"
            + "Type 'exit<>' (without '') to exit.")
        query = qin
        if query != "exit<>" and query != "||K||":
            query = stop(stem(tokenize(clean(query))))
            print(query)
            score = []
            N = len(tf_idf_matrix[list(tf_idf_matrix.keys())[0]])
            print("N in app: " + str(N))
            for _ in range(N):
                score.append(0)
            try:
                for term in query:
                    wtq = query.count(term)
                    for i in range(N):
                        wtd = tf_idf_matrix[term][i]
                        score[i] += wtd * wtq
            except KeyError as e:
                print("No results found")
                search(K)

            for i in range(N):
                score[i] = score[i] / N
            #print("Number of results: " + str(K) + '\n')
            prev = None
            results = []
            for highscore in sorted(score, reverse=True)[:K]:
                device_name = document_list[score.index(highscore)]
                if device_name != prev:
                    results.append(str(device_name).strip(".pickle") + get_sentiment(device_name))
                    #print(str(device_name).strip(".pickle") + get_sentiment(device_name))
                    prev = device_name
            return results
        elif query == "exit<>":
            exit()
        else:
            K = input("Enter K: ")
            search(K=int(K))


def run_gui(K=10, dataset_path=None):
    root = tk.ThemedTk()
    root.get_themes()
    root.set_theme('black')
    root.geometry("600x300")
    app = PhoneGUI(dataset_path)
    root.mainloop()

if __name__=="__main__":
    run_gui()
