"""."""
import collections
from itertools import permutations
import pandas as pd
from pandas.core.frame import DataFrame
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams, pr

SPANISH_STOPWORDS = stopwords.words('spanish') + ['si','mas'] + ['asi','mas']\
    + ['tan','hoy'] + ['@' + ','] + ['#','!'] + ['.',"?"] + ['de','bon']
SPANISH_STOPWORDS2 = ["@",",",".","!","?",";",":","(",")","J.","A.",\
    "$","''","La","O","EL","BA","as","``","&","gt","mm","2","da","I",\
    "Un","He","is","'m","Edo","Manuel","Daniel","Por","A","ser","�",\
    "*","the","this","account","�y","m�o","s�","m�s","recover","Bon"\
    "De","and","trusted","UV:0.0","Todopoderoso","de","really","TO","%",\
    "d�as","est�","transmisi�n","do","Saludos","DE","LA","E","to","be",\
    "muchas","dia","bueno","you","l�nea","IVSS","Meneses","4","ja","The",\
    "less","we","deserve","hope","AM","-","Amen","Am�n","c�dula","JesusJesusg2907",\
    "Juan","cedula","“","De","Lunes","hipismo","°C","│","...","Alex","Chacao","Beato",\
    "Jose","Gregorio","SE","menu","-los","puntos","Luisa","Buenos"]

def get_sentiment_general_probability_distribution(df: DataFrame):
    """."""
    df_lenght = len(df)
    sentiment_happiness = 0
    sentiment_sadness = 0
    sentiment_fear = 0
    sentiment_anger = 0
    for index, row in df.iterrows():
        if row['tweet_sentiment'] == 'felicidad':
            sentiment_happiness = sentiment_happiness + 1
        elif row['tweet_sentiment'] == 'tristeza':
            sentiment_sadness = sentiment_sadness + 1
        elif row['tweet_sentiment'] == 'miedo':
            sentiment_fear = sentiment_fear + 1
        elif row['tweet_sentiment'] == 'ira':
            sentiment_anger = sentiment_anger + 1
    percentage_happiness = (sentiment_happiness*100)/df_lenght
    percentage_sadness = (sentiment_sadness*100)/df_lenght
    percentage_fear = (sentiment_fear*100)/df_lenght
    percentage_anger = (sentiment_anger*100)/df_lenght

    print(round(percentage_happiness, 2))
    print(round(percentage_sadness, 2))
    print(round(percentage_fear, 2))
    print(round(percentage_anger, 2))

    return{
        "porcentaje_felicidad":round(percentage_happiness, 2),
        "porcentaje_tristeza":round(percentage_sadness, 2),
        "porcentaje_miedo":round(percentage_fear, 2),
        "porcentaje_ira":round(percentage_anger, 2)
    }

def get_opinion_general_probability_distribution(df: DataFrame):
    """."""
    df_lenght = len(df)
    opinion_for = 0
    opinion_against = 0
    opinion_neutro = 0
    for index, row in df.iterrows():
        if row['tweet_opinion'] == 'a favor':
            opinion_for = opinion_for + 1
        elif row['tweet_opinion'] == 'en contra':
            opinion_against = opinion_against + 1
        elif row['tweet_opinion'] == 'neutro':
            opinion_neutro = opinion_neutro + 1
    opinion_for = (opinion_for*100)/df_lenght
    opinion_against = (opinion_against*100)/df_lenght
    opinion_neutro = (opinion_neutro*100)/df_lenght

    print(round(opinion_for, 2))
    print(round(opinion_against, 2))
    print(round(opinion_neutro, 2))

    return{
        "porcentaje_a_favor":round(opinion_for, 2),
        "porcentaje_en_contra":round(opinion_against, 2),
        "porcentaje_neutro":round(opinion_neutro, 2)
    }

def get_general_probability_distribution(df: DataFrame):
    """."""
    df_lenght = len(df)
    sentiment_happiness = 0
    sentiment_sadness = 0
    sentiment_fear = 0
    sentiment_anger = 0
    opinion_for = 0
    opinion_against = 0
    opinion_neutro = 0
    for index, row in df.iterrows():
        if row['tweet_opinion'] == 'a favor':
            opinion_for = opinion_for + 1
        elif row['tweet_opinion'] == 'en contra':
            opinion_against = opinion_against + 1
        elif row['tweet_opinion'] == 'neutro':
            opinion_neutro = opinion_neutro + 1
        if row['tweet_sentiment'] == 'felicidad':
            sentiment_happiness = sentiment_happiness + 1
        elif row['tweet_sentiment'] == 'tristeza':
            sentiment_sadness = sentiment_sadness + 1
        elif row['tweet_sentiment'] == 'miedo':
            sentiment_fear = sentiment_fear + 1
        elif row['tweet_sentiment'] == 'ira':
            sentiment_anger = sentiment_anger + 1
    percentage_happiness = (sentiment_happiness*100)/df_lenght
    percentage_sadness = (sentiment_sadness*100)/df_lenght
    percentage_fear = (sentiment_fear*100)/df_lenght
    percentage_anger = (sentiment_anger*100)/df_lenght
    percentage_opinion_for = (opinion_for*100)/df_lenght
    percentage_opinion_against = (opinion_against*100)/df_lenght
    percentage_opinion_neutro = (opinion_neutro*100)/df_lenght
    return{
        "porcentaje_felicidad":round(percentage_happiness, 2),
        "porcentaje_tristeza":round(percentage_sadness, 2),
        "porcentaje_miedo":round(percentage_fear, 2),
        "porcentaje_ira":round(percentage_anger, 2),
        "porcentaje_a_favor":round(percentage_opinion_for, 2),
        "porcentaje_en_contra":round(percentage_opinion_against, 2),
        "porcentaje_neutro":round(percentage_opinion_neutro, 2)
    }


