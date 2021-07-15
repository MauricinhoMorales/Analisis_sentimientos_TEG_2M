import pandas as pd
import collections

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

# Función que permite obtener las palabras que mas se repiten del corpus dado
def monogram(folder):
    
    df = pd.read_csv('{}//Processed_Tweets.csv'.format(folder))
    df['tweet_tokenized'] = df['tweet_tokenized'].apply(eval)
    
    list_list_words = df['tweet_tokenized'].tolist()
    list_words = [item for sublist in list_list_words for item in sublist]
    
    words_counter = collections.Counter(list_words)
    words_counter_df = pd.DataFrame.from_dict(words_counter, orient='index').reset_index()
    words_counter_df = words_counter_df.rename(columns={'index':'word', 0:'count'})

    words_counter_df.to_csv('{}//Monograms.csv'.format(folder))

# Función que permite obtener las asociaciones de dos y tres palabras mas repetidas en el corpus
def bigram_trigram(folder):
    
    df = pd.read_csv('{}//Processed_Tweets.csv'.format(folder))
    
    stoplist = stopwords.words('spanish') + ['https','co'] + ['pm','am'] + ['10', '11'] + ['_','lvl']

    c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
    ngrams = c_vec.fit_transform(df['tweet'])
    count_values = ngrams.toarray().sum(axis=0)
    vocab = c_vec.vocabulary_
    df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)).rename(columns={0: 'frequency', 1:'bigram/trigram'})
    
    df_ngram.to_csv('{}//Bigrams_Trigrams.csv'.format(folder))

# Clase que se encarga de la obtención de palabras frecuentes y su asociación para determinar los temas presentes en el corpus
class tweets_ngrams():
    
    def __init__(self,user):
        
        self.user = user
        self.folder = user+"_Folder"
    
    def monogramming(self):
        
        monogram(self.folder)
    
    def ngraming(self):
        
        bigram_trigram(self.folder)
    
    pass