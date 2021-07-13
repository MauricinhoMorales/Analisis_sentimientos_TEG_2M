import twint
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from IPython.core.display import Markdown, display

df = pd.read_csv('tweets_list//prueba2.csv')

analyzer = SentimentIntensityAnalyzer()
sentence = df.at[0,'tweet_translated']

df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df['tweet_translated']]
df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet_translated']]
df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet_translated']]
df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet_translated']]

display(df.head())

df.to_csv('tweets_list//prueba_result2.csv')