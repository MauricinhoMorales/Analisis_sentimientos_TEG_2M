import os
import re
import sys
import twint
import pandas as pd
from textblob import TextBlob #para procesar datos de texto
from IPython.core.display import Markdown, display

def sentiment_analysis_textBlob(tweet):
    analysis = TextBlob(tweet)
    analysis = analysis.translate(to='en')
    # print(analysis.sentiment)
    if analysis.sentiment[0]>0:
        return 'Positive'
    elif analysis.sentiment[0]<0:
        return 'Negative'
    else:
        return "No result"
#---------------------

df = pd.read_csv('tweets_list//prueba.csv')

df['sentiment'] = df['tweet_cleaned'].apply(lambda x: sentiment_analysis_textBlob(x))

# display(df[['tweet','tweet_tokenized']].head())
# display(df[['tweet','tweet_cleaned','sentiment']])

df.to_csv('tweets_list//prueba_result.csv', columns=['tweet','tweet_cleaned','tweet_tokenized','sentiment'])
# df.to_csv('tweets_list//prueba_result.csv', columns=['tweet','tweet_cleaned','sentiment'])