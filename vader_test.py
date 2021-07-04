import os
import re
import sys
import twint
import pandas as pd
from textblob import TextBlob #para procesar datos de texto
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from IPython.core.display import Markdown, display

df = pd.read_csv('tweets_list//prueba2.csv')
# display(df.head())

# df2.at[0,'tweet']

analyzer = SentimentIntensityAnalyzer()
sentence = df.at[0,'tweet_translated']
# vs = analyzer.polarity_scores(sentence)
# print(sentence)
# print(vs)

df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df['tweet_translated']]
df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet_translated']]
df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet_translated']]
df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet_translated']]

display(df.head())

df.to_csv('tweets_list//prueba_result2.csv')