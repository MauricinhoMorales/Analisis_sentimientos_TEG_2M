import pandas as pd
import collections
from itertools import chain
from collections import Counter
from IPython.core.display import Markdown, display
from nltk.corpus import stopwords

spanish_stopwords = stopwords.words('spanish')

def find_ngrams(input_list, n):
    # print(input_list)
    return list(zip(*[input_list[i:] for i in range(n)]))

df_tweets = pd.read_csv('tweets_list//tweets.csv')
df_tweets = df_tweets.drop(columns='Unnamed: 0')

df_words_count = pd.read_csv('tweets_list//prueba_words_counter.csv')
df_words_count = df_words_count.drop(columns='Unnamed: 0')

df_matrix_words_counted = pd.read_csv('tweets_list//prueba_matrix_frequent_words.csv')
df_matrix_words_counted = df_matrix_words_counted.drop(columns=['Unnamed: 0'])

# print(df_matrix_words_counted.columns[100])
list_topics = []
word_index = -1

for x in df_matrix_words_counted.columns:
    
    word_index+=1
    if(word_index == 100):
        break
    
    word_test = df_matrix_words_counted.columns[word_index]      # Seleccionar la palabra a buscar del nombre de las columnas del DF.
    df_columns_specific_word = df_matrix_words_counted.loc[df_matrix_words_counted[word_test] != 0]     # DF donde salen las columnas donde aparece la palabra buscada.
    tweets_with_specific_word = df_columns_specific_word['tweet_tokenized']
    tweets_with_specific_word = tweets_with_specific_word.apply(eval)

    list_list_words = tweets_with_specific_word.tolist()
    filtered_tweets_with_specific_word = []
    
    for list_words in list_list_words:
        filtered = [w for w in list_words if not w in spanish_stopwords]
        filtered_tweets_with_specific_word.append(filtered)

    ngrams_tweets_with_specific_word = [find_ngrams(element, 2) for element in filtered_tweets_with_specific_word]
    ngrams_tweets_with_specific_word = list(chain(*ngrams_tweets_with_specific_word))
    ngrams_tweets_with_specific_word = [(x.lower(), y.lower()) for x,y in ngrams_tweets_with_specific_word]

    list_topics.append(ngrams_tweets_with_specific_word)
    # ngrams_tweets_with_specific_word_counter = Counter(ngrams_tweets_with_specific_word)
    # print(ngrams_tweets_with_specific_word_counter.most_common(10))

# print(len(list_topics))
list_bigrams_topics_unzipped = [item for sublist in list_topics for item in sublist]
list_bigrams_topics_counter = collections.Counter(list_bigrams_topics_unzipped)
print(list_bigrams_topics_counter.most_common(10))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
