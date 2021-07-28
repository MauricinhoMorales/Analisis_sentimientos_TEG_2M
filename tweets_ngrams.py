import pandas as pd
import collections

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

# Función que permite obtener las palabras que mas se repiten del corpus de un usuario
def monogram(folder):
    
    df = pd.read_csv('{}//Processed_Tweets.csv'.format(folder))
    df['tweet_tokenized'] = df['tweet_tokenized'].apply(eval)
    
    list_list_words = df['tweet_tokenized'].tolist()
    list_words = [item for sublist in list_list_words for item in sublist]
    
    words_counter = collections.Counter(list_words)
    words_counter_df = pd.DataFrame.from_dict(words_counter, orient='index').reset_index()
    words_counter_df = words_counter_df.rename(columns={'index':'word', 0:'count'})

    words_counter_df.to_csv('{}//Monograms.csv'.format(folder), index=False)

# Función que permite obtener las asociaciones de dos y tres palabras mas repetidas del corpus de un usuario
def bigram_trigram(folder):
    
    df = pd.read_csv('{}//Processed_Tweets.csv'.format(folder))
    stoplist = stopwords.words('spanish') + ['https','http'] + ['pm','am'] + ['10', '11'] + ['_','lvl'] + ['ja','eltiempolatino'] + ['today','unfollowers'] + ['and','followed'] + ['co', 'gt'] + ['followers','people'] + ['lt','dfk1urik4h'] + ['qhi53awlb9','2fshqrsmj3'] + ['maibortpetit','maibort'] + ['petit', 'stats'] + ['ee','uu'] + ['in','the'] + ['last','thank'] + ['you'+'day']

    c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
    ngrams = c_vec.fit_transform(df['tweet'])
    count_values = ngrams.toarray().sum(axis=0)
    vocab = c_vec.vocabulary_
    df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)).rename(columns={0: 'frequency', 1:'bigram/trigram'})
    df_ngram.to_csv('{}//Bigrams_Trigrams.csv'.format(folder),index=False)

# Función que permite obtener los conjuntos de bigramas y trigramas del corpus completo
def bigram_trigram_all_in_one(individual_folders,batch_folder,users_list):
    
    concat_df = pd.DataFrame()
    
    for user in users_list:
        df = pd.read_csv("{}//{}//Bigrams_Trigrams.csv".format(individual_folders,user+'_Folder',index=False))
        concat_df = concat_df.append(df)

    concat_df = concat_df.sort_values(by=['frequency'], ascending=False)
    concat_df = concat_df.rename(columns={'bigram/trigram':'bigram_trigram'})
    
    concat_df_2 = concat_df.groupby('bigram_trigram').agg({'frequency': sum}).reset_index()
    concat_df_2 = concat_df_2.sort_values(by=['frequency'], ascending=False)
    
    concat_df_2.to_csv('{}//Bigrams_Trigrams.csv'.format(batch_folder),index=False)

class tweets_ngrams():
    def __init__(self,user,dir):
        
        self.user = user
        if (type == 'users'):
            self.folder = "users//"+user+"_Folder"
        elif (type == 'batch'):
            self.folder = 'batch'
    
    def monogramming(self):
        
        monogram(self.folder)
    
    def ngraming(self):

        bigram_trigram(self.folder)
    
    def ngraming_in_one_file(self,users,batch,users_list):
        bigram_trigram_all_in_one(users,batch,users_list)
    pass