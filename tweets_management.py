import os
import re
import twint
import pandas as pd

from nltk.corpus import stopwords

# Función que crea una carpeta (en caso de que no exista) con el nombre dado.
def create_folder(folder):
    
    if not os.path.exists(folder):
        os.makedirs(folder)

# Función que Recopila los tweets deseados usando diferentes filtros.
def scrape_info(quantity,folder):
    
    create_folder(folder)
    
    c = twint.Config()
    c.Search = "Covid-19"
    c.Limit = quantity
    c.Count = True
    c.Lang = "es"
    c.Store_object = True
    c.Output = "{}//Raw_Tweets.csv".format(folder)
    c.Show_cashtags = False
    c.Store_csv = True
    c.Pandas = True
    c.Pandas_clean = True
    c.Store_pandas = True
    c.Retweets = False
    c.Replies = False
    c.Native_retweets = False
    c.Hide_output = True
    
    twint.run.Search(c)
    
# Funcion que permite limpiar y tokenizar los tweets
def clean_tokenized(texto):
    
    # Se convierte todo el texto a minúsculas
    if(texto == None):
        texto = ''
    
    nuevo_texto = texto.lower()
    
    # Eliminación de páginas web 
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    
    # Eliminación de signos de puntuación
    regex = '[\\!\\"\\“\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    
    # Eliminación de números
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    
    # Eliminación de espacios en blanco múltiples
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    
    # Tokenización por palabras individuales
    nuevo_texto = nuevo_texto.split(sep = ' ')
    
    # Eliminación de tokens con una longitud < 2
    nuevo_texto = [token for token in nuevo_texto if len(token) > 1]
    
    return(nuevo_texto)

# Función que permite remover las palabras que no aportar valor al analisis en un idioma dado
def remove_stopwords(word_list, language):
    
    final_words = [] 
    for token in word_list: # iterate over word_list
        if token not in stopwords.words(language):
            final_words.append(token)
    return str(final_words)
class tweets_management():
    
    def __init__(self,type):
        self.folder = type

    def scraping(self,amount):
        scrape_info(amount,self.folder)
        
    def cleaning(self):
        
        df = pd.read_csv("{}//Raw_Tweets.csv".format(self.folder), encoding = 'unicode_escape')
        
        df['tweet_tokenized'] = df['tweet'].apply(lambda x: clean_tokenized(x))
        
        df['tweet_tokenized'] = df['tweet_tokenized'].apply(lambda x: remove_stopwords(x,"spanish"))
        
        df['tweet_tokenized_translated'] = df['tweet_translated'].apply(lambda x: clean_tokenized(x))
        
        df['tweet_tokenized_translated'] = df['tweet_tokenized_translated'].apply(lambda x: remove_stopwords(x,"english"))
        
        df.to_csv('{}//Processed_Tweets.csv'.format(self.folder), columns=['tweet','tweet_tokenized','tweet_translated','tweet_tokenized_translated',self.folder],index=False)
