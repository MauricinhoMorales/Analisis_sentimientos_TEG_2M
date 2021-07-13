import os
import re
import sys
import numpy as np
import pandas as pd
import collections
from numpy import asarray
from numpy import savetxt
from IPython.core.display import Markdown, display


df_words_counter = pd.read_csv('tweets_list//prueba_words_counter.csv')
df_words_counter = df_words_counter.drop('Unnamed: 0',1)
df_words_counter = df_words_counter.sort_values(by="count", ascending=False)
df_words_counter = df_words_counter.head(100)
# df_words_counter['word'] = df_words_counter['word'].apply(eval)
word_list = df_words_counter['word'].tolist()
# display(df_words_counter)
# print(word_list)

df = pd.read_csv('tweets_list//tweets.csv')
df = df.drop('Unnamed: 0',1)
df['tweet_tokenized'] = df['tweet_tokenized'].apply(eval)
tweet_tokenized_lists = df['tweet_tokenized'].tolist()
# display(df)
# print(len(tweet_tokenized_lists))
# print(tweet_tokenized_lists)

df_to_records = df_words_counter.to_records(index=False)
counted_words = list(df_to_records)
# print(counted_words)

list_matrix = [[]]
list_matrix_index = list_matrix.copy()
list_matrix_index[0] = word_list
for tweet_tokenized in tweet_tokenized_lists:
    sub_list_matrix = []
    for word in word_list:
        for tweet_word in tweet_tokenized:
            if word == tweet_word:
                sub_list_matrix.append(1)
                break
            if tweet_word == tweet_tokenized[-1]:
                sub_list_matrix.append(0)
                break
    list_matrix.append(sub_list_matrix)
    list_matrix_index.append(sub_list_matrix)

# print(list_matrix_index)

list_matrix_index_df = pd.DataFrame(list_matrix_index)

new_header = list_matrix_index_df.iloc[0]
list_matrix_index_df = list_matrix_index_df[1:]
list_matrix_index_df.columns = new_header
list_matrix_index_df = list_matrix_index_df.assign(tweet_tokenized = tweet_tokenized_lists)

# display(list_matrix_index_df)
list_matrix_index_df.to_csv('tweets_list//prueba_matrix_frequent_words.csv')


# print(list_matrix)
# print(type(list_matrix))
# matrix = np.array(list_matrix)
# print(matrix)

# savetxt('tweets_list//matrix_frequent_words.csv', matrix, delimiter=',')