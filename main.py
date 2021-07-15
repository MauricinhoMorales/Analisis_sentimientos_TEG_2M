import os
from tweets_management import tweets_management
from tweets_classification import tweets_classification

def management():
    
    user_twitter = tweets_management('luisvicenteleon')

    # user_twitter.scraping(500)
    user_twitter.cleaning()
    user_twitter.sentiment_analysis()

def classification():
    
    sorter = tweets_classification('luisvicenteleon')

    sorter.training(0.25)
    sorter.test_Naive_Bayes()
    sorter.test_SVM()
    sorter.test_Decision_Forest()
    sorter.test_Max_Entropy()
    
management()
classification()