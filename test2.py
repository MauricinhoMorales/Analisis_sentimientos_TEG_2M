import sys
import twint
import pandas as pd
import psycopg2
import psycopg2.extras as extras
import os
import re

from textblob import TextBlob #para procesar datos de texto
from googletrans import Translator #libreria para traducir textos (Parece que tiene errores)
from google_trans_new import google_translator  #libreria para traducir textos

from sqlalchemy import create_engine
from IPython.display import display
from psycopg2 import OperationalError, errorcodes, errors

translator = google_translator() #variable global para inicializar el traductor

def scrape_info():
    #os.remove('prueba.csv')
    
    c = twint.Config()
    c.Search = "(Migración AND Venezuela) OR (Migración AND Venezolano)"
    # c.Search = ["Migración", "Venezuela"]
    c.Limit = 3000
    c.Count = True
    c.Lang = "es"
    # c.Near = "caracas"
    # c.Store_object = True
    # c.Output = "prueba.csv"
    # c.Since = "2018-01-01"
    # c.Hide_output = True
    c.Show_cashtags = False
    c.Store_csv = True
    c.Pandas = True
    c.Pandas_clean = True
    c.Store_pandas = True
    c.Popular_tweets = True
    c.Links = "exclude"
    # c.Replies = False
    c.Filter_retweets = True

    twint.run.Search(c)
    
def clean_tokenized(texto):
    '''
    Esta función limpia y tokeniza el texto en palabras individuales.
    El orden en el que se va limpiando el texto no es arbitrario.
    El listado de signos de puntuación se ha obtenido de: print(string.punctuation)
    y re.escape(string.punctuation)
    '''
    
    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de signos de puntuación
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
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

def first_clean_columns(df2):
    #------- Eliminar columnas innecesarias -------#
    
    df2 = df2.drop('conversation_id',1)
    df2 = df2.drop('created_at',1)
    df2 = df2.drop('timezone',1)
    df2 = df2.drop('user_id',1)
    df2 = df2.drop('place',1)
    df2 = df2.drop('language',1)
    df2 = df2.drop('mentions',1)
    df2 = df2.drop('urls',1)
    df2 = df2.drop('photos',1)
    df2 = df2.drop('hashtags',1)
    df2 = df2.drop('cashtags',1)
    df2 = df2.drop('link',1)
    df2 = df2.drop('retweet',1)
    df2 = df2.drop('quote_url',1)
    df2 = df2.drop('video',1)
    df2 = df2.drop('thumbnail',1)
    df2 = df2.drop('near',1)
    df2 = df2.drop('geo',1)
    df2 = df2.drop('source',1)
    df2 = df2.drop('user_rt_id',1)
    df2 = df2.drop('user_rt',1)
    df2 = df2.drop('retweet_id',1)
    df2 = df2.drop('reply_to',1)
    df2 = df2.drop('retweet_date',1)
    df2 = df2.drop('translate',1)
    df2 = df2.drop('trans_src',1)
    df2 = df2.drop('trans_dest',1)
    return(df2)

def translate_values(word):
    world_trans = translator.translate(word,lang_src='en', lang_tgt='es')
    #print(world_trans)
    return world_trans
#                                                                                                                          //
print('\n')

scrape_info()
#df = pd.read_csv('prueba.csv')

#------- Probando Metodos para operar DataFrames -------#

# display(df)                                       #Mostrar todo el Dataframe
#display(df.head())                                 #Mostrar las primeras 5 rows
# display(df.columns)                               #Mostrar todas las columnas del DataFrame
#display(df[['_id', 't_date', 't_time', 'username', 'place', 'tweet', 't_language', 'replies_count', 'retweets_count', 'likes_count', 'retweet']]) #Mostrar columnas especificas
#display(df.tweet)                                  #Mostrar solo los Tweets

# df2 = df                                          #Creando una copia para hacer pruebas
# df2 = first_clean_columns(df2)                    #Funcion para eliminar las columnas innecesarias y se guardan en una copia del Dataframe.
# display(df2.head())
# df2.to_csv('prueba2.csv')


# display(pd.read_csv('prueba2.csv'))


# df2['tweet_tokenized'] = df2['tweet'].apply(lambda x: clean_tokenized(x))
# display(df2[['tweet','tweet_tokenized']].head())

#------- ---------------------------- -------#

#------- Probando Funciones de Pandas -------#

#display(df2[df2.likes_count>10])           #Mostrar los Tweets que tengan mas de 10 likes
#display(df2.columns)
#display(df2.iat[0,5])                      #Mostrar un solo valor contenido en la posición 0,5 del DataFrame
#display(df2.at[0,'tweet'])                 #Mostrar un solo valor contenido en la row con el label '0' y la columna con el label 'tweet'
# tw = df2.iat[0,5]

# display(df2)

#------- ---------------------------- -------#

#----- Probando TextBlob -----#

#print(df2.at[0,'tweet'])
#analysis = TextBlob(df2.at[0,'tweet'])
#analysis = TextBlob("This table is black")
#print(analysis.sentiment)

#------- ---------------------------- -------#

#----- Probando leer un Diccionario -----#

# lexicon = pd.read_table(
#             'https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt',
#             names = ['termino', 'sentimiento']
#           )
# lexicon.to_csv(r'C:\Users\mike1\Documents\Mike\UCAB\Tesis\Python\AFINN-en-165.csv', index = False, header=True)

# lexicon = pd.read_csv('AFINN-en-165.csv')
# display(lexicon)

#------- ---------------------------- -------#

#----- Probando el Traductor -----#

# lexicon['termino_es'] = lexicon['termino'].apply(lambda x: translate_values(x))
# display(lexicon.head())
# lexicon.to_csv(r'C:\Users\mike1\Documents\Mike\UCAB\Tesis\Python\AFINN-es-165.csv', index = False, header=True)

#------- ---------------------------- -------#

#----- Agregando una columna al DataFrame con los Tweets limpios y Tokenizados -----#




print('\n')

#engine = create_engine('postgresql://postgres:26444352m@localhost:5432/TEG2Mv0.1')
#df.to_sql('prueba2', engine)