def get_category_probability_distribution_by_month(df: DataFrame, months_result:dict):
    """."""
    for index,row in df.iterrows():
        date_str = row['tweet_date']
        date = date_str.split('/')
        for month in months_result:
            if date[0] == month:
                if row['tweet_sentiment'] == 'felicidad':
                    months_result[month]['felicidad'] = months_result[month]['felicidad'] + 1
                elif row['tweet_sentiment'] == 'tristeza':
                    months_result[month]['tristeza'] = months_result[month]['tristeza'] + 1
                elif row['tweet_sentiment'] == 'miedo':
                    months_result[month]['miedo'] = months_result[month]['miedo'] + 1
                elif row['tweet_sentiment'] == 'ira':
                    months_result[month]['ira'] = months_result[month]['ira'] + 1
                if row['tweet_opinion'] == 'a favor':
                    months_result[month]['a favor'] = months_result[month]['a favor'] + 1
                elif row['tweet_opinion'] == 'en contra':
                    months_result[month]['en contra'] = months_result[month]['en contra'] + 1
                elif row['tweet_opinion'] == 'neutro':
                    months_result[month]['neutro'] = months_result[month]['neutro'] + 1
    return months_result

def get_probability_by_date(df: DataFrame):
    """."""
    month_list = []
    for index,row in df.iterrows():
        date_str = row['tweet_date']
        date = date_str.split('/')
        month_list.append(date[0])

    month = dict(zip(month_list,[month_list.count(i) for i in month_list]))
    month_result = {}
    for key in month.keys():
        month_result[key] = {}
        month_result[key]['tweets_quantity'] = month.get(key)
        month_result[key]['felicidad'] = 0
        month_result[key]['tristeza'] = 0
        month_result[key]['miedo'] = 0
        month_result[key]['ira'] = 0
        month_result[key]['a favor'] = 0
        month_result[key]['en contra'] = 0
        month_result[key]['neutro'] = 0
    return get_category_probability_distribution_by_month(df=df,months_result=month_result)

def get_category_probability_distribution_by_word(df: DataFrame, words_result: dict):
    """."""
    for index,row in df.iterrows():
        ngram = row['tweet_tokenized'].strip('][').split(', ')
        for word in ngram:
            word = word.replace("'","")
            for final_word in words_result:
                if word == final_word:
                    if row['tweet_sentiment'] == 'felicidad':
                        words_result[final_word]['felicidad'] = words_result[final_word]['felicidad'] + 1
                    elif row['tweet_sentiment'] == 'tristeza':
                        words_result[final_word]['tristeza'] = words_result[final_word]['tristeza'] + 1
                    elif row['tweet_sentiment'] == 'miedo':
                        words_result[final_word]['miedo'] = words_result[final_word]['miedo'] + 1
                    elif row['tweet_sentiment'] == 'ira':
                        words_result[final_word]['ira'] = words_result[final_word]['ira'] + 1
                    if row['tweet_opinion'] == 'a favor':
                        words_result[final_word]['a favor'] = words_result[final_word]['a favor'] + 1
                    elif row['tweet_opinion'] == 'en contra':
                        words_result[final_word]['en contra'] = words_result[final_word]['en contra'] + 1
                    elif row['tweet_opinion'] == 'neutro':
                        words_result[final_word]['neutro'] = words_result[final_word]['neutro'] + 1
    return words_result

def get_monograms_list(df: DataFrame):
    """."""
    ngrams_list = []
    for index,row in df.iterrows():
        ngram = row['tweet_tokenized'].strip('][').split(', ')
        for word in ngram:
            word = word.replace("'","")
            ngrams_list.append(word)
    filtered_list_words = [w for w in ngrams_list if not w in SPANISH_STOPWORDS]
    filtered_list_words = [w for w in filtered_list_words if not w in SPANISH_STOPWORDS2]
    words_counter = collections.Counter(filtered_list_words)
    words_counter = dict(words_counter.most_common(15))
    words_result = {}
    for key in words_counter.keys():
        words_result[key] = {}
        words_result[key]['frequency'] = words_counter.get(key)
        words_result[key]['felicidad'] = 0
        words_result[key]['tristeza'] = 0
        words_result[key]['miedo'] = 0
        words_result[key]['ira'] = 0
        words_result[key]['a favor'] = 0
        words_result[key]['en contra'] = 0
        words_result[key]['neutro'] = 0
    return get_category_probability_distribution_by_word(
            df=df,words_result=words_result)

def get_ngrams_list(df: DataFrame, ngram:int):
    """."""
    bigram_list = []
    for index,row in df.iterrows():
        token = nltk.word_tokenize(row['tweet'])
        bigram = list(ngrams(token, ngram))
        bigram_clean = [gram for gram in bigram if not any(stop in gram for stop in SPANISH_STOPWORDS)]
        bigram_clean = [gram for gram in bigram_clean if not any(stop in gram for stop in SPANISH_STOPWORDS2)]
        bigram_list.append(bigram_clean)
    ngrams_flat_list = [item for sublist in bigram_list for item in sublist]
    ngrams_counter = collections.Counter(ngrams_flat_list)
    ngrams_counter = ngrams_counter.most_common(15)
    ngram_df = pd.DataFrame(ngrams_counter, columns =['ngram', 'frecuency'])
    return ngram_df.to_dict('index')
