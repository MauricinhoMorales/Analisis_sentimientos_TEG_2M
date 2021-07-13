import os
import re
import sys
import twint
import pandas as pd
from textblob import TextBlob #para procesar datos de texto
from IPython.core.display import Markdown, display

def sentiment_analysis_textBlob(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment[0]>0:
        return 'Positive'
    elif analysis.sentiment[0]<0:
        return 'Negative'
    else:
        return "No result"

df = pd.read_csv('tweets_list//tweets.csv')

df['label'] = df['text'].apply(lambda x: sentiment_analysis_textBlob(x))

df.to_csv('tweets_list//corpus2.csv', columns=['text','label'])