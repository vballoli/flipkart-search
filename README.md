# CSF469 Information Retrieval Assignment
Aim: Implement a Vector Space model based search.

This project aims to implement an unbiased search across mobiles on Flipkart
including: `Reviews and Specs` thus differing in the usual biased search
off the website.

## Run the app

Software requirements: `python3` and `pip`

Run `python3 setup.py`

Note: Downloading dataset will take time

## Implementation
1. Each document contains the information, specs and reviews of all products scraped from Flipkart.
2. Content of all the reviews will be lemmatized, stop words will be removed and specs will be structured in a certain format.
3. Posting list of each word will be constructed.
4. Sentiment analysis model will be trained on a certain dataset and each document's combined review content is reviewed and sentiment is stored in a table according to the document.
5. According to the query, postings list is fetched -> Vectorized query and word -> scores calculated -> top 10 scores returned with an average sentiment analysis of the documents returned

## Statistics

On running this software on an Early 2015 Macbook Air(8 GB RAM):

1. Scrape time - 180s (subject to network)
2. Data preprocessed and Matrices generation - 26s
3. Average search time - 0.9s

` Note: There's a delay in the search since the reviews are also passed through
the pre-trained sentiment analysis model.`
