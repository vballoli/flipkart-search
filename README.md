# CSF469 Information Retrieval Assignment
Aim: Implement a Vector Space model based search.

This project aims to implement an unbiased search across Flipkart for mobiles, taking into considerations their
reviews and specifications thus offering an alternative to the default site search, which is biased towards newly released models.

## Run the app

Software requirements: `python3` and `pip`

Run `python3 setup.py`

Note: Downloading the dataset might take time depending on your internet connection.

## Implementation
1. Each document contains the information, specifications, and reviews of all products scraped from Flipkart.
2. The content of all the reviews will be lemmatized, stop words will be removed and structured in a certain format.
3. Posting list of each word will be constructed.
4. Sentiment analysis model will be trained on a certain dataset and each document's combined review content is used to assign a sentiment rating.
5. According to the query, the postings list is fetched. The application returns the top 10 results along with their sentiment ratings.

## Statistics

On running this software on an Early 2015 Macbook Air(8 GB RAM):

1. Scrape time - 180s (subject to network speed)
2. Data preprocessed and Matrices generation - 26s
3. Average search time - 0.9s

` Note: There's a delay in the search since the reviews are also passed through
the pre-trained sentiment analysis model.`
