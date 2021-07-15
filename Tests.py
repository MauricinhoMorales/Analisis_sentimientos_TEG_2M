import pandas as pd

from nltk.corpus import stopwords
from googletrans import Translator
from IPython.display import display
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import CountVectorizer

# translator = Translator()
# text = 'hola mundo'
# print(translator.translate(text).text)
# translated = GoogleTranslator(source='auto', target='english').translate('hola mundo')
# print(translated)

# corpus = [
# 'Great course. Love the professor.',
# 'Great content. Textbook was great',
# 'This course has very hard assignments. Great content.',
# 'Love the professor.',
# 'Hard assignments though',
# 'Hard to understand.'
# ]
# df = pd.DataFrame(corpus)
# df.columns = ['reviews']

# stoplist = stopwords.words('english')

# c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
# display(df['reviews'].head())
# # matrix of ngrams
# ngrams = c_vec.fit_transform(df['reviews'])
# print(type(ngrams))
# # count frequency of ngrams
# count_values = ngrams.toarray().sum(axis=0)
# # list of ngrams
# vocab = c_vec.vocabulary_
# df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)).rename(columns={0: 'frequency', 1:'bigram/trigram'})
# # display(df_ngram.head())


df = pd.read_csv('luisvicenteleon_Folder//Processed_Tweets.csv')
df['tweet_tokenized'] = df['tweet_tokenized'].apply(eval)

stoplist = stopwords.words('spanish') + ['https','co'] + ['pm','am'] + ['10', '11'] + ['_','lvl']

c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
# display(df['tweet'].head())
# matrix of ngrams
ngrams = c_vec.fit_transform(df['tweet'])
print(type(ngrams))
# count frequency of ngrams
count_values = ngrams.toarray().sum(axis=0)
# list of ngrams
vocab = c_vec.vocabulary_
df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)).rename(columns={0: 'frequency', 1:'bigram/trigram'})

display(df_ngram)