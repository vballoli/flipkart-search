import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

dataframe = pd.read_csv('sentiment/Amazon_Unlocked_Mobile.csv')

dataframe = dataframe.sample(frac=0.1,random_state=10)
dataframe.dropna(inplace=True)

dataframe = dataframe[dataframe['Rating']!=3 ]

dataframe['positive'] = np.where(dataframe['Rating']>3.5, 1, 0)

x_train,x_test,y_train,y_test = train_test_split(dataframe['Reviews'], dataframe['positive'], random_state=0)

vectorizer = CountVectorizer()
vectorizer.fit(x_train)
x_train_vec = vectorizer.transform(x_train)
x_test_vec = vectorizer.transform(x_test)

model = RandomForestClassifier(n_estimators=10)
model.fit(x_train_vec, y_train)

pickle.dump(vectorizer, open("sentiment/vect.pickle", "wb"))
pickle.dump(model, open("sentiment/sentiment_clf.pickle", 'wb'))
