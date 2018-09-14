# CSF469 Information Retrieval Assignment

## Get the dataset

Software requirements: `python3` and `pip`

Run the following in the rootdir/

1. `pip3 install -r requirements.txt`

Run the following in rootdir/scraping/flipkart/

2. `scrapy crawl FlipkartProduct`

3. `scrapy crawl ProductSpider`

4. `scrapy crawl ReviewSpider`

Check for the pickles of each item in a dictionary {review title: review content} in the scraping/flipkart/infos

## Implementation
1. Each document contains the information, specs and reviews of all products scraped from Flipkart.
2. Content of all the reviews will be lemmatized, stop words will be removed and specs will be structured in a certain format.
3. Posting list of each word will be constructed.
4. Sentiment analysis model will be trained on a certain dataset and each document's combined review content is reviewed and sentiment is stored in a table according to the document.
5. According to the query, postings list is fetched -> Vectorized query and word -> scores calculated -> top 10 scores returned with an average sentiment analysis of the documents returned
