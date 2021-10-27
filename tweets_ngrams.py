import pandas as pd
import collections

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def monogram(folder):
    """Función que permite obtener las palabras que mas se repiten del corpus de un usuario"""
    df = pd.read_csv('{}//Results_Tweets.csv'.format(folder))
    df['tweet_tokenized'] = df['tweet_tokenized'].apply(eval)
    
    list_list_words = df['tweet_tokenized'].tolist()
    list_words = [item for sublist in list_list_words for item in sublist]
    
    words_counter = collections.Counter(list_words)
    words_counter_df = pd.DataFrame.from_dict(words_counter, orient='index').reset_index()
    words_counter_df = words_counter_df.rename(columns={'index':'word', 0:'count'})

    words_counter_df.to_csv('{}//Monograms.csv'.format(folder), index=False)

def bigram_trigram(folder):
    """Función que permite obtener las asociaciones de dos y tres palabras mas repetidas del corpus de un usuario"""
    df = pd.read_csv('{}//Results_Tweets.csv'.format(folder))
    stoplist = stopwords.words('spanish') + ['https','http'] + ['pm','am'] + ['10', '11'] + ['_','lvl'] + ['ja','eltiempolatino'] + ['today','unfollowers'] + ['and','followed'] + ['co', 'gt'] + ['followers','people'] + ['lt','dfk1urik4h'] + ['qhi53awlb9','2fshqrsmj3'] + ['maibortpetit','maibort'] + ['petit', 'stats'] + ['ee','uu'] + ['in','the'] + ['last','thank'] + ['you','day'] + ['live','on'] + ['el_pais','tc'] + ['twitcam','correodelcaroni'] + ['vs','17'] + ['20','2001'] + ['2001online','impresa']

    c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
    ngrams = c_vec.fit_transform(df['tweet'])
    count_values = ngrams.toarray().sum(axis=0)
    vocab = c_vec.vocabulary_
    df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)).rename(columns={0: 'frequency', 1:'bigram/trigram'})
    df_ngram.to_csv('{}//Bigrams_Trigrams.csv'.format(folder),index=False)

# Clase que se encarga de la recopilación de los conjuntos de monogramas, bigramas y trigramas provenientes del corpus
class tweets_ngrams():
    def __init__(self,type):
        """."""
        self.folder = type
    def monogramming(self):
        """."""
        monogram(self.folder)
    def ngraming(self):
        """."""
        bigram_trigram(self.folder)
