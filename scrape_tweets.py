import twint
import re
import pandas as pd
from googletrans import Translator
from textblob import TextBlob
from IPython.core.display import display

#---------------------------------------------------------------------------------------------------------------------------------

def scrape_info(user):
    #os.remove('prueba.csv')
      
    c = twint.Config()
    c.Username = user
    c.Limit = 1000
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

def googletrans_translate(text):
    translator = Translator()
    return translator.translate(text).text
    
#---------------------------------------------------------------------------------------------------------------------------------

scrape_info("luisvicenteleon")

df = pd.read_csv('tweets_list//prueba.csv')
# display(df.head())

df['tweet_tokenized'] = df['tweet'].apply(lambda x: clean_tokenized(x))
df['tweet_translated'] = df['tweet'].apply(lambda x: googletrans_translate(x))
# df['tweet_translated'] = df['tweet'].apply(lambda x: textblob_translate(x))
display(df[['tweet','tweet_translated']].head())


df.to_csv('tweets_list//tweets.csv', columns=['tweet','tweet_translated','tweet_tokenized'],index=False)