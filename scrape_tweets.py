import os
import re
import sys
import time
import twint
import pandas as pd
import goslate
from textblob import TextBlob
from IPython.core.display import Markdown, display

#---------------------------------------------------------------------------------------------------------------------------------

def scrape_info():
    #os.remove('prueba.csv')
      
    c = twint.Config()
    c.Username = "luisvicenteleon"  
    c.Limit = 10
    c.Count = True
    c.Lang = "es"
    c.Store_object = True
    c.Output = "tweets_list//prueba.csv"
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
    
def clean_tokenized(texto):
    
    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminación de páginas web (palabras que empiezan por "http")
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

def just_clean_text(texto):
    
    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de signos de puntuación
    regex = '[\\¡\\!\\"\\“\\”\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\..\\...\\/\\:\\;\\<\\=\\>\\¿\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    # Eliminación de números
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    # Eliminación de espacios en blanco múltiples
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    
    return(nuevo_texto)

def goslate_translate(text):
    # time.sleep(0.5)
    gs = goslate.Goslate()
    print(gs.translate(text, 'en'))

def textblob_translate(text):
    blob = TextBlob(text)
    return(blob.translate(to='en')) 
    

#---------------------------------------------------------------------------------------------------------------------------------

# scrape_info()

df = pd.read_csv('tweets_list//prueba.csv')
display(df.head())


# df2.at[0,'tweet']
# print(df.at[0,'tweet'])
# print(textblob_translate(df.at[0,'tweet']))


# df['tweet_tokenized'] = df['tweet'].apply(lambda x: clean_tokenized(x))
# df['tweet_cleaned'] = df['tweet'].apply(lambda x: just_clean_text(x))
# df['tweet_translated'] = df['tweet'].apply(lambda x: textblob_translate(x))
# display(df[['tweet','tweet_translated']].head())


# df.to_csv('tweets_list//prueba2.csv', columns=['tweet','tweet_translated','tweet_cleaned','tweet_tokenized'])

