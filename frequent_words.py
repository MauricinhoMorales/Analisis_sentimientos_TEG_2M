import pandas as pd
import collections
from IPython.core.display import Markdown, display
from nltk.corpus import stopwords

spanish_stopwords = stopwords.words('spanish')

df = pd.read_csv('tweets_list//tweets.csv')

df['tweet_tokenized'] = df['tweet_tokenized'].apply(eval)           # PASO ABSOLUTAMENTE NECESARIO PARA QUE FUNCIONE

# for i, l in enumerate(df['tweet_tokenized']):                     # Comprobando el type de cada item en la columna
#     print("list",i,"is",type(l))

list_list_words = df['tweet_tokenized'].tolist()
list_words = [item for sublist in list_list_words for item in sublist]
filtered_list_words = [w for w in list_words if not w in spanish_stopwords]

words_counter = collections.Counter(filtered_list_words)
words_counter_df = pd.DataFrame.from_dict(words_counter, orient='index').reset_index()
words_counter_df = words_counter_df.rename(columns={'index':'word', 0:'count'})

words_counter_df.to_csv('tweets_list//prueba_words_counter.csv')