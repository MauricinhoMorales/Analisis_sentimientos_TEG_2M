import os
import twint
import re
import pandas as pd
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from deep_translator import GoogleTranslator

# Función que crea una carpeta (en caso de que no exista) con el nombre dado.
def create_folder(folder):
    
    if not os.path.exists(folder):
        os.makedirs(folder)

# Función que Recopila los tweets deseados usando diferentes filtros.
def scrape_info(user,quantity,folder):
    
    create_folder(folder)
    
    c = twint.Config()
    c.Username = user
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
    
    # Transformación del texto a minúsculas
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
    
    initial_words = list(word_list)
    final_words = [] 
    for token in word_list: # iterate over word_list
        if token not in stopwords.words(language):
            final_words.append(token)
    return str(final_words)

# Función que permite traducir un mensaje al idioma inglés
def googletrans_translate(text):
    
    return GoogleTranslator(source='auto', target='english').translate(text)

# Función que permite analizar el valor del sentimiento 
def assign_sentiment(row):
    
    if row['pos'] > row['neg'] and row['pos'] > row['neu']:
        return 'Positivo'
    elif row['neg']> row['neu']:
        return 'Negativo'
    else:
        return 'Neutral'
    
# Función que permite realizar el análisis de sentimientos usando la librería Vader.
def sentiment_analysis(folder):
    
    df = pd.read_csv("{}//Processed_Tweets.csv".format(folder))

    analyzer = SentimentIntensityAnalyzer()
    
    df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet_translated_tokenized']]
    df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet_translated_tokenized']]
    df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet_translated_tokenized']]
    
    df['sentiment'] = df.apply(assign_sentiment, axis=1)
    
    df.to_csv("{}//Processed_Tweets.csv".format(folder),index=False)

# Clase que se encarga de la recopilción, manejo y análisis de sentimientos de los tweets extraídos
class tweets_management():
    
    def __init__(self,user):
        
        self.user = user
        self.folder = user+"_Folder"
        self.translator = Translator()
        self.num_aux = 0
        
    def scraping(self,amount):
        
        scrape_info(self.user,amount,self.folder)
    
    def cleaning(self):
        df = pd.read_csv("{}//Raw_Tweets.csv".format(self.folder))
        
        df['tweet_tokenized'] = df['tweet'].apply(lambda x: clean_tokenized(x))
        df['tweet_tokenized'] = df['tweet_tokenized'].apply(lambda x: remove_stopwords(x,"spanish"))
        
        df['tweet_translated'] = df['tweet'].apply(lambda x: googletrans_translate(x,self.translator,self.num_aux))
        df['tweet_translated_tokenized'] = df['tweet_translated'].apply(lambda x: clean_tokenized(x))
        df['tweet_translated_tokenized'] = df['tweet_translated_tokenized'].apply(lambda x: remove_stopwords(x,"english"))
        
        df.to_csv('{}//Processed_Tweets.csv'.format(self.folder), columns=['tweet','tweet_tokenized','tweet_translated','tweet_translated_tokenized'],index=False)
    
    def sentiment_analysis(self):
        
        sentiment_analysis(self.folder)
        
    pass