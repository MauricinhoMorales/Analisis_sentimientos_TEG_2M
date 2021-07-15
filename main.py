import os
from tweets_management import tweets_management
from classification import classification
from ngrams import ngrams

user_twitter = tweets_management('luisvicenteleon')

# user_twitter.scraping(500)
# user_twitter.cleaning()
# user_twitter.sentiment_analysis()

sorter = classification('luisvicenteleon')

# sorter.training(0.3)
# sorter.test_naive_bayes()
# sorter.test_SVM()
# sorter.test_Decision_Forest()

user_tweets_ngrams = ngrams('luisvicenteleon')
user_tweets_ngrams.monogramming()
user_tweets_ngrams.ngraming()