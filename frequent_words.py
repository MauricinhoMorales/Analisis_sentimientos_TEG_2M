import os
import re
import sys
import pandas as pd
import itertools
import collections
from textblob import TextBlob #para procesar datos de texto
from IPython.core.display import Markdown, display

from textblob import TextBlob
from textblob import Blobber
import nltk
from nltk.corpus import stopwords

spanish_stopwords = stopwords.words('spanish')
# print(type(spanish_stopwords))

df = pd.read_csv('tweets_list//prueba2.csv')

df['tweet_tokenized'] = df['tweet_tokenized'].apply(eval)           # PASO ABSOLUTAMENTE NECESARIO PARA QUE FUNCIONE

# for i, l in enumerate(df['tweet_tokenized']):                     # Comprobando el type de cada item en la columna
#     print("list",i,"is",type(l))

list_list_words = df['tweet_tokenized'].tolist()

list_words = [item for sublist in list_list_words for item in sublist]
# print(list_words)

filtered_list_words = [w for w in list_words if not w in spanish_stopwords]
# print(filtered_list_words)

words_counter = collections.Counter(filtered_list_words)
# print(type(words_counter))
# display(words_counter.most_common(15))

# test_df = pd.DataFrame(words_counter.most_common(15), columns=['words', 'count'])
# display(test_df)

words_counter_df = pd.DataFrame.from_dict(words_counter, orient='index').reset_index()
words_counter_df = words_counter_df.rename(columns={'index':'word', 0:'count'})
# display(words_counter_df)

words_counter_df.to_csv('tweets_list//prueba_words_counter.csv')